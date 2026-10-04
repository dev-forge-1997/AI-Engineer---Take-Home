from typing import Literal
from pydantic import BaseModel, Field

class BookBrief(BaseModel):
  title: str
  audience: str
  chapters: int = Field(default=3, ge=1, le=10)
  words_per_chapter_min: int = Field(default=600, ge=100)
  words_per_chapter_max: int = Field(default=900, ge=100)
  tone: str = "Friendly, clear and encouraging."
  extra_requirements: str = ""

class ChapterPlan(BaseModel):
  number: int
  title: str
  purpose: str
  topics: list[str]
  facts_needed: list[str]

class BookPlan(BaseModel):
  title: str
  audience: str
  chapters: list[ChapterPlan]

class Source(BaseModel):
  id: int
  source_name: str
  title: str
  url: str
  supports_claims: list[str]
  evidence: str

class ResearchPacket(BaseModel):
  chapter_number: int
  sources: list[Source]

class EditorReview(BaseModel):
  status: Literal["approved", "revision_required"]
  issues: list[str] = []

class CitationCheck(BaseModel):
  citation_id: int
  url: str
  reachable: bool
  supports_claim: bool
  reason: str

class FactCheckResult(BaseModel):
  status: Literal["verified", "revision_required"]
  checks: list[CitationCheck]
  issues: list[str] = []

class ChapterResult(BaseModel):
  number: int
  title: str
  content: str
  research: ResearchPacket
  editor: EditorReview | None = None
  fact_check: FactCheckResult | None = None
  revisions: int = 0

class BookResult(BaseModel):
  title: str
  chapters: list[ChapterResult]
