#!/usr/bin/env python
# -*- coding: utf-8 -*

# Tetris implemented according to tetris guidline:
# http://tetris.wikia.com/wiki/Tetris_Guideline

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker
from tinkerforge.bricklet_segment_display_4x7 import SegmentDisplay4x7
from tinkerforge.bricklet_multi_touch import MultiTouch

import random
import copy
import time

import config

from threading import Thread

from repeated_timer import RepeatedTimer
from keypress import KeyPress


class TetrisSegmentDisplay:
    UID = config.UID_SEGMENT_DISPLAY_4X7_BRICKLET
    DIGITS = [0x3f,0x06,0x5b,0x4f,
              0x66,0x6d,0x7d,0x07,
              0x7f,0x6f,0x77,0x7c,
              0x39,0x5e,0x79,0x71] # // 0~9,A,b,C,d,E,F

    line_count = 0

    def __init__(self, ipcon):
        self.okay = False
        self.UID = config.UID_SEGMENT_DISPLAY_4X7_BRICKLET
        self.ipcon = ipcon

        if self.UID == None:
            print("Not Configured: Segment Display 4x7")
            return

        self.sd = SegmentDisplay4x7(self.UID, self.ipcon)

        try:
            self.sd.get_counter_value()
            print("Found: Segment Display 4x7 ({0})").format(self.UID)
        except:
            print("Not Found: Segment Display 4x7 ({0})").format(self.UID)
            return

        self.okay = True

        self.line_count_to_display()

    def increase_line_count(self, increase_by):
        if not self.okay:
            return

        self.line_count += increase_by
        self.line_count_to_display()

    def line_count_to_display(self):
        if not self.okay:
            return

        segments = (
            self.DIGITS[self.line_count/1000 % 10],
            self.DIGITS[self.line_count/100  % 10],
            self.DIGITS[self.line_count/10   % 10],
            self.DIGITS[self.line_count/1    % 10]
        )
        self.sd.set_segments(segments, 7, False)


class TetrisSpeaker:
    UID = config.UID_PIEZO_SPEAKER_BRICKLET

    def __init__(self, ipcon):
        self.okay = False
        self.UID = config.UID_PIEZO_SPEAKER_BRICKLET
        self.ipcon = ipcon

        if self.UID == None:
            print("Not Configured: Piezo Speaker")
            return

        self.speaker = PiezoSpeaker(self.UID, self.ipcon)

        try:
            self.speaker.get_identity()
            print("Found: Piezo Speaker ({0})").format(self.UID)
        except:
            print("Not Found: Piezo Speaker ({0})").format(self.UID)
            return

        self.okay = True

    def sirene(self, freq):
        if not self.okay:
            return

        for j in range(2):
            for i in range(25):
                self.speaker.beep(10, freq + i*20)
                time.sleep(0.007)
            for i in range(25):
                self.speaker.beep(10, freq + 24*20 - i*20)
                time.sleep(0.007)

    def beep_input(self):
        if not self.okay:
            return

        self.speaker.beep(10, 500)

    def beep_delete_line(self, lines):
        if not self.okay:
            return

        Thread(target=self.sirene, args=(1000*lines,)).start()


