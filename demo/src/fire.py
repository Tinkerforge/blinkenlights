#!/usr/bin/env python
# -*- coding: utf-8 -*

# Loosely based on https://github.com/giladaya/arduino-led-matrix/blob/master/fire/fire.ino

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip

import colorsys
import random

import config

class Fire:
    values = [
        [ 32,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,  32],
        [ 64,  32,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,  32,  64],
        [ 96,  64,  32,  32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  32,  32,  64,  96],
        [128,  96,  64,  64,  32,  32,   0,   0,   0,   0,   0,   0,   0,   0,  32,  32,  64,  64,  96, 128],
        [160, 128,  96,  96,  64,  64,  32,  32,   0,   0,   0,   0,  32,  32,  64,  64,  96,  96, 128, 160],
        [192, 160, 128, 128,  96,  96,  64,  64,  32,   0,   0,  32,  64,  64,  96,  96, 128, 128, 160, 192],
        [255, 192, 160, 160, 128, 128,  96,  96,  64,  32,  32,  64,  96,  96, 128, 128, 160, 160, 192, 255],
        [255, 255, 192, 192, 160, 160, 128, 128,  96,  64,  64,  96, 128, 128, 160, 160, 192, 192, 255, 255],
        [255, 255, 255, 255, 192, 192, 160, 160, 128,  96,  96, 128, 160, 160, 192, 192, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 192, 192, 160, 128, 128, 160, 192, 192, 255, 255, 255, 255, 255, 255]
    ]

    hues = [
        [1, 3, 4, 5, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 6, 4, 3, 1],
        [1, 2, 3, 3, 5, 6, 7, 7, 8, 8, 8, 8, 9, 9, 8, 7, 5, 3, 2, 1],
        [1, 2, 3, 3, 5, 5, 6, 6, 5, 6, 6, 7, 7, 7, 6, 6, 4, 3, 2, 1],
        [1, 1, 2, 3, 4, 4, 5, 5, 4, 4, 5, 5, 6, 5, 5, 5, 3, 2, 1, 1],
        [1, 1, 2, 2, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4, 4, 2, 2, 1, 1],
        [0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0],
        [0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

#    values = [
#        [ 32,   0,   0,   0,   0,   0,   0,   0,   0,  32],
#        [ 64,   0,   0,   0,   0,   0,   0,   0,   0,  64],
#        [ 96,  32,   0,   0,   0,   0,   0,   0,  32,  96],
#        [128,  64,  32,   0,   0,   0,   0,  32,  64, 128],
#        [160,  96,  64,  32,   0,   0,  32,  64,  96, 160],
#        [192, 128,  96,  64,  32,  32,  64,  96, 128, 192],
#        [255, 160, 128,  96,  64,  64,  96, 128, 160, 255],
#        [255, 192, 160, 128,  96,  96, 128, 160, 192, 255],
#        [255, 255, 192, 160, 128, 128, 160, 192, 255, 255],
#        [255, 255, 255, 192, 160, 160, 192, 255, 255, 255]
#    ]

#    hues = [
#        [1, 4, 7, 9, 9, 9, 9, 8, 4, 1],
#        [1, 3, 5, 7, 8, 8, 9, 7, 3, 1],
#        [1, 3, 5, 6, 5, 6, 7, 6, 3, 1],
#        [1, 2, 4, 5, 4, 5, 5, 5, 2, 1],
#        [1, 2, 4, 4, 4, 5, 4, 4, 2, 1],
#        [0, 1, 2, 3, 3, 3, 3, 2, 1, 0],
#        [0, 0, 1, 2, 2, 2, 2, 1, 0, 0],
#        [0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#    ]

    line = [0]*config.LED_ROWS
    matrix = [x[:] for x in [[0]*config.LED_COLS]*config.LED_ROWS]
    leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]
    percent = 0

    def __init__(self, ipcon):
        self.okay = False
        self.ipcon = ipcon

        if not config.UID_LED_STRIP_BRICKLET:
            print('Not Configured: LED Strip (required)')
            return

        self.led_strip = LEDStrip(config.UID_LED_STRIP_BRICKLET, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            print('Found: LED Strip ({0})').format(config.UID_LED_STRIP_BRICKLET)
        except:
            print('Not Found: LED Strip ({0})').format(config.UID_LED_STRIP_BRICKLET)
            return

        self.okay = True

        self.update_frame_rate()
        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         self.frame_rendered)

    def stop_rendering(self):
        if not self.okay:
            return

        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         None)

    def update_frame_rate(self):
        if not self.okay:
            return

        self.led_strip.set_frame_duration(1000.0 / config.FIRE_FRAME_RATE)

    def frame_rendered(self, _):
        self.frame_upload()
        self.frame_prepare_next()

    def frame_upload(self):
        if not self.okay:
            return

        # Reorder LED data into R, G and B channel
        r = []
        g = []
        b = []
        for row in range(config.LED_ROWS):
            col_range = range(config.LED_COLS)
            if row % 2 == 0:
                col_range = reversed(col_range)
            for col in col_range:
                r.append(self.leds[row][col][config.R_INDEX])
                g.append(self.leds[row][col][config.G_INDEX])
                b.append(self.leds[row][col][config.B_INDEX])

        # Make chunks of size 16
        r_chunk = [r[i:i+16] for i in range(0, len(r), 16)]
        g_chunk = [g[i:i+16] for i in range(0, len(g), 16)]
        b_chunk = [b[i:i+16] for i in range(0, len(b), 16)]

        for i in range(len(r_chunk)):
            length = len(r_chunk[i])

            # Fill up chunks with zeros
            r_chunk[i].extend([0]*(16-len(r_chunk[i])))
            g_chunk[i].extend([0]*(16-len(g_chunk[i])))
            b_chunk[i].extend([0]*(16-len(b_chunk[i])))

            try:
                self.led_strip.set_rgb_values(i*16, length, r_chunk[i], g_chunk[i], b_chunk[i])
            except:
                break

    def frame_prepare_next(self):
        def shift_up():
            for y in reversed(range(1, config.LED_COLS)):
                for x in range(config.LED_ROWS):
                    self.matrix[x][y] = self.matrix[x][y-1]

            for x in range(config.LED_ROWS):
                self.matrix[x][0] = self.line[x]

        def generate_line():
            for x in range(config.LED_ROWS):
                self.line[x] = random.randint(min(config.FIRE_RAND_VALUE_START, config.FIRE_RAND_VALUE_END), config.FIRE_RAND_VALUE_END)

        def make_frame():
            def hsv_to_rgb(h, s, v):
                r, g, b = colorsys.hsv_to_rgb(h/255.0, s/255.0, v/255.0)
                return ((int(255*r), int(255*g), int(255*b)))

            for y in reversed(range(1, config.LED_COLS)):
                for x in range(config.LED_ROWS):
                    self.leds[x][config.LED_COLS-1-y] = hsv_to_rgb(self.hues[y][x]*config.FIRE_HUE_FACTOR,
                                                                   255,
                                                                   max(0, (((100.0-self.percent)*self.matrix[x][y] + self.percent*self.matrix[x][y-1])/100.0) - self.values[y][x]))

            for x in range(config.LED_ROWS):
                self.leds[x][config.LED_COLS-1] = hsv_to_rgb(self.hues[0][x]*config.FIRE_HUE_FACTOR,
                                                             255,
                                                             max(0, ((100.0-self.percent)*self.matrix[x][0] + self.percent*self.line[x])/100.0))

        self.percent += 20
        if self.percent >= 100:
            shift_up()
            generate_line()
            self.percent = 0

        make_frame()


if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    fire = Fire(ipcon)
    fire.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
