from core.models import BookBrief, ChapterPlan, EditorReview
class EditorAgent:
  def __init__(self, llm): self.llm = llm
  def run(self, brief: BookBrief, chapter: ChapterPlan, draft: str) -> EditorReview:
    schema = {"status":"approved | revision_required","issues":["string"]}
    inp = f"Brief:{brief.model_dump_json()}\nPlan:{chapter.model_dump_json()}\nDraft:\n{draft}"
    data = self.llm.ask_json("You are the Editor. Check grammar, tone, readability, word count, no bullet lists, Takeaway and citation/reference formatting. Do not fact-check sources. JSON only.", inp, schema)
    return EditorReview.model_validate(data)