class Tetris:
    # Position of R, G and B pixel on LED Pixel
    R = 2
    G = 1
    B = 0

    FIELD_ROWS = 24 # 22 rows in playfield, with only 20 columns visible and 2 coloms border
    FIELD_COLS = 12 # 10 columns in playfield, 2 column border

    FIELD_ROW_START = 2
    FIELD_COL_START = 4

    drop_timer = None

    tetromino_current = 'O'
    tetromino_form    = 0
    tetromino_pos_row = FIELD_ROW_START
    tetromino_pos_col = FIELD_COL_START

    colors = [
        (10,  10,  10),  # grey
        (255, 0,   0),   # red
        (255, 80,  0),   # orange
        (255, 255, 0),   # yellow
        (0,   255, 0),   # green
        (0,   0,   255), # blue
        (255, 0,   150), # violet
        (255, 0,   40),  # purple
    ]

    playfield = [x[:] for x in [[0]*FIELD_COLS]*FIELD_ROWS]

    tetromino = {
      None: [[[0], [0], [0], [0]]],

      'I': [[[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,2,0,0]],
            [[2,2,2,2], [0,0,2,0], [0,0,0,0], [0,2,0,0]],
            [[0,0,0,0], [0,0,2,0], [2,2,2,2], [0,2,0,0]],
            [[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,2,0,0]]],

      'J': [[[6,0,0], [0,6,6], [0,0,0], [0,6,0]],
            [[6,6,6], [0,6,0], [6,6,6], [0,6,0]],
            [[0,0,0], [0,6,0], [0,0,6], [6,6,0]]],

      'L': [[[0,0,5], [0,5,0], [0,0,0], [5,5,0]],
            [[5,5,5], [0,5,0], [5,5,5], [0,5,0]],
            [[0,0,0], [0,5,5], [5,0,0], [0,5,0]]],

      'O': [[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],
            [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],
            [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]]],

      'S': [[[0,3,3], [0,3,0], [0,0,0], [3,0,0]],
            [[3,3,0], [0,3,3], [0,3,3], [3,3,0]],
            [[0,0,0], [0,0,3], [3,3,0], [0,3,0]]],

      'T': [[[0,7,0], [0,7,0], [0,0,0], [0,7,0]],
            [[7,7,7], [0,7,7], [7,7,7], [7,7,0]],
            [[0,0,0], [0,7,0], [0,7,0], [0,7,0]]],

      'Z': [[[4,4,0], [0,0,4], [0,0,0], [0,4,0]],
            [[0,4,4], [0,4,4], [4,4,0], [4,4,0]],
            [[0,0,0], [0,4,0], [0,4,4], [4,0,0]]]
    }

    random_bag       = ['O', 'I', 'S', 'Z', 'L', 'J', 'T']
    random_bag_index = len(random_bag)-1

    game_over = [
        "GameOverGameOverGameOverGameOverGameOverGameOverGameOve",
        "                                                       ",
        "         GGGG                      OO                  ",
        "        G   GG                    O  O                 ",
        "        G      aaa  mmm mm   ee   O  O v   v  ee   rr  ",
        "        G  GG     a m  m  m e  e  O  O v   v e  e r  r ",
        "        G    G aaaa m  m  m eeee  O  O  v v  eeee r    ",
        "        G    G a  a m  m  m e     O  O  v v  e    r    ",
        "         GGGG  aaaa m  m  m  eee   OO    v    eee r    ",
        "                                                       ",
        "                                                       ",
        "GameOverGameOverGameOverGameOverGameOverGameOverGameOve"
    ]
    game_over_to_color = {
        ' ': 0,
        'G': 1,
        'a': 2,
        'm': 3,
        'e': 4,
        'O': 5,
        'v': 6,
        'r': 7
    }
    game_over_position = 0
    is_game_over = False
    loop = True

    def __init__(self, ipcon):
        self.okay = False
        self.UID = config.UID_LED_STRIP_BRICKLET
        self.ipcon = ipcon

        if self.UID == None:
            print("Not Configured: LED Strip (required)")
            return

        self.led_strip = LEDStrip(self.UID, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            print("Found: LED Strip ({0})").format(self.UID)
        except:
            print("Not Found: LED Strip ({0})").format(self.UID)
            return

        self.kp = KeyPress(self.ipcon)
        self.display = TetrisSegmentDisplay(self.ipcon)
        self.speaker = TetrisSpeaker(self.ipcon)

        self.okay = True

        self.led_strip.set_frame_duration(40)
        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         self.frame_rendered)

        self.init_tetris()

    def close(self):
        try:
            self.ipcon.disconnect()
        except:
            pass

    def init_tetris(self):
        self.tetromino_current = 'O'
        self.tetromino_form    = 0
        self.tetromino_pos_row = self.FIELD_ROW_START
        self.tetromino_pos_col = self.FIELD_COL_START

        # Add border to playfield
        self.playfield = [x[:] for x in [[0]*self.FIELD_COLS]*self.FIELD_ROWS]
        self.playfield[0] = [255]*self.FIELD_COLS
        self.playfield[-1] = [255]*self.FIELD_COLS
        for col in self.playfield[1:-1]:
            col[0] = 255
            col[-1] = 255

        # initialize current tetronimo randomly
        self.tetromino_current = self.get_random_tetromino()
        self.is_game_over = False
        if self.drop_timer != None:
            self.drop_timer.interval = 1

    def frame_rendered(self, length):
        self.write_playfield()

    # See http://tetris.wikia.com/wiki/Random_Generator for
    # details of random bag implementation according to tetris specification
    def get_random_tetromino(self):
        self.random_bag_index += 1
        if self.random_bag_index >= len(self.random_bag):
            self.random_bag_index = 0
            random.shuffle(self.random_bag)

        return self.random_bag[self.random_bag_index]

    def add_tetromino_to_field(self, field, pos_row, pos_col, tetromino):
        for index_col, col in enumerate(self.tetromino[tetromino]):
            for index_row, color in enumerate(col[self.tetromino_form]):
                if color != 0:
                    row = pos_row + index_row
                    col = pos_col + index_col
                    if row >= 0 and row < self.FIELD_ROWS and col >= 0 and col < self.FIELD_COLS:
                        field[row][col] = color

    def tetromino_fits(self, field, pos_row, pos_col, tetromino, form):
        for index_col, col in enumerate(self.tetromino[tetromino]):
            for index_row, color in enumerate(col[form]):
                if color != 0:
                    row = pos_row + index_row
                    col = pos_col + index_col
                    if row >= 0 and row < self.FIELD_ROWS and col >= 0 and col < self.FIELD_COLS:
                        if field[row][col] != 0:
                            return False
        return True

    def write_playfield(self):
        if not self.okay:
            return

        field = copy.deepcopy(self.playfield)
        if not self.is_game_over:
            self.add_tetromino_to_field(field, self.tetromino_pos_row, self.tetromino_pos_col, self.tetromino_current)

        r = []
        g = []
        b = []
        for col in reversed(range(3, self.FIELD_ROWS-1)):
            row_range = range(1, self.FIELD_COLS-1)
            if col % 2 == 0:
                row_range = reversed(row_range)
            for row in row_range:
                r.append(self.colors[field[col][row]][self.R])
                g.append(self.colors[field[col][row]][self.G])
                b.append(self.colors[field[col][row]][self.B])

        # Make chunks of size 16
        r_chunk = [r[i:i+16] for i in range(0, len(r), 16)]
        g_chunk = [g[i:i+16] for i in range(0, len(g), 16)]
        b_chunk = [b[i:i+16] for i in range(0, len(b), 16)]

        for i in range(len(r_chunk)):
            length = len(r_chunk[i])

            # Fill up chunks with zeros
            r_chunk[i].extend([0]*(16-len(r_chunk[i])))
            g_chunk[i].extend([0]*(16-len(g_chunk[i])))
            b_chunk[i].extend([0]*(16-len(b_chunk[i])))

            try:
                self.led_strip.set_rgb_values(i*16, length, r_chunk[i], g_chunk[i], b_chunk[i])
            except:
                break

    def clear_lines(self, rows_to_clear):
        if not self.okay:
            return

        self.drop_timer.stop()
        rows_save = {}
        for to_clear in rows_to_clear:
            rows_save[to_clear] = self.playfield[to_clear]

        self.display.increase_line_count(len(rows_to_clear))
        self.speaker.beep_delete_line(len(rows_to_clear))

        for i in range(6):
            if i % 2 == 0:
                for to_clear in rows_to_clear:
                    self.playfield[to_clear] = [255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255]
            else:
                for to_clear in rows_to_clear:
                    self.playfield[to_clear] = rows_save[to_clear]
            time.sleep(0.1)

        for to_clear in rows_to_clear:
            for row in reversed(range(1, to_clear+1)):
                self.playfield[row] = self.playfield[row-1]
            self.playfield[1] = [255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255]

        self.drop_timer.start()

    def check_for_line_clears(self):
        rows_to_clear = []

        for row_index, col in enumerate(self.playfield[1:-1]):
            to_clear = True
            for color in col[1:-1]:
                if color == 0:
                    to_clear = False
                    break
            if to_clear:
                rows_to_clear.append(row_index+1)

        if rows_to_clear != []:
            self.clear_lines(rows_to_clear)

    def new_tetromino(self):
        self.add_tetromino_to_field(self.playfield, self.tetromino_pos_row, self.tetromino_pos_col, self.tetromino_current)
        self.tetromino_current = None
        self.check_for_line_clears()
        self.tetromino_current = self.get_random_tetromino()
        self.tetromino_pos_row = self.FIELD_ROW_START
        self.tetromino_pos_col = self.FIELD_COL_START
        self.tetromino_form    = 0
        if not self.tetromino_fits(self.playfield, self.tetromino_pos_row, self.tetromino_pos_col, self.tetromino_current, self.tetromino_form):
            self.is_game_over = True
            self.game_over_position = 0
            self.drop_timer.interval = 0.15

    def next_game_over_step(self):
        for col in range(len(self.game_over)):
            for row in range(10):
                self.playfield[7+col][row] = self.game_over_to_color[self.game_over[col][(self.game_over_position+row) % len(self.game_over[0])]]

        self.game_over_position += 1

    def drop_tetromino(self):
        if self.is_game_over:
            self.next_game_over_step()
            return
        if self.tetromino_fits(self.playfield, self.tetromino_pos_row+1, self.tetromino_pos_col, self.tetromino_current, self.tetromino_form):
            self.tetromino_pos_row += 1
        else:
            self.new_tetromino()

    def move_tetromino(self, row, col, form):
        if self.tetromino_fits(self.playfield, self.tetromino_pos_row+row, self.tetromino_pos_col+col, self.tetromino_current, self.tetromino_form):
            self.tetromino_pos_row += row
            self.tetromino_pos_col += col
            self.tetromino_form = form

            if row > 0:
                # restart drop timer, so we don't drop two tetrominos in a row
                self.drop_timer.stop()
                self.drop_timer.start()
        elif row == 1: # user is at bottom and hits button to go down again
            self.new_tetromino()

    def tetris_loop(self):
        self.drop_timer = RepeatedTimer(1.0, self.drop_tetromino)

        while self.loop:
            key = self.kp.read_single_keypress().lower()
            self.speaker.beep_input()

            if key == 'a':
                self.move_tetromino(0, -1, self.tetromino_form)
            elif key == 'd':
                self.move_tetromino(0, 1, self.tetromino_form)
            elif key == 's':
                self.move_tetromino(1, 0, self.tetromino_form)
            elif key == 'k':
                self.move_tetromino(0, 0, (self.tetromino_form-1) % 4)
            elif key == 'l':
                self.move_tetromino(0, 0, (self.tetromino_form+1) % 4)
            elif key == 'r':
                self.init_tetris()
            elif key == 'q':
                break

        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED, None)
        self.drop_timer.stop()
