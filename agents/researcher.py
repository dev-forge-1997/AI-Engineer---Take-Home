import json
from agents import AgentBase
from core.models import BookBrief, ChapterPlan, ResearchPacket
from tools.web import search_web, fetch_page


class ResearcherAgent(AgentBase):
  """Collect web evidence once for the whole book, then map it to chapters."""

  def run(self, brief: BookBrief, chapter: ChapterPlan) -> ResearchPacket:
    packets = self.run_all(brief, [chapter])
    return packets[chapter.number]

  def run_all(self, brief: BookBrief, chapters: list[ChapterPlan]) -> dict[int, ResearchPacket]:
    if self.llm.demo_mode:
      return {
        chapter.number: ResearchPacket(chapter_number=chapter.number, sources=[])
        for chapter in chapters
      }

    evidence_by_chapter = {}
    for chapter in chapters:
      query = (
        f"{brief.title} {chapter.title} {' '.join(chapter.facts_needed)} "
        "India NPCI RBI government official statistics"
      )
      candidates = search_web(query, 5)
      evidence = []
      for item in candidates:
        try:
          page = fetch_page(item["url"])
          evidence.append({
            "title": item["title"],
            "url": page["url"],
            "page_title": page["title"],
            "text": page["text"][:3500],
          })
        except Exception:
          continue
      evidence_by_chapter[chapter.number] = {
        "chapter": chapter.model_dump(),
        "evidence": evidence,
      }

    prompt = (
      f"BOOK BRIEF:\n{brief.model_dump_json()}\n\n"
      "For every chapter below, select only real sources supported by the supplied "
      "web evidence. Prefer NPCI, RBI, Government of India and reputable public sources. "
      "Never invent URLs. Return a separate research packet for every chapter.\n\n"
      f"WEB EVIDENCE BY CHAPTER:\n{json.dumps(evidence_by_chapter, ensure_ascii=False)}"
    )
    schema = {
      "research": [
        {
          "chapter_number": "integer",
          "sources": [
            {
              "id": "integer",
              "source_name": "string",
              "title": "string",
              "url": "string",
              "supports_claims": ["string"],
              "evidence": "string",
            }
          ],
        }
      ]
    }
    data = self.llm.ask_json(
      "You are the Researcher. Use only supplied web evidence.",
      prompt,
      schema,
    )

    result = {}
    for packet in data.get("research", []):
      validated = ResearchPacket.model_validate(packet)
      result[validated.chapter_number] = validated

    for chapter in chapters:
      result.setdefault(
        chapter.number,
        ResearchPacket(chapter_number=chapter.number, sources=[]),
      )
    return result
