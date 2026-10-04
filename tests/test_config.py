import os

def test_no_ollama_dependency():
  assert not os.path.exists("ollama")
