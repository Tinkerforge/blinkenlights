#!/usr/bin/env python
# -*- coding: utf-8 -*

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip

import sys

import config

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
