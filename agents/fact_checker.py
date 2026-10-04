from core.models import FactCheckResult, ResearchPacket
from tools.web import fetch_url
class FactCheckerAgent:
  def __init__(self, llm, timeout=20): self.llm=llm; self.timeout=timeout
  def run(self, draft: str, research: ResearchPacket) -> FactCheckResult:
    if self.llm.demo_mode:
      return FactCheckResult(status="revision_required", checks=[], issues=["Demo mode has no real citation evidence."])
    checks=[]; evidence=[]
    for s in research.sources:
      ok, text = fetch_url(s.url, self.timeout)
      checks.append({"citation_id":s.id,"url":s.url,"reachable":ok,"supports_claim":False,"reason":text[:300]})
      evidence.append({"id":s.id,"url":s.url,"reachable":ok,"page_text":text[:9000],"expected_claims":s.supports_claims})
    schema={"status":"verified | revision_required","checks":[{"citation_id":"integer","url":"string","reachable":"boolean","supports_claim":"boolean","reason":"string"}],"issues":["string"]}
    data=self.llm.ask_json("You are the Fact-checker. Every citation must have a reachable URL and source evidence supporting the attached claim. JSON only.", f"DRAFT:\n{draft}\nEVIDENCE:\n{evidence}", schema)
    result=FactCheckResult.model_validate(data)
    reach={c["citation_id"]:c["reachable"] for c in checks}
    for c in result.checks:
      if not reach.get(c.citation_id, False): c.reachable=False; c.supports_claim=False
    if any(not c.reachable or not c.supports_claim for c in result.checks): result.status="revision_required"
    return result
