from flask import Blueprint, render_template, request, session
import threading
import multiprocessing
import psutil
import board
from .spi import RgbStrip, Snake
import time
import ctypes

views = Blueprint("views", __name__)
spi = board.SPI()
rs = RgbStrip(spi)

SetColors = ["#ffffff", "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#00ffff", "#ff00ff", "#000000", "#224fdd"]
Modes = ["set", "manual", "rainbow", "fireflies", "walker", "pin ball", "noise", "snake"]
snake_speed = multiprocessing.Value("f", 0.0)
snake_config = multiprocessing.Value("i", 1)
snake_turn = multiprocessing.Value("i", 1)

def steady_color(eh):
    while True:
        rs.set_color(*eh)
        time.sleep(3)

def rainbow(eh):
    while True:
        #print(f'Running task {threading.current_thread().name}')
        rs.rainbow_cycle(float(eh))

def fireflies(eh):
    while True:
        rs.fireflies(eh)

def walker(eh):
    while True:
        rs.walker.walker(float(eh))

def pinball(eh):
    while True:
        rs.pinball.pinball(eh)

def noise_loop(eh):
    while True:
        rs.noise.noise_loop(float(eh))

def snake(eh):
    while True:
        rs.snake.game_loop(eh[0].value, eh[1].value, eh[2].value)

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
        current_mode = request.form.get('modes')
        rainbow_speed = request.form.get('rainbow_speed')
        walker_speed = request.form.get('walker_speed')

        if request.form.get('updated_snake_speed') is not None:
            snake_speed.value = float(request.form.get('updated_snake_speed'))

        if request.form.get('updated_snake_config') is not None:
            snake_config.value = int(request.form.get('updated_snake_config'))

        if request.form.get('turn_req') is not None:
            snake_turn.value = int(request.form.get('turn_req'))

        if 'modes' in request.form:
            if current_mode == '1' or current_mode == '2':
                # task_runner()
                r = int(request.form.get('color_r'))
                g = int(request.form.get('color_g'))
                b = int(request.form.get('color_b'))
                # rs.set_color(r, g, b)
                task_runner(steady_color, (r, g, b))
            elif current_mode == '3': 
                task_runner(rainbow, rainbow_speed)
            elif current_mode == '4': 
                task_runner(fireflies, 1)
            elif current_mode == '5': 
                task_runner(walker, walker_speed)
            elif current_mode == '6': 
                task_runner(pinball, 1)
            elif current_mode == '7': 
                task_runner(noise_loop, 1)
            elif current_mode == '8': 
                snake_speed.value = float(request.form.get('snake_speed'))
                snake_config.value = int(request.form.get('current_snake_config'))
                task_runner(snake, (snake_speed, snake_config, snake_turn))

    return render_template("home.html", ColorsLen=len(SetColors), SetColors=SetColors, ModesLen=len(Modes), Modes=Modes)
