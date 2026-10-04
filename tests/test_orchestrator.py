from core.models import BookBrief
from core.llm import LLMClient
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from agents.editor import EditorAgent
from agents.fact_checker import FactCheckerAgent
from core.orchestrator import BookOrchestrator

def test_demo_pipeline_runs():
  llm=LLMClient("demo")
  o=BookOrchestrator(PlannerAgent(llm),ResearcherAgent(llm),WriterAgent(llm),EditorAgent(llm),FactCheckerAgent(llm),max_revisions=1)
  b=o.run(BookBrief(title="Test",audience="Beginners",chapters=3))
  assert len(b.chapters)==3
  assert all(c.fact_check is not None for c in b.chapters)
