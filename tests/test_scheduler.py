import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from zoneinfo import ZoneInfo
import datetime

from aiogram import Bot
from services.scheduler import check_and_send

@pytest.fixture
def mock_bot():
    return AsyncMock(spec=Bot)

@pytest.mark.asyncio
async def test_scheduler_no_subscribed_users(mock_bot, mock_session):
    # Setup: no users connected
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_session.execute.return_value = mock_result
    
    with patch("services.scheduler.get_async_session") as mock_get_session:
        mock_get_session.return_value.__aenter__.return_value = mock_session
        await check_and_send(mock_bot)
        
        mock_bot.send_message.assert_not_called()

@pytest.mark.asyncio
async def test_scheduler_subscribed_user_wrong_time(mock_bot, mock_session, mock_user):
    # Provide a user but patch datetime to be outside the delivery window (14:00 - 15:05)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_user]
    mock_session.execute.return_value = mock_result
    
    with patch("services.scheduler.get_async_session") as mock_get_session:
        # Mocking time to be 10:00:00 (outside window)
        mock_get_session.return_value.__aenter__.return_value = mock_session
        
        mock_now = datetime.datetime(2026, 1, 1, 7, 0, 0, tzinfo=datetime.timezone.utc)
        
        with patch("services.scheduler.datetime") as mock_datetime:
            mock_datetime.datetime.now.return_value = mock_now
            mock_datetime.time = datetime.time
            mock_datetime.timezone = datetime.timezone
            
            await check_and_send(mock_bot)
            
            mock_bot.send_message.assert_not_called()
