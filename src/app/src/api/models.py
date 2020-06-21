from fastapi_users import FastAPIUsers, models

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



