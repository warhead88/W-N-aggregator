import pytest
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession
from db.tables import User

@pytest.fixture
def mock_session():
    """Fixture to provide a mocked SQLAlchemy AsyncSession"""
    session = AsyncMock(spec=AsyncSession)
    
    from unittest.mock import MagicMock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_result.scalars.return_value.all.return_value = []
    
    session.execute.return_value = mock_result
    return session

@pytest.fixture
def mock_user():
    """Fixture to provide a mock User object"""
    return User(
        id=123456789,
        place="Kazan",
        query="IT",
        count=5,
        is_subscribed=True,
        timezone="Europe/Moscow"
    )
