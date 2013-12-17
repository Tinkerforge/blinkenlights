# -*- coding: utf-8 -*-

# General
HOST = 'localhost'
PORT = 4223

# Bricklet
UID_LED_STRIP_BRICKLET = 'abc' # Change to your UID

# Size of LED Pixel matrix
LED_ROWS = 20
LED_COLS = 10

# Position of R, G and B pixel on LED Pixel
R_INDEX = 2
G_INDEX = 1
B_INDEX = 0

# Fire Parameters
FIRE_FRAME_RATE = 50 # in Hz, valid range: 10 - 100
FIRE_HUE_FACTOR = 1.2 # valid range: 0.1 - 5.0
FIRE_RAND_VALUE_START = 64 # valid range: 0 - 255
FIRE_RAND_VALUE_END = 255 # valid range: 1 - 255
