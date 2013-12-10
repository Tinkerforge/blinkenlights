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
        image = None
        def __init__(self, f):
            self.image = Image.open(f).convert('RGB')
            size = self.get_size()
            if size != (20, 10):
                self.image = self.image.resize((20, 10), Image.ANTIALIAS)

        def get_size(self):
            if self.image == None:
                return (0, 0)

            return self.image.size

        def get_pixel(self, x, y):
            if self.image == None:
                return (0, 0, 0)

            return self.image.getpixel((x, y))
except:
    pil_available = False

    from PyQt4.QtGui import QImage, QColor
    class ImageLoaderQt:
        image = None
        def __init__(self, f):
            self.image = QImage(f)
            if self.get_size() != (20, 10):
                self.image = self.image.scaled(20, 10)

        def get_size(self):
            size = self.image.size()
            return (size.width(), size.height())

        def get_pixel(self, x, y):
            r, g, b, _ = QColor(self.image.pixel(x, y)).getRgbF()
            r, g, b = int(255*r), int(255*g), int(255*b)
            return r, g, b


if pil_available:
    ImageLoader = ImageLoaderPIL
else:
    ImageLoader = ImageLoaderQt

class Images:
    colors = [
        (10,  10,  10),  # grey
        (255, 0,   0),   # red
        (255, 80,  0),   # orange
        (255, 255, 0),   # yellow
        (0,   255, 0),   # green
        (0,   0,   255), # blue
        (255, 0,   150), # violet
        (255, 0,   40),  # purple
    ]

    leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]
    files = []
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

        self.led_strip.set_frame_duration(1000.0 / config.IMAGES_FRAME_RATE)

    def new_images(self, image_urls):
        self.files = []
        for url in image_urls:
            self.files.append(ImageLoader(url))
        self.image_position = 0

    def frame_rendered(self, _):
        self.frame_upload()
        self.frame_prepare_next()

    def frame_upload(self):
        if not self.okay:
            return

        r = []
        g = []
        b = []
        for col in range(config.LED_ROWS):
            row_range = range(config.LED_COLS)
            if col % 2 == 0:
                row_range = reversed(row_range)
            for row in row_range:
                r.append(self.leds[col][row][config.R])
                g.append(self.leds[col][row][config.G])
                b.append(self.leds[col][row][config.B])

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
        if len(self.files) == 0:
            return

        h, w = self.files[self.image_position].get_size()

        self.leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]
        for x in range(min(config.LED_COLS, w)):
            for y in range(min(config.LED_ROWS, h)):
                self.leds[y][x] = self.files[self.image_position].get_pixel(y, x)

        self.image_position = (self.image_position + 1) % len(self.files)


if __name__ == "__main__":
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    images = Images(ipcon)

    images.new_images(sys.argv[1:])
    images.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
