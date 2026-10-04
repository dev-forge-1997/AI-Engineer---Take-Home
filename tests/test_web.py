from tools.web import fetch_url

def test_invalid_url_is_not_verified():
  ok,_=fetch_url("http://127.0.0.1:1",timeout=1)
  assert ok is False
