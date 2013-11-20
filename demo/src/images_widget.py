# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>

tetris_widget.py: Widget for Tetris example

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

from PyQt4.QtGui import QWidget, QFileDialog
from PyQt4.QtCore import QDir
from ui_images import Ui_Images

from images import Images

class ImagesWidget(QWidget, Ui_Images):
    images = None
    thread = None
    
    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app
        
        self.setupUi(self)
        
        self.slider_speed.valueChanged.connect(self.slider_speed_changed)
        self.spinbox_speed.valueChanged.connect(self.spinbox_speed_changed)
        self.button_choose.pressed.connect(self.choose_pressed)
        self.button_show.pressed.connect(self.show_pressed)
         
    def show_pressed(self):
        if self.images.UID != None:
            new_images = unicode(self.text_edit_files.toPlainText()).split('\n')
            self.images.new_images(new_images)
            self.images.frame_prepare_next()
            self.images.frame_rendered(0)
         
    def choose_pressed(self):
        dialog = QFileDialog()
        dialog.setDirectory(QDir.homePath())
        dialog.setFileMode(QFileDialog.ExistingFiles)
        if dialog.exec_():
            filenames = dialog.selectedFiles()
            for filename in filenames:
                self.text_edit_files.append(filename)
         
    def default_values(self):
        self.slider_speed.setValue(1000)
         
    def spinbox_speed_changed(self, speed):
        self.slider_speed.setValue(speed)
         
    def slider_speed_changed(self, speed):
        self.spinbox_speed.setValue(speed)
        if self.images.UID != None:
            self.images.SPEED = speed 
            self.images.update_speed()

    def start(self):
        self.images = Images(self.app.ipcon)
        if self.images.UID != None:
            self.default_values()
            self.images.frame_rendered(0)
    
    def stop(self):
        if self.images.UID != None:
            self.images.stop_rendering()
