#!/usr/bin/env python
# -*- coding: utf-8 -*

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip

import colorsys
import math

import config

class Rainbow:
    leds = [x[:] for x in [(0, 0, 0)]*config.LED_ROWS*config.LED_COLS]
    rainbow = [x[:] for x in [(0, 0, 0)]*config.LED_ROWS*config.LED_COLS]
    rainbow_position = 0

    def __init__(self, ipcon):
        self.okay = False
        self.ipcon = ipcon

        if not config.UID_LED_STRIP_BRICKLET:
            print("Not Configured: LED Strip (required)")
            return

        self.led_strip = LEDStrip(config.UID_LED_STRIP_BRICKLET, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            print("Found: LED Strip ({0})").format(config.UID_LED_STRIP_BRICKLET)
        except:
            print("Not Found: LED Strip ({0})").format(config.UID_LED_STRIP_BRICKLET)
            return

        for i in range(config.LED_ROWS*config.LED_COLS):
            r, g, b = colorsys.hsv_to_rgb(1.0*i/(config.LED_ROWS*config.LED_COLS), 1, 0.1)
            self.rainbow[i] = (int(r*255), int(g*255), int(b*255))

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

        self.led_strip.set_frame_duration(1000.0 / config.RAINBOW_FRAME_RATE)

    def frame_rendered(self, _):
        self.frame_upload()
        self.frame_prepare_next()

    def frame_upload(self):
        if not self.okay:
            return

        r = []
        g = []
        b = []
        for i in range(config.LED_ROWS*config.LED_COLS):
            r.append(self.leds[i][config.R])
            g.append(self.leds[i][config.G])
            b.append(self.leds[i][config.B])

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
        self.leds = self.rainbow[int(self.rainbow_position) % (config.LED_ROWS*config.LED_COLS):] + self.rainbow[:int(self.rainbow_position) % (config.LED_ROWS*config.LED_COLS)]
        self.rainbow_position += (config.LED_ROWS*config.LED_COLS) * config.RAINBOW_SPEED / 4.0


if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    rainbow = Rainbow(ipcon)
    rainbow.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
