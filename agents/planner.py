from core.models import BookBrief, BookPlan
class PlannerAgent:
  def __init__(self, llm): self.llm = llm
  def run(self, brief: BookBrief) -> BookPlan:
    schema = {"title":"string","audience":"string","chapters":[{"number":"integer","title":"string","purpose":"string","topics":["string"],"facts_needed":["string"]}]}
    data = self.llm.ask_json("You are the Planner. Create a logical 3-chapter outline. Identify factual items Researcher must verify. JSON only.", brief.model_dump_json(), schema)
    return BookPlan.model_validate(data)
