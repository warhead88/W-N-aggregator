import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from aiogram import types
from handlers.weather import get_weather

@pytest.fixture
def mock_message():
    msg = MagicMock(spec=types.Message)
    msg.text = "/weather Kazan"
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_get_weather_invalid_format(mock_message):
    mock_message.text = "/weather" # No city provided
    await get_weather(mock_message)
    mock_message.answer.assert_awaited_once()
    assert "Введите команду в корректной форме" in mock_message.answer.await_args[0][0]

@pytest.mark.asyncio
async def test_get_weather_success(mock_message):
    with patch("handlers.weather.weather.get_weather") as mock_service:
        mock_service.return_value = {
            "name": "Kazan",
            "weather": [{"description": "clear"}],
            "main": {"temp": 15, "feels_like": 14, "temp_min": 10, "temp_max": 18, "humidity": 50, "pressure": 1010},
            "wind": {"speed": 5, "deg": 180, "gust": 7},
            "clouds": {"all": 0},
            "visibility": 10000,
            "sys": {"sunrise": 1234567, "sunset": 12345678}
        }
        
        await get_weather(mock_message)
        
        mock_service.assert_awaited_once_with("Kazan")
        mock_message.answer.assert_awaited_once()
        text = mock_message.answer.await_args[0][0]
        assert "Kazan" in text
        assert "clear" in text
        assert "15" in text

@pytest.mark.asyncio
async def test_get_weather_api_failure(mock_message):
    with patch("handlers.weather.weather.get_weather") as mock_service:
        mock_service.side_effect = Exception("API error")
        await get_weather(mock_message)
        
        assert "Не удалось получить погоду" in mock_message.answer.await_args[0][0]
