from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from settings import SECRET
from src.api.models import User, UserCreate, UserUpdate, UserDB, Appointment, Approval
from src.db import user_db
from src.api import crud
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
    if user.is_client:
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
    try:
        response = requests.put(
            "http://appointment-api:9000/appointment/backoffice/approve",
            data=json.dumps(dict(approval)))
        approved_appointment = json.loads(response.text)
        user = await crud.fetch_specific_user(approved_appointment.get('user_id'))
        mail_request = {
            'email': user._row.get('email'),
            'userName': user._row.get('user_name'),
            'userSurname': user._row.get('user_surname'),
            'appointmentDate': approval.appointment_datetime,
            "appointmentPlace": approved_appointment.get('org_name')
        }
        headers = {
            'Content-Type': 'application/json'
        }
        mail_response = requests.post(
            "http://mail-notifier:5000/MailNotifier",
            headers=headers,
            data=json.dumps(mail_request))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(mail_response)
    if mail_response.status_code != 200:
        raise HTTPException(status_code=mail_response.status_code, detail=mail_response.reason)
    return response.text
