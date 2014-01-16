# -*- coding: utf-8 -*-

DEMO_VERSION = '1.0.0'

# Bricklets
UID_LED_STRIP_BRICKLET = None
UID_MULTI_TOUCH_BRICKLET = None
UID_DUAL_BUTTON_BRICKLET = (None, None)
UID_SEGMENT_DISPLAY_4X7_BRICKLET = None
UID_PIEZO_SPEAKER_BRICKLET = None

# Size of LED Pixel matrix
LED_ROWS = 20
LED_COLS = 10

# Position of R, G and B pixel on LED Pixel
R_INDEX = 2
G_INDEX = 1
B_INDEX = 0

# Pong Parameters
PONG_COLOR_INDEX_PLAYER = (1, 5)
PONG_COLOR_INDEX_BALL = 4

# Keymaps for Tetris and Pong
KEYMAP_MULTI_TOUCH = {
    0: 'a',
    1: 's',
    2: 'd',
    3: 'k',
    4: 'l',
    5: 'r',
    6: 'q'
}

KEYMAP_DUAL_BUTTON = {
    0: 'a',
    1: 's',
    2: 'k',
    3: 'l'
}

# Fire Parameters
FIRE_FRAME_RATE = 50 # in Hz, valid range: 10 - 100
FIRE_HUE_FACTOR = 1.2 # valid range: 0.1 - 5.0
FIRE_RAND_VALUE_START = 64 # valid range: 0 - 255
FIRE_RAND_VALUE_END = 255 # valid range: 1 - 255

# Text Parameters
TEXT_FRAME_RATE = 25 # in Hz, valid range: 10 - 100
TEXT_COLOR = None # = rainbow
#TEXT_COLOR = (255, 0, 0) # = red

# Images Parameters
IMAGES_FRAME_RATE = 1 # in Hz, valid range: 1 - 100

# Rainbow Parameters
RAINBOW_FRAME_RATE = 50 # in Hz, valid range: 10 - 100
RAINBOW_STEP = 0.002 # valid range: 0.0 - 1.0
