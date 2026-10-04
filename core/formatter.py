from core.models import BookResult
def render_markdown(book: BookResult) -> str:
  out=[f"# {book.title}",""]
  for c in book.chapters:
    out += [f"## Chapter {c.number}: {c.title}","",c.content.strip(),"",f"Validation status: {c.fact_check.status if c.fact_check else 'unknown'}","","---",""]
  return "\n".join(out)
