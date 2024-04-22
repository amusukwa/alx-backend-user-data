#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import dotenv

dotenv.load_dotenv()
# Define the database URI'
# 'postgresql://cv-me-db:cv-me-pwd@localhost:5432/cv-me-db'
DATABASE_URL ="postgresql://cvme:cvme88@localhost:5432/cvme"
print('DB', DATABASE_URL)
# Create the engine
engine = create_engine(DATABASE_URL)

# Create a session maker
Session = sessionmaker(bind=engine)
# Create a base class for declarative models
Base = declarative_base()

class BaseModel(Base):
    """
    Represents a base model in the system.

    Attributes:
        id (int): The unique identifier for the model.
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True)
