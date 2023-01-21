#!/usr/bin/env python3

import time
import board
import neopixel_spi as neopixel
import sys
import random

class SnakeSegment():
    def __init__(self, pos, action=1):
        self.pos = pos
        self.action = action
    
    def __repr__(self):
        return f'SnakeSegment(pos={self.pos})'

    def go(self, pixels_num):
        self.pos += self.action
        self.pos = (self.pos % pixels_num)
    

class Snake():
    def __init__(self, pixels, pixels_num):
        self.pixels = pixels
        self.pixels_num = pixels_num
        self.snake_color = (0, 100, 0)
        self.apple_color = (100, 0, 0)
        self.p = self.pixels_num // 2
        self.snake_length = 3
        self.direction = True
        self.apple_pos = None
        self.cant_change = False
        # self.time_now = int(round(time.time()))

        self.snake_body = [ SnakeSegment(s) for s in range(self.snake_length-1+self.p, -1+self.p, -1) ]

    def game_loop(self, wait, c_or_p, turn):
        while self.apple_pos is None:
            self.apple_pos = random.randint(0, self.pixels_num - 1)
            if all([i == j for i, j in zip(self.pixels[self.apple_pos], self.snake_color)]):
                self.apple_pos = None
        
        self.pixels.fill((0, 0, 0))

        self.pixels[self.apple_pos] = self.apple_color

        if c_or_p == 1:
            self.change_direction()
        else:
            if turn == 1:
                self.direction = False
            else:
                self.direction = True 


        if self.direction:
            self.snake_body[0].action = 1
        else:
            self.snake_body[0].action = -1

        if all([i == j for i, j in zip(self.pixels[(self.snake_body[0].pos+1) % self.pixels_num], self.apple_color)]):
            last_seg = self.snake_body[-1]
            first_seg = self.snake_body[0]
            self.snake_body.insert(0, SnakeSegment((first_seg.pos+first_seg.action) % self.pixels_num, first_seg.action))
            self.apple_pos = None
            for sb in self.snake_body:
                self.pixels[sb.pos] = self.snake_color
        else:
            for sb in self.snake_body:
                sb.go(self.pixels_num)
                self.pixels[sb.pos] = self.snake_color

            for i in range(len(self.snake_body)-1, 0, -1):
                self.snake_body[i].action = self.snake_body[i-1].action

        if len(self.snake_body) >= 127:
            self.end()

        self.pixels.show()
        time.sleep(wait)

    def end(self):
        self.pixels.fill(self.snake_color)
        self.pixels.show()
        time.sleep(0.5)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        time.sleep(0.5)
        self.pixels.fill(self.snake_color)
        self.pixels.show()
        time.sleep(0.5)
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        time.sleep(0.5)
        self.snake_body = [ SnakeSegment(s) for s in range(self.snake_length-1+self.p, -1+self.p, -1) ]

    def change_direction(self):
        current_pos = self.snake_body[0].pos
        if current_pos >= self.apple_pos :
            left = abs(current_pos - self.apple_pos)
            right = self.apple_pos + (self.pixels_num - current_pos) + 1 
        else:
            right = abs(current_pos - self.apple_pos)
            left = current_pos + (self.pixels_num - self.apple_pos) + 1 
        if left < right:
            self.direction = False
        else:
            self.direction = True
        # if int(round(time.time())) > self.time_now + random.randint(3, 8):
        #     self.cant_change = False
        # if not self.cant_change:
        #     self.direction = not self.direction
        #     self.time_now = int(round(time.time()))
        #     self.cant_change = True


