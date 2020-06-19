import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import pkg_resources
from fastapi.responses import FileResponse, PlainTextResponse
import requests
import json
app = FastAPI()
# app.mount("/static", StaticFiles(directory=pkg_resources.resource_filename(__name__, 'static')), name="static")
#
#
# @app.get("/", include_in_schema=False)
# def root():
#     return FileResponse(pkg_resources.resource_filename(__name__, '/static/index.html'))


@app.get("/send-email", response_class=PlainTextResponse)
def send_mail():
    # defining the api-endpoint
    API_ENDPOINT = "http://localhost:5000/MailNotifier"
    # data to be sent to api
    data = {
        "email": "tzisxa1@gmail.com",
        "userName": "Nikos",
        "userSurname": "Koukos",
        "appointmentDate": "2020-06-18T14:01:54",
        "appointmentPlace": "Eforia kalamatas"
    }
    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, data=data)
    # extracting response text
    return r.text

@app.get("/organizations")
def get_organizations():
    # todo save response to redis 
    request = "https://hr.apografi.gov.gr/api/public/organizations"
    response = requests.get(request)
    return json.loads(response.text)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
