import pytest
from unittest.mock import patch
from app.ai_integration import summarize_text


@pytest.fixture
def mock_response():
    return {"candidates": [{"content": {"parts": [{"text": "This is a summary."}]}}]}


def test_summarize_text(mock_response):
    with patch("app.ai_integration.requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response

        result = summarize_text("This is a long text that needs summarizing.")
        assert result == "This is a summary."


def test_summarize_text_no_api_key():
    with patch("app.ai_integration.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API key for Gemini AI is not set"):
            summarize_text("This is a long text that needs summarizing.")
