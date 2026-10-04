import json
import time
from typing import Any
from core.config import (
  GEMINI_API_KEY,
  GEMINI_MIN_REQUEST_INTERVAL,
  GEMINI_MODEL,
  PROVIDER,
)


class LLMClient:
  def __init__(self, provider: str = PROVIDER):
    self.provider = provider
    self.model = GEMINI_MODEL
    self.client = None
    self._last_request_at = 0.0
    if provider == "gemini":
      if not GEMINI_API_KEY:
        raise RuntimeError("PROVIDER=gemini requires GEMINI_API_KEY in .env")
      from google import genai
      self.client = genai.Client(api_key=GEMINI_API_KEY)
    elif provider != "demo":
      raise ValueError("PROVIDER must be demo or gemini")

  @property
  def demo_mode(self):
    return self.provider == "demo"

  def _pace(self):
    if self.demo_mode:
      return
    elapsed = time.monotonic() - self._last_request_at
    if elapsed < GEMINI_MIN_REQUEST_INTERVAL:
      time.sleep(GEMINI_MIN_REQUEST_INTERVAL - elapsed)

  def ask(self, instructions: str, input_text: str) -> str:
    if self.demo_mode:
      return self._demo_text(input_text)
    self._pace()
    try:
      response = self.client.models.generate_content(
        model=self.model,
        contents=f"SYSTEM INSTRUCTIONS:\n{instructions}\n\nUSER INPUT:\n{input_text}",
      )
      self._last_request_at = time.monotonic()
      return response.text or ""
    except Exception as exc:
      self._last_request_at = time.monotonic()
      message = str(exc)
      if "429" in message or "RESOURCE_EXHAUSTED" in message:
        raise RuntimeError(
          "Gemini rate limit reached. The free-tier project is limited to a "
          "small number of requests per minute. Wait about 60 seconds and try again. "
          "This app now paces requests and uses one research call for the whole book."
        ) from exc
      raise

  def ask_json(self, instructions: str, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
    if self.demo_mode:
      return self._demo_json(input_text, schema)
    prompt = input_text + "\n\nReturn ONLY valid JSON. Schema:\n" + json.dumps(schema, indent=2)
    raw = self.ask(instructions, prompt).strip()
    if raw.startswith("```"):
      raw = raw.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(raw)

  def _demo_json(self, input_text: str, schema: dict[str, Any]) -> dict[str, Any]:
    text = json.dumps(schema).lower()
    if "research" in text:
      return {"research": []}
    if "chapters" in text and "facts_needed" in text:
      return {"title": "Pay Me on UPI: How Digital Payments Changed Small Business in India", "audience": "First-time small-business owners in India", "chapters": [
        {"number": 1, "title": "From Cash to Digital Payments", "purpose": "Explain the rise of digital payments.", "topics": ["UPI basics", "digital payments", "small businesses"], "facts_needed": ["UPI history", "official transaction statistics"]},
        {"number": 2, "title": "How UPI Fits a Small Business", "purpose": "Explain practical merchant use.", "topics": ["accepting payments", "customer convenience", "records"], "facts_needed": ["merchant payments", "transaction trends"]},
        {"number": 3, "title": "Using Digital Payments Safely", "purpose": "Explain safe payment habits.", "topics": ["payment verification", "fraud awareness", "record keeping"], "facts_needed": ["official safety guidance"]},
      ]}
    if "checks" in text:
      return {"status": "revision_required", "checks": [], "issues": ["Demo mode has no real citation evidence."]}
    return {"status": "approved", "issues": []}

  def _demo_text(self, input_text: str) -> str:
    return "DEMO MODE: This chapter is a workflow placeholder. Switch PROVIDER=gemini for AI-generated assessment content.\n\nTakeaway: Demo mode validates orchestration only.\n\nReferences\n[1] DEMO ONLY — https://example.com/demo"
