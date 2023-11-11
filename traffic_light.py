#!/usr/bin/env python3

import time
from datetime import datetime
from zoneinfo import ZoneInfo
import pprint

import gpiod
from gpiod.line import Direction, Value
import requests
import msal

LINE_RED = 9
LINE_YLW = 10
LINE_GRN = 11

def acquire_token():
    """
    Acquire token via MSAL
    """
    authority_url = 'https://login.microsoftonline.com/{tenant_id_or_name}'
    app = msal.ConfidentialClientApplication(
        authority=authority_url,
        client_id='{client_id}',
        client_credential='{client_secret}'
    )
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token

# calendar
cal_details = {
    "Schedules": ["craig.tomkow@bc.net"],
    "StartTime": {
        "dateTime": f'{datetime.now(tz=ZoneInfo("America/Edmonton")).replace(microsecond=0,second=0,minute=0,hour=9).isoformat()[:-6]}',
        "timeZone": "Mountain Standard Time"
    },
    "EndTime": {
        "dateTime": f'{datetime.now(tz=ZoneInfo("America/Edmonton")).replace(microsecond=0,second=0,minute=0,hour=18).isoformat()[:-6]}',
        "timeZone": "Mountain Standard Time"
    },
               "availabilityViewInterval": "15"
}

r = requests.post('https://graph.microsoft.com/v1.0/me/calendar/getschedule', data=cal_details)
pprint.pprint(r.json())
raise SystemExit


with gpiod.request_lines(
    "/dev/gpiochip0",
    consumer="blink-example",
    config={
        LINE_GRN: gpiod.LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    while True:
        request.set_value(LINE_GRN, Value.ACTIVE)
        time.sleep(1)
        #request.set_value(LINE, Value.INACTIVE)
        time.sleep(1)