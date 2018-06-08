#!/usr/bin/env python
# -*- coding: utf-8 -*

# Loosely based on https://github.com/giladaya/arduino-led-matrix/blob/master/fire/fire.ino

import colorsys
import random

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_led_strip_v2 import LEDStripV2

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
            print("Not Configured: LED Strip or LED Strip V2 (required)")
            return

        if not config.IS_LED_STRIP_V2:
            self.led_strip = LEDStrip(config.UID_LED_STRIP_BRICKLET, self.ipcon)
        else:
            self.led_strip = LEDStripV2(config.UID_LED_STRIP_BRICKLET, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            if not config.IS_LED_STRIP_V2:
                print("Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
            else:
                print("Found: LED Strip V2 ({0})".format(config.UID_LED_STRIP_BRICKLET))
        except:
            if not config.IS_LED_STRIP_V2:
                print("Not Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
            else:
                print("Not Found: LED Strip V2({0})".format(config.UID_LED_STRIP_BRICKLET))
            return

        self.okay = True

        self.update_frame_rate()
        if not config.IS_LED_STRIP_V2:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                             self.frame_rendered)
        else:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_STARTED,
                                             self.frame_rendered)

        self.led_strip.set_channel_mapping(config.CHANNEL_MAPPING)
    def stop_rendering(self):
        if not self.okay:
            return

        if not config.IS_LED_STRIP_V2:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                             None)
        else:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_STARTED,
                                             None)

    def update_frame_rate(self):
        if not self.okay:
            return

        self.led_strip.set_frame_duration(int(1000.0 / config.FIRE_FRAME_RATE))

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
        frame = []

        for row in range(config.LED_ROWS):
            col_range = range(config.LED_COLS)
            if row % 2 == 0:
                col_range = reversed(col_range)
            for col in col_range:
                r.append(self.leds[row][col][0])
                g.append(self.leds[row][col][1])
                b.append(self.leds[row][col][2])
                frame.append(self.leds[row][col][0])
                frame.append(self.leds[row][col][1])
                frame.append(self.leds[row][col][2])

        if not config.IS_LED_STRIP_V2:
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
        else:
            try:
                self.led_strip.set_led_values(0, frame)
            except:
                return

    def frame_prepare_next(self):
        def shift_up():
            for y in reversed(range(1, config.LED_COLS)):
                for x in range(config.LED_ROWS):
                    self.matrix[x][y] = self.matrix[x][y-1]

            for x in range(config.LED_ROWS):
                self.matrix[x][0] = self.line[x]

        def generate_line():
            start = min(config.FIRE_RAND_VALUE_START, config.FIRE_RAND_VALUE_END)
            end = config.FIRE_RAND_VALUE_END

            for x in range(config.LED_ROWS):
                self.line[x] = random.randint(start, end)

        def make_frame():
            def hsv_to_rgb(h, s, v):
                r, g, b = colorsys.hsv_to_rgb(h/255.0, s/255.0, v/255.0)
                return ((int(255*r), int(255*g), int(255*b)))

            def interpolate2(x, y):
                p0 = 100.0 - self.percent
                p1 = self.percent
                m0 = self.matrix[x][y]
                m1 = self.matrix[x][y-1]

                return (p0*m0 + p1*m1) / 100.0

            def interpolate1(x):
                p0 = 100.0 - self.percent
                p1 = self.percent
                m0 = self.matrix[x][0]
                m1 = self.line[x]

                return (p0*m0 + p1*m1) / 100.0

            for y in reversed(range(1, config.LED_COLS)):
                for x in range(config.LED_ROWS):
                    rgb = hsv_to_rgb(self.hues[y][x]*config.FIRE_HUE_FACTOR, 255,
                                     max(0, interpolate2(x, y) - self.values[y][x]))
                    self.leds[x][config.LED_COLS-1-y] = rgb

            for x in range(config.LED_ROWS):
                rgb = hsv_to_rgb(self.hues[0][x]*config.FIRE_HUE_FACTOR, 255,
                                 max(0, interpolate1(x)))
                self.leds[x][config.LED_COLS-1] = rgb

        self.percent += 20
        if self.percent >= 100:
            shift_up()
            generate_line()
            self.percent = 0

        make_frame()


if __name__ == "__main__":
    # Create IP Connection and connect it
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    # Create Fire object and start rendering
    fire = Fire(ipcon)
    fire.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
