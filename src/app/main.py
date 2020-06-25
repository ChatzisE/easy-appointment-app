from fastapi import FastAPI
import uvicorn
import redis
import os
from src.api import ping, notes
from src.db import engine, metadata, database
from fastapi_users.authentication import JWTAuthentication
from settings import SECRET, REDIS_SERVER, REDIS_PASS
from fastapi_users import FastAPIUsers
from src.db import user_db
from src.api.models import User, UserCreate, UserUpdate, UserDB
from starlette.requests import Request
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pkg_resources
from fastapi.responses import FileResponse, PlainTextResponse

metadata.create_all(engine)

auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB, SECRET,
)

app.include_router(fastapi_users.router, prefix="/users", tags=["users"])

r = redis.StrictRedis(host=REDIS_SERVER, port=6379,
                      password=REDIS_PASS, charset="utf-8", decode_responses=True)


def fetch_organizations(reload) -> str:
    if r.exists('organizations') and reload is False:
        organizations = r.get("organizations")
    else:
        url = "https://hr.apografi.gov.gr/api/public/organizations"
        response = requests.get(url)
        organizations = response.text
        r.set('organizations', organizations)
    return organizations


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@fastapi_users.on_after_register()
def on_after_register(user: User, request: Request):
    print(f"User {user.id} has registered.")


@fastapi_users.on_after_forgot_password()
def on_after_forgot_password(user: User, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")



# @app.get("/")
# async def root():
#     if r.exists('visits') == 1:
#         visits = r.get("visits")
#         print("Read {} visits".format(visits))
#     else:
#         visits = 0
#     print("Save {} visits".format(int(visits) + 1))
#     r.set("visits", int(visits) + 1)
#     return {"message": "Hello World, visits {}".format(str(visits))}


@app.get("/organizations/{reload}/")
async def get_organizations(reload: bool):
    org = fetch_organizations(reload)
    return json.loads(org)


app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
if __name__ == "__main__":
    fetch_organizations(True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
