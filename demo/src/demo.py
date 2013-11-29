#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>

demo.py: Entry file for Demo

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

import socket
import sys
import time
import math
import signal
import os


from program_path import ProgramPath
import config

from tinkerforge.ip_connection import IPConnection
from tinkerforge.ip_connection import Error
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
from tinkerforge.bricklet_segment_display_4x7 import SegmentDisplay4x7
from tinkerforge.bricklet_multi_touch import MultiTouch
from tinkerforge.bricklet_dual_button import DualButton

from setup_widget import SetupWidget
from tetris_widget import TetrisWidget
from pong_widget import PongWidget
from fire_widget import FireWidget
from text_widget import TextWidget
from images_widget import ImagesWidget
from rainbow_widget import RainbowWidget

from PyQt4.QtGui import QApplication, QWidget, QErrorMessage, QGridLayout, QIcon
from PyQt4.QtGui import QPalette, QTextFormat, QTabWidget, QMainWindow, QVBoxLayout
from PyQt4.QtCore import QTimer, pyqtSignal

class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.app = app
        
    def keyPressEvent(self, event):
        try:
            button = event.text().toAscii()[0]
            # Don't allow quit trigger of games by user input
            if button != 'q':
                self.app.active_project.button_press(button)
        except:
            pass

    def closeEvent(self, event):
        self.app.exit_demo()

