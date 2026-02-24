import pytest
from unittest.mock import AsyncMock, MagicMock

from aiogram import types
from handlers.start import start

@pytest.fixture
def mock_message():
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    # answer is awaited, so make it an AsyncMock
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_start_handler_new_user(mock_session, mock_message):
    # Simulate DB returning no user
    mock_session.execute.return_value.scalar_one_or_none.return_value = None
    
    await start(mock_message, mock_session)
    
    # Verify user was added to session
    mock_session.add.assert_called_once()
    added_user = mock_session.add.call_args[0][0]
    assert added_user.id == 123
    
    # Verify welcome message
    mock_message.answer.assert_awaited_once()
    assert "Привет!" in mock_message.answer.await_args[0][0]

@pytest.mark.asyncio
async def test_start_handler_existing_user(mock_session, mock_user, mock_message):
    mock_message.from_user.id = mock_user.id
    
    # Simulate DB returning existing user
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    await start(mock_message, mock_session)
    
    # Verify no new user added
    mock_session.add.assert_not_called()
    
    # Verify welcome back message
    mock_message.answer.assert_awaited_once()
    assert "введи команду /help" in mock_message.answer.await_args[0][0]
