# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013 Matthias Bolte <matthias@tinkerforge.com>

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

from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QTimer
from ui_rainbow import Ui_Rainbow

from rainbow import Rainbow

class RainbowWidget(QWidget, Ui_Rainbow):
    rainbow = None

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.slider_speed.valueChanged.connect(self.slider_speed_changed)
        self.slider_movement.valueChanged.connect(self.slider_movement_changed)

        self.speed_timer = QTimer(self)
        self.speed_timer.timeout.connect(self.apply_speed)

    def slider_speed_changed(self, speed):
        self.speed_timer.start(100)

    def apply_speed(self):
        self.speed_timer.stop()
        self.rainbow.SPEED = self.slider_speed.value()
        self.rainbow.update_speed()

    def slider_movement_changed(self, value):
        self.rainbow.MOVEMENT = value

    def start(self):
        self.rainbow = Rainbow(self.app.ipcon)
        self.rainbow.frame_rendered(0)

    def stop(self):
        self.rainbow.stop_rendering()
        self.rainbow = None
