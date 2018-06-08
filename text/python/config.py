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

# Text Parameters
TEXT_FRAME_RATE = 25 # in Hz, valid range: 10 - 100
TEXT_COLOR = None # = rainbow
#TEXT_COLOR = (255, 0, 0) # = red
TEXT_TOP_OFFSET = 1
