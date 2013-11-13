# -*- coding: utf-8 -*

# General Settings
HOST = 'localhost'
PORT = 4223

# Optional Bricklets (use None as UID if not connected)
UID_MULTI_TOUCH_BRICKLET = 'pax'
UID_DUAL_BUTTON_BRICKLET = ('dbb', 'dbc')
UID_SEGMENT_DISPLAY_4X7_BRICKLET = 'xyz'
UID_PIEZO_SPEAKER_BRICKLET = 'XYZ'

# Required Bricklets
UID_LED_STRIP_BRICKLET = 'abc'

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