#!/usr/bin/env python

import os

os.system("pyuic4 -o ui_setup.py ui/setup.ui")
os.system("pyuic4 -o ui_tetris.py ui/tetris.ui")
os.system("pyuic4 -o ui_pong.py ui/pong.ui")
os.system("pyuic4 -o ui_fire.py ui/fire.ui")
os.system("pyuic4 -o ui_text.py ui/text.ui")
os.system("pyuic4 -o ui_images.py ui/images.ui")
