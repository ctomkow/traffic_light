#!/usr/bin/env python3

from threading import Thread
from time import sleep

import gpiod
from gpiod.line import Direction, Value
from flask import Flask, Response

LINE_RED = 9
LINE_YLW = 10
LINE_GRN = 11
global_current_line = 11
global_toggle_count = 0

app = Flask(__name__)

def light_control():
    while True:
        toggle_count = global_toggle_count
        current_line = global_current_line
        with gpiod.request_lines(
            "/dev/gpiochip0",
            consumer="blink-example",
            config={
                global_current_line: gpiod.LineSettings(
                    direction=Direction.OUTPUT, output_value=Value.ACTIVE
                )
            },
        ) as request:
            while True:
                # if light has changed, break out of loop
                if current_line != global_current_line:
                    break
                # if toggle_count has changed, toggle light
                if toggle_count != global_toggle_count:
                    toggle_count = global_toggle_count
                    line_status = request.get_value(global_current_line)
                    if line_status == Value.ACTIVE:
                        request.set_value(global_current_line, Value.INACTIVE)
                    else:
                        request.set_value(global_current_line, Value.ACTIVE)
                    sleep(0.1)
                    continue
                sleep(0.1)

@app.route("/v1/trafficlight/red")
def red():
    global global_current_line
    global global_toggle_count
    global_current_line = LINE_RED
    global_toggle_count += 1
    return Response(status=204)

@app.route("/v1/trafficlight/yellow")
def yellow():
    global global_current_line
    global global_toggle_count
    global_current_line = LINE_YLW
    global_toggle_count += 1
    return Response(status=204)

@app.route("/v1/trafficlight/green")
def green():
    global global_current_line
    global global_toggle_count
    global_current_line = LINE_GRN
    global_toggle_count += 1
    return Response(status=204)

if __name__ == "__main__":
    traffic_light_thread = Thread(target=light_control)
    traffic_light_thread.start()
    app.run(host='0.0.0.0', port=5000)

