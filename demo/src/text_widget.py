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

from PyQt4.QtGui import QWidget, QColorDialog
from ui_text import Ui_Text

from text import ScrollingText

class TextWidget(QWidget, Ui_Text):
    text = None
    thread = None
    r = 255
    g = 0
    b = 0
    
    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app
        
        self.setupUi(self)
        
        self.slider_speed.valueChanged.connect(self.slider_speed_changed)
        self.edit_text.textChanged.connect(self.text_changed)
        self.button_pick.pressed.connect(self.pick_pressed)
        self.radio_rainbow.pressed.connect(self.rainbow_pressed)
        self.radio_color.pressed.connect(self.color_pressed)
        
        self.update_colors()
         
    def rainbow_pressed(self):
        self.text.COLOR = None
        
    def color_pressed(self):
        self.text.COLOR = (self.r, self.g, self.b)
         
    def pick_pressed(self):
        r, g, b, _ = QColorDialog.getColor().getRgbF()
        self.r, self.g, self.b = int(255*r), int(255*g), int(255*b)
        self.update_colors()
        self.radio_color.click()
        
    def update_colors(self):
        s = '(' + str(self.r) + ', ' + str(self.g) + ', ' + str(self.b) + ')'
        self.label_color.setText(s)
         
    def default_values(self):
        self.slider_speed.setValue(40)
        self.edit_text.setText('Starter Kit: Blinkenlights')
         
    def text_changed(self, text):
        self.text.new_text(str(text))
       
    def slider_speed_changed(self, speed):
        if self.text.UID != None:
            self.text.SPEED = speed 
            self.text.update_speed()

    def start(self):
        self.text = ScrollingText(self.app.ipcon)
        if self.text.UID != None:
            self.default_values()
            self.text.frame_rendered(0)

    def stop(self):
        if self.text.UID != None:
            self.text.stop_rendering()
