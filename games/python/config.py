# -*- coding: utf-8 -*-

from tinkerforge.bricklet_led_strip import LEDStrip

HAS_GUI = False

# General
HOST = 'localhost'
PORT = 4223

# Required Bricklets
UID_LED_STRIP_BRICKLET = 'Fjy'

# Optional Bricklets (use None as UID if not connected)
UID_MULTI_TOUCH_BRICKLET = None#'pax'
UID_DUAL_BUTTON_BRICKLET = (None, None)#('dbb', 'dbc')
UID_SEGMENT_DISPLAY_4X7_BRICKLET = None#'xyz'
UID_PIEZO_SPEAKER_BRICKLET = None#'XYZ'

# Set this to True if LEDStripV2 Bricklet is used
IS_LED_STRIP_V2 = True

# Size of LED Pixel matrix
LED_ROWS = 20
LED_COLS = 10

# Position of R, G and B pixel on LED Pixel
CHANNEL_MAPPING = LEDStrip.CHANNEL_MAPPING_RGB

# Pong Parameters
PONG_COLOR_INDEX_PLAYER = (1, 5)
PONG_COLOR_INDEX_BALL = 4

# Keymaps
KEYMAP_MULTI_TOUCH = {
    0: 'a',
    1: 's',
    2: 'd',
    3: 'k',
    4: 'l',
    5: 'q'
}

KEYMAP_DUAL_BUTTON = {
    0: 'a',
    1: 's',
    2: 'k',
    3: 'l'
}
