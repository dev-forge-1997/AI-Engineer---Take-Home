import streamlit as st
from core.config import PROVIDER
from core.formatter import render_markdown
from core.models import BookBrief
from main import build_orchestrator

st.set_page_config(page_title="Multi-Agent Book Writer", layout="wide")
st.title("📚 Multi-Agent Book Writer")
st.caption("Planner → Researcher → Writer → Editor → Fact-checker")
if PROVIDER == "demo":
  st.warning("DEMO MODE: no AI credential is used. This mode validates the workflow only and must not be submitted as research evidence.")
else:
  st.success(f"LLM provider: {PROVIDER}")

title=st.text_input("Book title","Pay Me on UPI: How Digital Payments Changed Small Business in India")
audience=st.text_input("Audience","First-time small-business owners in India")
chapters=st.number_input("Chapters",1,5,3)
min_words,max_words=st.slider("Words per chapter",400,1200,(600,900))
tone=st.text_input("Tone","Friendly, clear and encouraging, like a mentor.")
if st.button("Generate Book", type="primary"):
  logs=[]
  def log(msg): logs.append(msg); st.write("• "+msg)
  brief=BookBrief(title=title,audience=audience,chapters=int(chapters),words_per_chapter_min=min_words,words_per_chapter_max=max_words,tone=tone)
  try:
    book=build_orchestrator(log).run(brief)
    md=render_markdown(book)
    st.download_button("Download Markdown",md,file_name="book.md")
    st.markdown(md)
  except Exception as exc:
    st.error(str(exc))
