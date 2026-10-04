from core.models import BookBrief
def test_brief_defaults():
  b=BookBrief(title="x",audience="y")
  assert b.chapters==3 and b.words_per_chapter_min==600
