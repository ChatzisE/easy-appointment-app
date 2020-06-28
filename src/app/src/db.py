import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,Boolean,
                        create_engine)
from sqlalchemy.sql import func
from databases import Database
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from src.api.models import UserDB

from settings import DATABASE_URL


# engine = create_engine(
#             DATABASE_URL, connect_args={"check_same_thread": False}
#             )
engine = create_engine(DATABASE_URL)

# SQLAlchemy

metadata = MetaData()
# databases query builder
database = Database(DATABASE_URL)


Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    user_name = Column(String,nullable=False)
    user_surname = Column(String, nullable=False)
    is_client = Column(Boolean, default=True, nullable=False)
    organization = Column(Integer,nullable=True)

Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)
