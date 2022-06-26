from flask import Blueprint, render_template, request, session
import threading
import multiprocessing
import psutil
import board
from .spi import RgbStrip

views = Blueprint("views", __name__)
spi = board.SPI()
rs = RgbStrip(spi)

def task(eh):
    while True:
        #print(f'Running task {threading.current_thread().name}')
        rs.rainbow_cycle(float(eh))

def task_runner(var=None):
    processes = psutil.Process().children()
    for p in processes:
        p.kill()
    if var is not None:
        process = multiprocessing.Process(target=task, args=(var,))
        process.start()


@views.route("/", methods=["GET", "POST"])
def home():
    r = 0
    g = 0
    b = 0
    if request.method == "POST":
        current_mode = request.form.get('modes')
        rainbow_speed = request.form.get('rainbow_speed')
        #print(request.form)

        if 'modes' in request.form:
            if current_mode == '1' or current_mode == '2':
                task_runner()
                r = int(request.form.get('color_r'))
                g = int(request.form.get('color_g'))
                b = int(request.form.get('color_b'))
                rs.set_color(r, g, b)
            elif current_mode == '3': 
                task_runner(rainbow_speed)

    return render_template("home.html")
