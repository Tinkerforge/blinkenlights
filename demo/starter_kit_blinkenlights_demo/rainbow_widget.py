# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013, 2015 Matthias Bolte <matthias@tinkerforge.com>

rainbow_widget.py: Widget for rainbow example

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

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

import starter_kit_blinkenlights_demo.config as config
from starter_kit_blinkenlights_demo.ui_rainbow import Ui_Rainbow
from starter_kit_blinkenlights_demo.rainbow import Rainbow


class RainbowWidget(QWidget, Ui_Rainbow):
    rainbow = None

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.slider_frame_rate.valueChanged.connect(self.slider_frame_rate_changed)
        self.slider_step.valueChanged.connect(self.slider_step_changed)

        self.spinbox_frame_rate.valueChanged.connect(self.spinbox_frame_rate_changed)
        self.spinbox_step.valueChanged.connect(self.spinbox_step_changed)

        self.button_default.pressed.connect(self.default_pressed)

        self.update_frame_rate_timer = QTimer(self)
        self.update_frame_rate_timer.timeout.connect(self.update_frame_rate)

        self.default_pressed()

    def start(self):
        self.rainbow = Rainbow(self.app.ipcon)

        self.update_frame_rate()
        self.update_step()

        self.rainbow.frame_rendered(0)

    def stop(self):
        if self.rainbow:
            self.rainbow.stop_rendering()
            self.rainbow = None

    def spinbox_frame_rate_changed(self, frame_rate):
        self.slider_frame_rate.setValue(frame_rate)
        self.update_frame_rate_timer.start(100)

    def spinbox_step_changed(self, step):
        self.slider_step.setValue(step * 10)
        self.update_step()

    def slider_frame_rate_changed(self, frame_rate):
        self.spinbox_frame_rate.setValue(frame_rate)

    def slider_step_changed(self, step):
        self.spinbox_step.setValue(step / 10.0)

    def default_pressed(self):
        self.spinbox_frame_rate.setValue(50)
        self.spinbox_step.setValue(0.2)

    def update_frame_rate(self):
        self.update_frame_rate_timer.stop()

        config.RAINBOW_FRAME_RATE = self.spinbox_frame_rate.value()

        if self.rainbow:
            self.rainbow.update_frame_rate()

    def update_step(self):
        config.RAINBOW_STEP = self.spinbox_step.value() / 100.0
