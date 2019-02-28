# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013, 2015 Matthias Bolte <matthias@tinkerforge.com>

text_widget.py: Widget for text example

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer

import starter_kit_blinkenlights_demo.config as config
from starter_kit_blinkenlights_demo.ui_text import Ui_Text
from starter_kit_blinkenlights_demo.text import Text


class TextWidget(QWidget, Ui_Text):
    text = None
    r = 255
    g = 0
    b = 0
    color_mode = 'rainbow'

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.slider_frame_rate.valueChanged.connect(self.slider_frame_rate_changed)
        self.spinbox_frame_rate.valueChanged.connect(self.spinbox_frame_rate_changed)
        self.radio_rainbow.pressed.connect(self.rainbow_pressed)
        self.radio_color.pressed.connect(self.color_pressed)
        self.button_pick.pressed.connect(self.pick_pressed)
        self.edit_text.textChanged.connect(self.text_changed)
        self.button_default.pressed.connect(self.default_pressed)

        self.update_frame_rate_timer = QTimer(self)
        self.update_frame_rate_timer.timeout.connect(self.update_frame_rate)

        self.default_pressed()

    def start(self):
        self.text = Text(self.app.ipcon)

        self.update_frame_rate()
        self.update_color()

        self.text.frame_rendered(0)

    def stop(self):
        if self.text:
            self.text.stop_rendering()
            self.text = None

    def slider_frame_rate_changed(self, frame_rate):
        self.spinbox_frame_rate.setValue(frame_rate)

    def spinbox_frame_rate_changed(self, frame_rate):
        self.slider_frame_rate.setValue(frame_rate)
        self.update_frame_rate_timer.start(100)

    def rainbow_pressed(self):
        self.color_mode = 'rainbow'
        self.update_color()

    def color_pressed(self):
        self.color_mode = 'single'
        self.update_color()

    def pick_pressed(self):
        r, g, b, _ = QColorDialog.getColor(QColor(self.r, self.g, self.b)).getRgbF()
        self.r, self.g, self.b = int(255*r), int(255*g), int(255*b)
        self.update_color()
        self.radio_color.click()

    def text_changed(self, text):
        self.text.set_new_text(str(text))

    def default_pressed(self):
        self.r, self.g, self.b = (255, 0, 0)

        self.spinbox_frame_rate.setValue(25)
        self.radio_rainbow.click()
        self.edit_text.setText('Starter Kit: Blinkenlights')

    def update_frame_rate(self):
        self.update_frame_rate_timer.stop()

        config.TEXT_FRAME_RATE = self.spinbox_frame_rate.value()

        if self.text:
            self.text.update_frame_rate()

    def update_color(self):
        s = '(' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ')'
        self.label_color.setText(s)

        if self.color_mode == 'rainbow':
            config.TEXT_COLOR = None
        else:
            config.TEXT_COLOR = (self.r, self.g, self.b)
