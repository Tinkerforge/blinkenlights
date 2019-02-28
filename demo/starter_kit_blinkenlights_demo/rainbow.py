#!/usr/bin/env python
# -*- coding: utf-8 -*

import colorsys
import math

from starter_kit_blinkenlights_demo.tinkerforge.ip_connection import IPConnection
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip import LEDStrip
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip_v2 import LEDStripV2

import starter_kit_blinkenlights_demo.config as config

class Rainbow:
    leds = [x[:] for x in [(0, 0, 0)]*config.LED_ROWS*config.LED_COLS]
    rainbow = [x[:] for x in [(0, 0, 0)]*config.LED_ROWS*config.LED_COLS]
    rainbow_position = 0

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

        for i in range(config.LED_ROWS*config.LED_COLS):
            r, g, b = colorsys.hsv_to_rgb(1.0*i/(config.LED_ROWS*config.LED_COLS), 1, 0.1)
            self.rainbow[i] = (int(r*255), int(g*255), int(b*255))

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

        self.led_strip.set_frame_duration(int(1000.0 / config.RAINBOW_FRAME_RATE))

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

        for i in range(config.LED_ROWS*config.LED_COLS):
            r.append(self.leds[i][0])
            g.append(self.leds[i][1])
            b.append(self.leds[i][2])
            frame.append(self.leds[i][0])
            frame.append(self.leds[i][1])
            frame.append(self.leds[i][2])

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
        self.leds = self.rainbow[int(self.rainbow_position) % (config.LED_ROWS*config.LED_COLS):] + self.rainbow[:int(self.rainbow_position) % (config.LED_ROWS*config.LED_COLS)]
        self.rainbow_position += (config.LED_ROWS*config.LED_COLS) * config.RAINBOW_STEP


if __name__ == "__main__":
    # Create IP Connection and connect it
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    # Create Rainbow object and start rendering
    rainbow = Rainbow(ipcon)
    rainbow.frame_rendered(0)

    input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
