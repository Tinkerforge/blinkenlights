# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2013-2014 Matthias Bolte <matthias@tinkerforge.com>

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
from ui_tetris import Ui_Tetris

from tetris import Tetris

import config

from threading import Thread

class TetrisWidget(QWidget, Ui_Tetris):
    tetris = None
    thread = None

    def __init__(self, parent, app):
        super(QWidget, self).__init__()
        self.app = app

        self.setupUi(self)

        self.button_a.pressed.connect(lambda: self.button_press('a'))
        self.button_s.pressed.connect(lambda: self.button_press('s'))
        self.button_d.pressed.connect(lambda: self.button_press('d'))
        self.button_k.pressed.connect(lambda: self.button_press('k'))
        self.button_l.pressed.connect(lambda: self.button_press('l'))
        self.button_r.pressed.connect(lambda: self.button_press('r'))

    def start_tetris(self):
        self.tetris = Tetris(self.app.ipcon)

        if self.tetris.okay:
            self.tetris.run_game_loop()

        self.tetris = None

    def button_press(self, button):
        if self.tetris:
            self.tetris.kp.key_queue.put(button)

    def start(self):
        self.thread = Thread(target=self.start_tetris)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.tetris:
            self.tetris.loop = False
            self.tetris.kp.key_queue.put('q')
