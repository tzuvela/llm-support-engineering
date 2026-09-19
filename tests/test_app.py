import app

def test_ask_llm_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"output": [{"content": "Hello from the fake LLM"}]}

    def fake_post(url, json, timeout):
        return FakeResponse()

    monkeypatch.setattr(app.requests, "post", fake_post)
    result = app.ask_llm("Hello")
    assert result["output"][0]["content"] == "Hello from the fake LLM"


def test_ask_llm_request_failure(monkeypatch):
    def fake_post(url, json, timeout):
        raise app.requests.exceptions.RequestException("Connection failed")

    monkeypatch.setattr(app.requests, "post", fake_post)
    result = app.ask_llm("Hello")
    assert result is None


def test_ask_llm_invalid_json(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            raise ValueError("Invalid JSON")

    def fake_post(url, json, timeout):
        return FakeResponse()

    monkeypatch.setattr(app.requests, "post", fake_post)
    result = app.ask_llm("Hello")
    assert result is None


def test_print_response_unexpected_format(capsys):
    data = {"output": []}
    app.print_response(data)

    captured = capsys.readouterr()
    assert "Unexpected response format:" in captured.out