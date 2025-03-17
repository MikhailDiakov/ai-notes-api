import pytest
from unittest.mock import AsyncMock, patch
from app.ai_integration import summarize_text


@pytest.fixture
def mock_response():
    return {"candidates": [{"content": {"parts": [{"text": "This is a summary."}]}}]}


@pytest.mark.asyncio
async def test_summarize_text(mock_response):
    async_mock = AsyncMock()
    async_mock.__aenter__.return_value = async_mock
    async_mock.json.return_value = mock_response

    with patch("aiohttp.ClientSession.post", return_value=async_mock):
        result = await summarize_text("This is a long text that needs summarizing.")

        assert result == "This is a summary."


@pytest.mark.asyncio
async def test_summarize_text_no_api_key():
    with patch("app.ai_integration.os.getenv", return_value=None):
        with pytest.raises(ValueError, match="API key for Gemini AI is not set"):
            await summarize_text("This is a long text that needs summarizing.")