class PinBall():
    def __init__(self, pixels, pixels_num):
        self.pixels = pixels
        self.pixels_num = pixels_num

        self.tower_color = (150, 0, 0)
        self.hit_color = (0, 150, 0)
        self.ball_color = (0, 150, 0)
        self.towers = range(10, self.pixels_num, 10)
        self.pos = 0
        self.delta = 1

    def rand(self, i):
        return random.getrandbits(20) % i

    def pinball(self, eh):
        self.fill()
        for i in self.towers:
            self.pixels[i] = self.tower_color
        self.pixels.show()
        self.pos = 0
        self.delta = 1
        while True:
            if self.pos in self.towers:
                self.pixels[self.pos] = self.tower_color
            else:
                self.pixels[self.pos] = (0, 0, 0)

            self.pos = self.pos + self.delta

            if self.pos == self.pixels_num:
                break
            elif self.pos < 0:
                self.delta = -self.delta
                self.pos = 0
                continue

            if self.pos in self.towers:
                self.pixels[self.pos] = self.hit_color
                if self.rand(4) > 0:
                    self.delta = -self.delta
            else:
                self.pixels[self.pos] = self.ball_color
            self.pixels.show()
            time.sleep(0.01)

    def fill(self):
        self.pixels.fill((0, 0, 0))
        for i in range(self.pixels_num):
            self.pixels[i] = self.tower_color
            self.pixels.show()
            time.sleep(0.01)


