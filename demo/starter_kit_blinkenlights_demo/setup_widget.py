# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

setup_widget.py: Widget for Blinkenlights setup

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

from starter_kit_blinkenlights_demo.ui_setup import Ui_Setup


class SetupWidget(QWidget, Ui_Setup):
    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.button_reconnect.pressed.connect(self.app.connect)

    def button_press(self, button):
        pass

    def start(self):
        pass

    def stop(self):
        pass
