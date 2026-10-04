from core.models import BookBrief, BookResult, ChapterResult


class BookOrchestrator:
  def __init__(self, planner, researcher, writer, editor, fact_checker, max_revisions=1, logger=None):
    self.planner = planner
    self.researcher = researcher
    self.writer = writer
    self.editor = editor
    self.fact_checker = fact_checker
    self.max_revisions = max_revisions
    self.logger = logger or (lambda _: None)

  def run(self, brief: BookBrief) -> BookResult:
    self.logger("Planner: creating outline...")
    plan = self.planner.run(brief)
    chapter_plans = plan.chapters[:brief.chapters]

    # Research all chapters in one LLM call. Web fetching itself does not consume Gemini quota.
    self.logger("Researcher: collecting evidence for all chapters...")
    research_map = self.researcher.run_all(brief, chapter_plans)

    chapters = []
    for cp in chapter_plans:
      research = research_map[cp.number]
      draft = ""
      feedback = []
      editor = None
      fact = None
      attempt = 0

      for attempt in range(self.max_revisions + 1):
        self.logger(f"Writer: Chapter {cp.number}, round {attempt + 1}...")
        draft = self.writer.run(brief, cp, research, draft, feedback)

        self.logger(f"Editor: Chapter {cp.number}...")
        editor = self.editor.run(brief, cp, draft)
        if editor.status != "approved":
          feedback = editor.issues
          if attempt < self.max_revisions:
            continue

        self.logger(f"Fact-checker: Chapter {cp.number}...")
        fact = self.fact_checker.run(draft, research)
        if fact.status == "verified":
          break

        feedback = fact.issues
        # Reuse the same research packet on revision to avoid unnecessary API calls.
        # The next writer pass can correct the chapter using verified evidence.

        if attempt >= self.max_revisions:
          break

      chapters.append(
        ChapterResult(
          number=cp.number,
          title=cp.title,
          content=draft,
          research=research,
          editor=editor,
          fact_check=fact,
          revisions=attempt,
        )
      )

    return BookResult(title=plan.title, chapters=chapters)
