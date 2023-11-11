#!/usr/bin/env python3

import gpiod
from gpiod.line import Direction, Value
from fastapi import FastAPI

LINE_RED = 9
LINE_YLW = 10
LINE_GRN = 11

app = FastAPI()

def toggle_light(line):
    with gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="blink-example",
        config={
            line: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
            )
        },
    ) as request:
        status = request.get_value(line)
        if status == Value.ACTIVE:
            request.set_value(line, Value.INACTIVE)
        else:
            request.set_value(line, Value.ACTIVE)

@app.put("/v1/stoplight/red")
async def red():
    toggle_light(LINE_RED)

@app.put("/v1/stoplight/yellow")
async def yellow():
    toggle_light(LINE_YLW)

@app.put("/v1/stoplight/green")
async def green():
    toggle_light(LINE_GRN)
