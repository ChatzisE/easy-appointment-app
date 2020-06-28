from fastapi_users import FastAPIUsers, models
from datetime import datetime
from pydantic import BaseModel


class User(models.BaseUser):
    user_name: str
    user_surname: str
    is_client: bool
    organization: int


class UserCreate(User, models.BaseUserCreate):
    user_name: str
    user_surname: str
    is_client: bool
    organization: int


class UserUpdate(User, models.BaseUserUpdate):
    user_name: str
    user_surname: str
    is_client: bool
    organization: int


class UserDB(User, models.BaseUserDB):
    user_name: str
    user_surname: str
    is_client: bool
    organization: int


class Appointment(BaseModel):
    user_id: str
    org_code: int
    org_name: str
    appointment_datetime: str


class Approval(BaseModel):
    org_code: int
    appointment_id: str
    appointment_datetime: datetime 
    user_id: str
