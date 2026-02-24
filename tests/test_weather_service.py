import pytest
from unittest.mock import patch, AsyncMock
from aiohttp import ClientError

from services.weather import get_weather, get_forecast

@pytest.fixture
def mock_weather_response():
    return {
        "name": "Kazan",
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 15.5}
    }

@pytest.fixture
def mock_forecast_response():
    return {
        "list": [
            {
                "dt_txt": "2026-02-25 12:00:00",
                "main": {"temp": 10},
                "weather": [{"description": "rain"}]
            }
        ]
    }

@pytest.mark.asyncio
async def test_get_weather_success(mock_weather_response):
    with patch("services.weather.aiohttp.ClientSession.get") as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_weather_response
        mock_resp.raise_for_status = lambda: None
        
        # Setup context manager mock
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        result = await get_weather("Kazan")
        
        assert result["name"] == "Kazan"
        assert result["main"]["temp"] == 15.5

@pytest.mark.asyncio
async def test_get_forecast_success(mock_forecast_response):
    with patch("services.weather.aiohttp.ClientSession.get") as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = mock_forecast_response
        mock_resp.raise_for_status = lambda: None
        
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        result = await get_forecast("Kazan")
        
        assert len(result["list"]) == 1
        assert result["list"][0]["main"]["temp"] == 10

@pytest.mark.asyncio
async def test_weather_api_failure():
    with patch("services.weather.aiohttp.ClientSession.get") as mock_get:
        mock_resp = AsyncMock()
        
        def raise_client_error():
            raise ClientError("API Error")
            
        mock_resp.raise_for_status = raise_client_error
        
        mock_get.return_value.__aenter__.return_value = mock_resp
        
        with pytest.raises(ClientError):
            await get_weather("UnknownCity")
