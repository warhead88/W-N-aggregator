import pytest
from unittest.mock import patch, AsyncMock
from aiohttp import ClientError

from services.news import get_news

@pytest.fixture
def mock_news_response():
    return {
        "totalArticles": 2,
        "articles": [
            {"title": "News 1", "description": "Desc 1", "url": "http://link1.com"},
            {"title": "News 2", "description": "Desc 2", "url": "http://link2.com"}
        ]
    }

@pytest.mark.asyncio
async def test_get_news_success(mock_news_response):
    with patch("services.news.aiohttp.ClientSession.get") as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_news_response
        mock_resp.raise_for_status = lambda: None
        
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        articles = await get_news(query="IT", country="ru")
        
        assert len(articles) == 2
        assert articles[0]["title"] == "News 1"
        assert articles[1]["url"] == "http://link2.com"
        
        # Verify params
        call_args, call_kwargs = mock_get.call_args
        params = call_kwargs.get("params", {})
        assert params.get("q") == "IT"
        assert params.get("country") == "ru"

@pytest.mark.asyncio
async def test_get_news_api_failure():
    with patch("services.news.aiohttp.ClientSession.get") as mock_get:
        mock_resp = AsyncMock()
        
        def raise_client_error():
            raise ClientError("API Error")
            
        mock_resp.raise_for_status = raise_client_error
        
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        with pytest.raises(ClientError):
            await get_news(query="Tech")
