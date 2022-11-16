from flask import Blueprint, render_template, request, session
import threading
import multiprocessing
import psutil
import board
from .spi import RgbStrip
import time

views = Blueprint("views", __name__)
spi = board.SPI()
rs = RgbStrip(spi)


def task(eh):
    while True:
        # print(f'Running task {threading.current_thread().name}')
        rs.rainbow_cycle(float(eh))


def steady_color(eh):
    while True:
        # print(f'Running task {threading.current_thread().name}')
        rs.set_color(*eh)
        time.sleep(3)


def task_runner(func=None, var=None):
    processes = psutil.Process().children()
    for p in processes:
        p.kill()
    if var is not None:
        process = multiprocessing.Process(target=func, args=(var,))
        process.start()


task_runner(steady_color, (100, 100, 100))


@views.route("/", methods=["GET", "POST"])
def home():
    r = 0
    g = 0
    b = 0
    if request.method == "POST":
        current_mode = request.form.get("modes")
        rainbow_speed = request.form.get("rainbow_speed")

        if "modes" in request.form:
            if current_mode == "1" or current_mode == "2":
                r = int(request.form.get("color_r"))
                g = int(request.form.get("color_g"))
                b = int(request.form.get("color_b"))
                task_runner(steady_color, (r, g, b))
            elif current_mode == "3":
                task_runner(task, rainbow_speed)

    return render_template("home.html")