class Noise:
    def __init__(self, pixels, leds_num):
        self.color1 = (0,0,255)
        self.color2 = (0,153,153)
        self.color3 = (255, 50, 255)
        self.color4 = (10, 25, 217)
        self.color5 = (50, 50, 150)
        self.color6 = (230, 0, 10)
        self.color7 = (0, 160, 0)
        self.color8 = (1, 0, 1)
        self.color9 = (100, 100, 0)
        self.color1 = (0,0,255)
        self.color2 = (0,153,153)
        self.color3 = (255, 50, 255)
        self.color4 = (10, 25, 217)
        self.color5 = (50, 50, 150)
        self.color6 = (230, 0, 10)
        self.color7 = (0, 160, 0)
        self.color8 = (100, 100, 0)
        self.color9 = (0, 0, 0)
        self.pixels = pixels
        self.leds_num = leds_num

    def noise_setup(self):
        for i in range(self.leds_num//2, 0, -1):
            self.pixels[i] = (152, 0, 10)
            self.pixels[self.leds_num-i] = (152, 0, 10)
            time.sleep(0.04)
            self.pixels.show()

    def noise_loop(self, eh):
        self.noise_setup()
        while True:
            s = random.randint(50, 250)
            s = s*2

            if s >= 450 and s <= 540:
                self.pixels[self.leds_num//2 - 1] = self.color1
                self.pixels[self.leds_num//2] = self.color1

            elif s >= 400 and s <= 450:
                self.pixels[self.leds_num//2 - 1] = self.color2
                self.pixels[self.leds_num//2] = self.color2

            elif s >= 350 and s <= 400:
                self.pixels[self.leds_num//2 - 1] = self.color3
                self.pixels[self.leds_num//2] = self.color3

            elif s >= 300 and s <= 350:
                self.pixels[self.leds_num//2 - 1] = self.color4
                self.pixels[self.leds_num//2] = self.color4

            elif s >= 276 and s <= 300:
                self.pixels[self.leds_num//2 - 1] = self.color5
                self.pixels[self.leds_num//2] = self.color5

            elif s >= 250 and s <= 275:
                self.pixels[self.leds_num//2 - 1] = self.color6
                self.pixels[self.leds_num//2] = self.color6

            elif s >= 235 and s <= 250:
                self.pixels[self.leds_num//2 - 1] = self.color7
                self.pixels[self.leds_num//2] = self.color7

            elif s >= 200 and s <= 230:
                self.pixels[self.leds_num//2 - 1] = self.color8
                self.pixels[self.leds_num//2] = self.color8

            else:
                self.pixels[self.leds_num//2 - 1] = self.color9
                self.pixels[self.leds_num//2] = self.color9

            for i in range(self.leds_num//2 - 1):
                self.pixels[i] = self.pixels[i + 1]
                self.pixels[self.leds_num - 2 - i] = self.pixels[self.leds_num - i - 3]

            self.pixels.show()
            time.sleep(0.025)


class Walker:
    def __init__(self, pixels, pixels_num):
        self.pixels = pixels
        self.pixels_num = pixels_num

        self.walker_index = 0
        self.current_side = 1
        self.current_phase = 1
        self.current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def walker(self, wait):
        if self.walker_index < 0:
            self.current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if not self.current_side:
                self.current_phase = not self.current_phase
                self.walker_index += 1
            else:
                self.walker_index = self.pixels_num-1
            self.current_side = not self.current_side

        if self.walker_index > self.pixels_num-1:
            self.current_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            if not self.current_side:
                self.current_phase = not self.current_phase
                self.walker_index -= 1
            else:
                self.walker_index = 0
            self.current_side = not self.current_side
        if self.current_side:
            self.pixels[self.walker_index] = self.current_color
        else:
            self.pixels[self.walker_index] = (0, 0, 0)

        self.pixels.show()
        time.sleep(wait)
        if self.current_phase:
            self.walker_index += 1
        else:
            self.walker_index -= 1


class RgbStrip:
    Colors = [
        #[232, 100, 255],  # Purple
        #[100, 100, 255],  # Yellow
        #[30, 200, 200],  # Blue
        #[150,50,10],
        #[50,200,10],
        [30, 200, 255],
        [30, 0, 255],
        [30, 100, 255],
        [0, 200, 255],
        [0, 0, 255],
    ]

    Max_len = 20
    Min_len = 5
    Flashing = []

    Num_flashes = 20

    def __init__(self, spi):
        self.num_pixels = 127
        self.pixel_order = neopixel.GRB

        # spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(
            spi, self.num_pixels, brightness=1.0, auto_write=False, pixel_order=self.pixel_order, bit0=0b10000000
        )

        self.walker = Walker(self.pixels, self.num_pixels)
        self.pinball = PinBall(self.pixels, self.num_pixels)
        self.noise = Noise(self.pixels, self.num_pixels)
        self.snake = Snake(self.pixels, self.num_pixels)

        for i in range(RgbStrip.Num_flashes):
            pix = random.randint(0, self.num_pixels - 1)
            col = random.randint(1, len(RgbStrip.Colors) - 1)
            flash_len = random.randint(RgbStrip.Min_len, RgbStrip.Max_len)
            RgbStrip.Flashing.append([pix, RgbStrip.Colors[col], flash_len, 0, 1])

    def wheel(self, pos):
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.pixel_order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def set_color(self, r, g, b):
        self.pixels.fill((r, g, b))
        self.pixels.show()

    def fireflies(self, some):
        for i in range(RgbStrip.Num_flashes):
            pix = RgbStrip.Flashing[i][0]
            brightness = (RgbStrip.Flashing[i][3]/RgbStrip.Flashing[i][2])
            colr = (int(RgbStrip.Flashing[i][1][0]*brightness), 
                    int(RgbStrip.Flashing[i][1][1]*brightness), 
                    int(RgbStrip.Flashing[i][1][2]*brightness))
            self.pixels[pix] = (colr[0], colr[1], colr[2])

            if RgbStrip.Flashing[i][2] == RgbStrip.Flashing[i][3]:
                RgbStrip.Flashing[i][4] = -1
            if RgbStrip.Flashing[i][3] == 0 and RgbStrip.Flashing[i][4] == -1:
                pix = random.randint(0, self.num_pixels - 1)
                col = random.randint(0, len(RgbStrip.Colors) - 1)
                flash_len = random.randint(RgbStrip.Min_len, RgbStrip.Max_len)
                RgbStrip.Flashing[i] = [pix, RgbStrip.Colors[col], flash_len, 0, 1]
            RgbStrip.Flashing[i][3] = RgbStrip.Flashing[i][3] + RgbStrip.Flashing[i][4]
            time.sleep(0.005)
            self.pixels.show()


def main():
    rgb_strip = RgbRgbStrip(board.SPI())
    while True:
        rgb_strip.rainbow_cycle(0.01)


if __name__ == '__main__':
    main()
