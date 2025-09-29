from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    place = Column(String)
    query = Column(String)
    count = Column(Integer)
    is_subscribed = Column(Boolean, default=False, nullable=False)
