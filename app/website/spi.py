#!/usr/bin/env python3

import time
import board
import neopixel_spi as neopixel
import sys


class RgbStrip:
    def __init__(self, spi):
        self.num_pixels = 60
        self.pixel_order = neopixel.GRB
        self.delay = 1

        # spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(
            spi, self.num_pixels, brightness=1.0, auto_write=False, pixel_order=self.pixel_order, bit0=0b10000000
        )

    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
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


def main():
    rgb_strip = RgbStrip(board.SPI())
    while True:
        rgb_strip.rainbow_cycle(0.01)


if __name__ == '__main__':
    main()
