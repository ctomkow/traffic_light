#!/usr/bin/env python3

from threading import Thread
from time import sleep

import gpiod
from gpiod.line import Direction, Value
from flask import Flask, Response

LINE_RED = 9
LINE_YLW = 10
LINE_GRN = 11
current_line = 11
global_toggle_count = 0

app = Flask(__name__)

def toggle_light():
    toggle_count = global_toggle_count
    with gpiod.request_lines(
        "/dev/gpiochip0",
        consumer="blink-example",
        config={
            current_line: gpiod.LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
            )
        },
    ) as request:
        while True:
            if toggle_count != global_toggle_count:
                toggle_count = global_toggle_count
                line_status = request.get_value(current_line)
                if line_status == Value.ACTIVE:
                    request.set_value(current_line, Value.INACTIVE)
                else:
                    request.set_value(current_line, Value.ACTIVE)
                sleep(0.1)
                continue
            sleep(0.1)

@app.route("/v1/trafficlight/red")
def red():
    global current_line
    global global_toggle_count
    current_line = LINE_RED
    global_toggle_count += 1
    return Response(status=204)

@app.route("/v1/trafficlight/yellow")
def yellow():
    global current_line
    global global_toggle_count
    current_line = LINE_YLW
    global_toggle_count += 1
    return Response(status=204)

@app.route("/v1/trafficlight/green")
def green():
    global current_line
    global global_toggle_count
    current_line = LINE_GRN
    global_toggle_count += 1
    return Response(status=204)

if __name__ == "__main__":
    traffic_light_thread = Thread(target=toggle_light)
    traffic_light_thread.start()
    app.run(host='0.0.0.0', port=5000)

