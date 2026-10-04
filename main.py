from agents.editor import EditorAgent
from agents.fact_checker import FactCheckerAgent
from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.writer import WriterAgent
from core.config import MAX_REVISIONS, PROVIDER, REQUEST_TIMEOUT
from core.llm import LLMClient
from core.models import BookBrief
from core.orchestrator import BookOrchestrator

def build_orchestrator(logger=print):
  llm=LLMClient(PROVIDER)
  return BookOrchestrator(PlannerAgent(llm),ResearcherAgent(llm),WriterAgent(llm),EditorAgent(llm),FactCheckerAgent(llm,REQUEST_TIMEOUT),MAX_REVISIONS,logger)

def run_default():
  brief=BookBrief(title="Pay Me on UPI: How Digital Payments Changed Small Business in India",audience="First-time small-business owners in India",chapters=3,words_per_chapter_min=600,words_per_chapter_max=900,tone="Friendly, clear and encouraging.")
  print(build_orchestrator().run(brief).model_dump_json(indent=2))
if __name__=="__main__": run_default()
