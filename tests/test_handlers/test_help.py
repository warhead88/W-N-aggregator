import pytest
from unittest.mock import AsyncMock, MagicMock

from aiogram import types
from handlers.help import show_help

@pytest.mark.asyncio
async def test_help_handler():
    mock_message = MagicMock(spec=types.Message)
    mock_message.answer = AsyncMock()
    
    await show_help(mock_message)
    
    mock_message.answer.assert_awaited_once()
    call_text = mock_message.answer.await_args[0][0]
    
    # Assert all commands are present in help text
    assert "/news" in call_text
    assert "/weather" in call_text
    assert "/forecast" in call_text
    assert "/menu" in call_text
