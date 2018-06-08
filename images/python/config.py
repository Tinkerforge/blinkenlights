# -*- coding: utf-8 -*-

from tinkerforge.bricklet_led_strip import LEDStrip

# General
HOST = 'localhost'
PORT = 4223

# Bricklet
UID_LED_STRIP_BRICKLET = 'Fjy'

# Set this to True if LEDStripV2 Bricklet is used
IS_LED_STRIP_V2 = True

# Size of LED Pixel matrix
LED_ROWS = 20
LED_COLS = 10

# Position of R, G and B pixel on LED Pixel
CHANNEL_MAPPING = LEDStrip.CHANNEL_MAPPING_RGB

# Images Parameters
IMAGES_FRAME_RATE = 1 # in Hz, valid range: 1 - 100
