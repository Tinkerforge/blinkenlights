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

from PyQt4.QtGui import QWidget
from ui_fire import Ui_Fire

from fire import Fire

class FireWidget(QWidget, Ui_Fire):
    fire = None
    thread = None
    
    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app
        
        self.setupUi(self)
        
        self.spinbox_speed.valueChanged.connect(self.spinbox_speed_changed)
        self.spinbox_hue.valueChanged.connect(self.spinbox_hue_changed)
        self.spinbox_start.valueChanged.connect(self.spinbox_start_changed)
        self.spinbox_end.valueChanged.connect(self.spinbox_end_changed)
        
        self.slider_speed.valueChanged.connect(self.slider_speed_changed)
        self.slider_hue.valueChanged.connect(self.slider_hue_changed)
        self.slider_start.valueChanged.connect(self.slider_start_changed)
        self.slider_end.valueChanged.connect(self.slider_end_changed)
        
        self.button_default.pressed.connect(self.default_pressed)
         
    def default_pressed(self):
        self.spinbox_speed.setValue(20)
        self.spinbox_hue.setValue(1.2)
        self.spinbox_start.setValue(64)
        self.spinbox_end.setValue(255)
        
    def spinbox_speed_changed(self, speed):
        self.slider_speed.setValue(speed)
        
    def spinbox_hue_changed(self, hue):
        self.slider_hue.setValue(int(hue*10))
        
    def spinbox_start_changed(self, start):
        self.slider_start.setValue(start)
        
    def spinbox_end_changed(self, end):
        self.slider_end.setValue(end)
        
    def slider_speed_changed(self, speed):
        self.spinbox_speed.setValue(speed)
        if self.fire.UID != None:
            self.fire.SPEED = speed 
            self.fire.update_speed()
        
    def slider_hue_changed(self, hue):
        self.spinbox_hue.setValue(hue/10.0)
        if self.fire.UID != None:
            self.fire.HUE_FACTOR = hue/10.0 
        
    def slider_start_changed(self, start):
        self.spinbox_start.setValue(start)
        if self.fire.UID != None:
            self.fire.RAND_VALUE_START = start
        
    def slider_end_changed(self, end):
        self.spinbox_end.setValue(end)
        if self.fire.UID != None:
            self.fire.RAND_VALUE_END = end
                    
    def button_press(self, button):
        if self.fire != None:
            self.fire.kp.key_queue.put(button)

    def start(self):
        self.fire = Fire(self.app.ipcon)
        self.default_pressed()
        self.fire.frame_rendered(0)

    
    def stop(self):
        if self.fire != None:
            self.fire.stop_rendering()