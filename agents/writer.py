from core.models import BookBrief, ChapterPlan, ResearchPacket
class WriterAgent:
  def __init__(self, llm): self.llm = llm
  def run(self, brief: BookBrief, chapter: ChapterPlan, research: ResearchPacket, previous_draft: str = "", feedback: list[str] | None = None) -> str:
    instructions = """You are the Writer. Write one chapter from supplied research only. Every factual claim, figure and date needs [n]. No bullet lists. Plain English, friendly mentor tone. Explain jargon on first use. Target the requested word count. End with one Takeaway: line, then References with [n] Source — Title — URL. Never invent a source or fact. Return chapter text only."""
    inp = f"Brief:\n{brief.model_dump_json()}\nChapter:\n{chapter.model_dump_json()}\nResearch:\n{research.model_dump_json()}\nPrevious draft:\n{previous_draft}\nFeedback:\n{feedback or []}"
    return self.llm.ask(instructions, inp)
