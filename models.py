from database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean, DateTime
import time
from datetime import datetime



class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key = True, nullable=False,)
    Name = Column(String,nullable=False,)
    Email = Column(String,nullable=False,)
    Password = Column(String,default=True,)
