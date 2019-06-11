#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Starter Kit: Blinkenlights Demo Application
Copyright (C) 2013 Olaf Lüke <olaf@tinkerforge.com>
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2018 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

main.py: Entry file for Demo

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

import sys
if (sys.hexversion & 0xFF000000) != 0x03000000:
    print('Python 3.x required')
    sys.exit(1)

import socket
import time
import math
import signal
import os

def prepare_package(package_name):
    # from http://www.py2exe.org/index.cgi/WhereAmI
    if hasattr(sys, 'frozen'):
        program_path = os.path.dirname(os.path.realpath(sys.executable))
    else:
        program_path = os.path.dirname(os.path.realpath(__file__))

    # add program_path so OpenGL is properly imported
    sys.path.insert(0, program_path)

    # allow the program to be directly started by calling 'main.py'
    # without '<package_name>' being in the path already
    if package_name not in sys.modules:
        head, tail = os.path.split(program_path)

        if head not in sys.path:
            sys.path.insert(0, head)

        if not hasattr(sys, 'frozen'):
            # load and inject in modules list, this allows to have the source in a
            # directory named differently than '<package_name>'
            sys.modules[package_name] = __import__(tail, globals(), locals())

prepare_package('starter_kit_blinkenlights_demo')

from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QErrorMessage, QGridLayout, QTabWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QIcon, QPalette, QTextFormat, QFont

from starter_kit_blinkenlights_demo.tinkerforge.ip_connection import IPConnection
from starter_kit_blinkenlights_demo.tinkerforge.ip_connection import Error
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip import LEDStrip
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_led_strip_v2 import LEDStripV2
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_segment_display_4x7 import SegmentDisplay4x7
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_multi_touch import MultiTouch
from starter_kit_blinkenlights_demo.tinkerforge.bricklet_dual_button import DualButton

from starter_kit_blinkenlights_demo.setup_widget import SetupWidget
from starter_kit_blinkenlights_demo.tetris_widget import TetrisWidget
from starter_kit_blinkenlights_demo.pong_widget import PongWidget
from starter_kit_blinkenlights_demo.fire_widget import FireWidget
from starter_kit_blinkenlights_demo.text_widget import TextWidget
from starter_kit_blinkenlights_demo.images_widget import ImagesWidget
from starter_kit_blinkenlights_demo.rainbow_widget import RainbowWidget
from starter_kit_blinkenlights_demo.load_pixmap import load_pixmap, get_resources_path
import starter_kit_blinkenlights_demo.config as config

def load_commit_id(name):
    try:
        # Don't warn if the file is missing, as it is expected when run from source.
        path = get_resources_path(name, warn_on_missing_file=False)

        if path is not None:
            with open(path, 'r') as f:
                return f.read().strip()
    except FileNotFoundError:
        pass

    return None

INTERNAL = load_commit_id('internal')

SNAPSHOT = load_commit_id('snapshot')

DEMO_FULL_VERSION = config.DEMO_VERSION

if INTERNAL != None:
    DEMO_FULL_VERSION += '+internal~{}'.format(INTERNAL)
elif SNAPSHOT != None:
    DEMO_FULL_VERSION += '+snapshot~{}'.format(SNAPSHOT)

class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.app = app

    def keyPressEvent(self, event):
        try:
            button = event.text()[0]
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
        super().__init__(args)

        self.error_msg = QErrorMessage()
        self.error_msg.setWindowTitle("Starter Kit: Blinkenlights Demo " + DEMO_FULL_VERSION)

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
        self.main.setWindowIcon(QIcon(load_pixmap('starter_kit_blinkenlights_demo-icon.png')))

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
        self.tabs.addTab(self.text, "Text")
        self.tabs.addTab(self.images, "Images")
        self.tabs.addTab(self.rainbow, "Rainbow")

        self.active_project = self.projects[0]

        self.tabs.currentChanged.connect(self.tab_changed_slot)

        self.main.setWindowTitle("Starter Kit: Blinkenlights Demo " + DEMO_FULL_VERSION)
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
            self.error_msg.showMessage('Connection Error: ' + str(e.description) + "<br><br>Brickd installed and running?")
            return
        except socket.error as e:
            self.error_msg.showMessage('Socket error: ' + str(e) + "<br><br>Brickd installed and running?")
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
            if device_identifier == LEDStrip.DEVICE_IDENTIFIER or device_identifier == LEDStripV2.DEVICE_IDENTIFIER:
                if device_identifier == LEDStripV2.DEVICE_IDENTIFIER:
                    self.setup.label_7.setText('LED Strip V2')
                    config.IS_LED_STRIP_V2 = True
                else:
                    self.setup.label_7.setText('LED Strip')
                    config.IS_LED_STRIP_V2 = False
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
    argv = sys.argv

    sys.exit(Blinkenlights(argv).exec_())
