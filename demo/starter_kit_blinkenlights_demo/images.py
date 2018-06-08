#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys

from starter_kit_blinkenlights_demo.tinkerforge.ip_connection import IPConnection
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip import LEDStrip
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip_v2 import LEDStripV2

import starter_kit_blinkenlights_demo.config as config

pil_available = True
try:
    from PIL import Image
    class ImageLoaderPIL:
        def __init__(self, f):
            self.image = Image.open(f).convert('RGB')

            if self.image.size != (config.LED_ROWS, config.LED_COLS):
                self.image = self.image.resize((config.LED_ROWS, config.LED_COLS), Image.ANTIALIAS)

        def get_pixel(self, x, y):
            return self.image.getpixel((x, y))
except:
    pil_available = False

    from PyQt4.QtGui import QImage, QColor
    class ImageLoaderQt:
        def __init__(self, f):
            self.image = QImage(f)

            width = self.image.size().width()
            height = self.image.size().height()

            if width != config.LED_ROWS or height != config.LED_COLS:
                self.image = self.image.scaled(config.LED_ROWS, config.LED_COLS)

        def get_pixel(self, x, y):
            r, g, b, _ = QColor(self.image.pixel(x, y)).getRgbF()
            return int(255*r), int(255*g), int(255*b)

if pil_available:
    print('Using PIL for image handling')
    ImageLoader = ImageLoaderPIL
else:
    print('Using Qt for image handling')
    ImageLoader = ImageLoaderQt


class Images:
    leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]
    images = []
    image_position = 0

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

        self.led_strip.set_frame_duration(int(1000.0 / config.IMAGES_FRAME_RATE))

    def set_new_images(self, image_urls):
        self.images = []

        for url in image_urls:
            loader = ImageLoader(url)
            image = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]

            for y in range(config.LED_ROWS):
                for x in range(config.LED_COLS):
                    image[y][x] = loader.get_pixel(y, x)

            self.images.append(image)

        self.image_position = 0

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
        if len(self.images) == 0:
            return

        self.leds = self.images[self.image_position]
        self.image_position = (self.image_position + 1) % len(self.images)


if __name__ == "__main__":
    # Create IP Connection and connect it
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    # Create Images object and start rendering
    images = Images(ipcon)

    images.set_new_images(sys.argv[1:])
    images.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
