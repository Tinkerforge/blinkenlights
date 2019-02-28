# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013, 2015 Matthias Bolte <matthias@tinkerforge.com>

fire_widget.py: Widget for fire example

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
from starter_kit_blinkenlights_demo.ui_fire import Ui_Fire
from starter_kit_blinkenlights_demo.fire import Fire


class FireWidget(QWidget, Ui_Fire):
    fire = None

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.slider_frame_rate.valueChanged.connect(self.slider_frame_rate_changed)
        self.slider_hue.valueChanged.connect(self.slider_hue_changed)
        self.slider_start.valueChanged.connect(self.slider_start_changed)
        self.slider_end.valueChanged.connect(self.slider_end_changed)

        self.spinbox_frame_rate.valueChanged.connect(self.spinbox_frame_rate_changed)
        self.spinbox_hue.valueChanged.connect(self.spinbox_hue_changed)
        self.spinbox_start.valueChanged.connect(self.spinbox_start_changed)
        self.spinbox_end.valueChanged.connect(self.spinbox_end_changed)

        self.button_default.pressed.connect(self.default_pressed)

        self.update_frame_rate_timer = QTimer(self)
        self.update_frame_rate_timer.timeout.connect(self.update_frame_rate)

        self.default_pressed()

    def start(self):
        self.fire = Fire(self.app.ipcon)

        self.update_frame_rate()
        self.update_hue()
        self.update_start()
        self.update_end()

        self.fire.frame_rendered(0)

    def stop(self):
        if self.fire:
            self.fire.stop_rendering()
            self.fire = None

    def spinbox_frame_rate_changed(self, frame_rate):
        self.slider_frame_rate.setValue(frame_rate)
        self.update_frame_rate_timer.start(100)

    def spinbox_hue_changed(self, hue):
        self.slider_hue.setValue(int(hue*10))
        self.update_hue()

    def spinbox_start_changed(self, start):
        self.slider_start.setValue(start)
        self.update_start()

    def spinbox_end_changed(self, end):
        self.slider_end.setValue(end)
        self.update_end()

    def slider_frame_rate_changed(self, frame_rate):
        self.spinbox_frame_rate.setValue(frame_rate)

    def slider_hue_changed(self, hue):
        self.spinbox_hue.setValue(hue/10.0)

    def slider_start_changed(self, start):
        self.spinbox_start.setValue(start)

    def slider_end_changed(self, end):
        self.spinbox_end.setValue(end)

    def default_pressed(self):
        self.spinbox_frame_rate.setValue(50)
        self.spinbox_hue.setValue(1.2)
        self.spinbox_start.setValue(64)
        self.spinbox_end.setValue(255)

    def update_frame_rate(self):
        self.update_frame_rate_timer.stop()

        config.FIRE_FRAME_RATE = self.spinbox_frame_rate.value()

        if self.fire:
            self.fire.update_frame_rate()

    def update_hue(self):
        config.FIRE_HUE_FACTOR = self.spinbox_hue.value()

    def update_start(self):
        config.FIRE_RAND_VALUE_START = self.spinbox_start.value()

    def update_end(self):
        config.FIRE_RAND_VALUE_END = self.spinbox_end.value()
