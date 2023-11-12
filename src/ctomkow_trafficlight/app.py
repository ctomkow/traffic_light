#!/usr/bin/env python3

import gpiod
from gpiod.line import Direction, Value
from flask import Flask, Response

LINE_RED = 9
LINE_YLW = 10
LINE_GRN = 11

app = Flask(__name__)

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

@app.route("/v1/trafficlight/red")
def red():
    toggle_light(LINE_RED)
    return Response(status=204)

@app.route("/v1/trafficlight/yellow")
def yellow():
    toggle_light(LINE_YLW)
    return Response(status=204)

@app.route("/v1/trafficlight/green")
def green():
    toggle_light(LINE_GRN)
    return Response(status=204)

if __name__ == "__main__":
    app.run()

