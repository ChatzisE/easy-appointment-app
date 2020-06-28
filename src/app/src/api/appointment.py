from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from settings import SECRET
from src.api.models import User, UserCreate, UserUpdate, UserDB, Appointment, Approval
from src.db import user_db
from fastapi import Body, Depends, HTTPException
import requests
import os
import json
import datetime

auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]

fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB, SECRET,
)
router = APIRouter()


def dt_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@router.get("/")
async def get_appointments(user: user_db = Depends(fastapi_users.authenticator.get_current_active_user)):
    response = None
    if (user.is_client):
        response = requests.get("http://appointment-api:9000/appointment/appoint/", params={"user_id": user.id})
    else:
        response = requests.get("http://appointment-api:9000/appointment/backoffice/",
                                params={"org_code": str(user.organization)})
        appointments = response.text
    return appointments


@router.post("/")
async def new_appointment(appointment: Appointment):
    payload = {
        'org_code': appointment.org_code,
        'org_name': appointment.org_name,
        'appointment_datetime': appointment.appointment_datetime
    }
    response = requests.post("http://appointment-api:9000/appointment/appoint/" + appointment.user_id,
                             data=json.dumps(payload))
    return response.text


@router.put("/")
async def approve_appointment(approval: Approval):
    response = requests.put(
        "http://appointment-api:9000/appointment/backoffice/approve",
        data=json.dumps(approval))
    # --todo send email, get user info from database
    mail_request = {
        'email': "tzisxa1@gmail.com",
        'userName': "Edwina",
        'userSurname': "Nakos",
        'appointmentDate': approval.appointment_datetime,
        "appointmentPlace": json.loads(response.text).org_name
    }
    mail_response = requests.post(
        "http://mail-notifier:5000/MailNotifier",
        data=json.dumps(mail_request))
    return response.text
