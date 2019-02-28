# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013, 2015 Matthias Bolte <matthias@tinkerforge.com>

images_widget.py: Widget for images example

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

from PyQt5.QtWidgets import QWidget, QFileDialog, QErrorMessage
from PyQt5.QtCore import QDir, QTimer

import starter_kit_blinkenlights_demo.config as config
from starter_kit_blinkenlights_demo.ui_images import Ui_Images
from starter_kit_blinkenlights_demo.images import Images


class ImagesWidget(QWidget, Ui_Images):
    images = None

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowTitle("Starter Kit: Blinkenlights Demo " + config.DEMO_VERSION)

        self.slider_frame_rate.valueChanged.connect(self.slider_frame_rate_changed)
        self.spinbox_frame_rate.valueChanged.connect(self.spinbox_frame_rate_changed)
        self.button_choose.pressed.connect(self.choose_pressed)
        self.button_show.pressed.connect(self.show_pressed)
        self.button_default.pressed.connect(self.default_pressed)

        self.update_frame_rate_timer = QTimer(self)
        self.update_frame_rate_timer.timeout.connect(self.update_frame_rate)

        self.default_pressed()

    def start(self):
        self.images = Images(self.app.ipcon)

        self.update_frame_rate()

        self.images.frame_rendered(0)

    def stop(self):
        if self.images:
            self.images.stop_rendering()
            self.images = None

    def spinbox_frame_rate_changed(self, frame_rate):
        self.slider_frame_rate.setValue(frame_rate)
        self.update_frame_rate_timer.start(100)

    def slider_frame_rate_changed(self, frame_rate):
        self.spinbox_frame_rate.setValue(frame_rate)

    def show_pressed(self):
        if self.images:
            files = self.text_edit_files.toPlainText().strip()

            if len(files) > 0:
                new_images = files.split('\n')

                try:
                    self.images.set_new_images(new_images)
                except Exception as e:
                    self.error_msg.showMessage(str(e))

                self.images.frame_prepare_next()
                self.images.frame_rendered(0)

    def choose_pressed(self):
        names, selected_filter = QFileDialog.getOpenFileNames(self, 'Choose Images', QDir.homePath())
        for filename in names:
            self.text_edit_files.append(filename)

    def default_pressed(self):
        self.spinbox_frame_rate.setValue(1)

    def update_frame_rate(self):
        self.update_frame_rate_timer.stop()

        config.IMAGES_FRAME_RATE = self.spinbox_frame_rate.value()

        if self.images:
            self.images.update_frame_rate()
