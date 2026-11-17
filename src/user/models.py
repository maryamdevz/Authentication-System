from sqlalchemy import Column, String, Integer
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    username = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hash_password = Column(String, nullable=False)