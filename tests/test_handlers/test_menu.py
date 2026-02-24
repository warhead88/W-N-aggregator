import pytest
from unittest.mock import AsyncMock, MagicMock

from aiogram import types
from aiogram.fsm.context import FSMContext

from handlers.menu import open_menu, process_weather_place, change_place, Weather

@pytest.fixture
def mock_state():
    return AsyncMock(spec=FSMContext)

@pytest.fixture
def mock_message():
    msg = MagicMock(spec=types.Message)
    msg.from_user = MagicMock()
    msg.from_user.id = 123
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_open_menu_no_user(mock_message, mock_session):
    # Simulate DB returning no user
    mock_session.execute.return_value.scalar_one_or_none.return_value = None
    
    await open_menu(mock_message, mock_session)
    
    # Verify unauth message
    mock_message.answer.assert_awaited_once()
    assert "/start" in mock_message.answer.await_args[0][0]

@pytest.mark.asyncio
async def test_open_menu_existing_user(mock_message, mock_session, mock_user):
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    await open_menu(mock_message, mock_session)
    
    mock_message.answer.assert_awaited_once()
    # verify user info in text
    text = mock_message.answer.await_args[0][0]
    assert mock_user.place in text
    assert mock_user.timezone in text

@pytest.mark.asyncio
async def test_change_place_button(mock_state):
    mock_callback = MagicMock(spec=types.CallbackQuery)
    mock_callback.message = MagicMock()
    mock_callback.message.answer = AsyncMock()
    mock_callback.answer = AsyncMock()
    mock_callback.from_user = MagicMock()
    mock_callback.from_user.id = 123
    
    await change_place(mock_callback, mock_state)
    
    mock_state.set_state.assert_awaited_once_with(Weather.waiting_for_text)
    mock_callback.message.answer.assert_awaited_once()
    mock_callback.answer.assert_awaited_once()

@pytest.mark.asyncio
async def test_process_weather_place(mock_message, mock_state, mock_session, mock_user):
    mock_message.text = "Moscow"
    mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
    
    await process_weather_place(mock_message, mock_state, mock_session)
    
    assert mock_user.place == "Moscow"
    mock_message.answer.assert_awaited_once()
    assert "Moscow" in mock_message.answer.await_args[0][0]
    mock_state.clear.assert_awaited_once()