class Blinkenlights(QApplication):
    HOST = "localhost"
    PORT = 4223

    ipcon = None

    projects = []
    active_project = None

    error_msg = None

    def __init__(self, args):
        super(QApplication, self).__init__(args)

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowTitle("Starter Kit: Blinkenlights Demo " + config.DEMO_VERSION)

        signal.signal(signal.SIGINT, self.exit_demo)
        signal.signal(signal.SIGTERM, self.exit_demo)
        
        self.make_gui()
        self.connect()

    def exit_demo(self, signl=None, frme=None):
        try:
            self.ipcon.disconnect()
            self.timer.stop()
            self.tabs.destroy()
        except:
            pass

        sys.exit()

    def make_gui(self):
        self.main = MainWindow(self)
        self.main.setFixedSize(600, 400)
        self.main.setWindowIcon(QIcon(os.path.join(ProgramPath.program_path(), "demo-icon.png")))
        
        self.tabs = QTabWidget()
        
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        widget.setLayout(layout)

        self.main.setCentralWidget(widget)
        
        self.setup = SetupWidget(self.tabs, self)
        self.tetris = TetrisWidget(self.tabs, self)
        self.pong = PongWidget(self.tabs, self)
        self.fire = FireWidget(self.tabs, self)
        self.text = TextWidget(self.tabs, self)
        self.images = ImagesWidget(self.tabs, self)
        self.rainbow = RainbowWidget(self.tabs, self)

        self.projects.append(self.setup)
        self.projects.append(self.tetris)
        self.projects.append(self.pong)
        self.projects.append(self.fire)
        self.projects.append(self.text)
        self.projects.append(self.images)
        self.projects.append(self.rainbow)

        self.tabs.addTab(self.setup, "Setup")
        self.tabs.addTab(self.tetris, "Tetris")
        self.tabs.addTab(self.pong, "Pong")
        self.tabs.addTab(self.fire, "Fire")
        self.tabs.addTab(self.text, "Scrolling Text")
        self.tabs.addTab(self.images, "Images")
        self.tabs.addTab(self.rainbow, "Rainbow")

        self.active_project = self.projects[0]

        self.tabs.currentChanged.connect(self.tab_changed_slot)

        self.main.setWindowTitle("Starter Kit: Blinkenlights Demo " + config.DEMO_VERSION)
        self.main.show()

    def connect(self):
        config.UID_LED_STRIP_BRICKLET = None
        self.setup.label_led_strip_found.setText('No')
        self.setup.label_led_strip_uid.setText('None')

        config.UID_MULTI_TOUCH_BRICKLET = None
        self.setup.label_multi_touch_found.setText('No')
        self.setup.label_multi_touch_uid.setText('None')

        config.UID_DUAL_BUTTON_BRICKLET = (None, None)
        self.setup.label_dual_button1_found.setText('No')
        self.setup.label_dual_button1_uid.setText('None')
        self.setup.label_dual_button2_found.setText('No')
        self.setup.label_dual_button2_uid.setText('None')

        config.UID_PIEZO_SPEAKER_BRICKLET = None
        self.setup.label_piezo_speaker_found.setText('No')
        self.setup.label_piezo_speaker_uid.setText('None')

        config.UID_SEGMENT_DISPLAY_4X7_BRICKLET = None
        self.setup.label_segment_display_found.setText('No')
        self.setup.label_segment_display_uid.setText('None')
        
        if self.ipcon != None:
            try:
                self.ipcon.disconnect()
            except:
                pass

        self.ipcon = IPConnection()
        
        host = self.setup.edit_host.text()
        port = self.setup.spinbox_port.value()
        try:
            self.ipcon.connect(host, port)
        except Error as e:
            self.error_msg.showMessage('Connection Error: ' + str(e.description) + "\nBrickd installed and running?")
            return
        except socket.error as e:
            self.error_msg.showMessage('Socket error: ' + str(e) + "\nBrickd installed and running?")
            return

        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE,
                                     self.cb_enumerate)
        self.ipcon.register_callback(IPConnection.CALLBACK_CONNECTED,
                                     self.cb_connected)
        
        # Wait for a second to give user visual feedback
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.ipcon.enumerate)
        timer.start(250)

    def tab_changed_slot(self, tabIndex):
        self.active_project.stop()
        self.active_project = self.projects[tabIndex]
        self.active_project.start()

    def cb_enumerate(self, uid, connected_uid, position, hardware_version,
                     firmware_version, device_identifier, enumeration_type):
        if enumeration_type == IPConnection.ENUMERATION_TYPE_CONNECTED or \
           enumeration_type == IPConnection.ENUMERATION_TYPE_AVAILABLE:
            if device_identifier == LEDStrip.DEVICE_IDENTIFIER:
                config.UID_LED_STRIP_BRICKLET = uid
                self.setup.label_led_strip_found.setText('Yes')
                self.setup.label_led_strip_uid.setText(uid)
            elif device_identifier == MultiTouch.DEVICE_IDENTIFIER:
                config.UID_MULTI_TOUCH_BRICKLET = uid
                self.setup.label_multi_touch_found.setText('Yes')
                self.setup.label_multi_touch_uid.setText(uid)
            elif device_identifier == DualButton.DEVICE_IDENTIFIER:
                if config.UID_DUAL_BUTTON_BRICKLET[0] == None:
                    config.UID_DUAL_BUTTON_BRICKLET = (uid, None)
                    self.setup.label_dual_button1_found.setText('Yes')
                    self.setup.label_dual_button1_uid.setText(uid)
                else:
                    config.UID_DUAL_BUTTON_BRICKLET = (config.UID_DUAL_BUTTON_BRICKLET[0], uid)
                    self.setup.label_dual_button2_found.setText('Yes')
                    self.setup.label_dual_button2_uid.setText(uid)
            elif device_identifier == PiezoSpeaker.DEVICE_IDENTIFIER:
                config.UID_PIEZO_SPEAKER_BRICKLET = uid
                self.setup.label_piezo_speaker_found.setText('Yes')
                self.setup.label_piezo_speaker_uid.setText(uid)
            elif device_identifier == SegmentDisplay4x7.DEVICE_IDENTIFIER:
                config.UID_SEGMENT_DISPLAY_4X7_BRICKLET = uid
                self.setup.label_segment_display_found.setText('Yes')
                self.setup.label_segment_display_uid.setText(uid)

    def cb_connected(self, connected_reason):
        if connected_reason == IPConnection.CONNECT_REASON_AUTO_RECONNECT:
            while True:
                try:
                    self.ipcon.enumerate()
                    break
                except Error as e:
                    self.error_msg.showMessage('Enumerate Error: ' + str(e.description))
                    time.sleep(1)

if __name__ == "__main__":
    blinkenlights = Blinkenlights(sys.argv)
    sys.exit(blinkenlights.exec_())
