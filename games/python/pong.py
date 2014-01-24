#!/usr/bin/env python
# -*- coding: utf-8 -*

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_piezo_speaker import PiezoSpeaker

import random
import copy
import time

import config

from threading import Thread

from repeated_timer import RepeatedTimer
from keypress import KeyPress


class PongSpeaker:
    def __init__(self, ipcon):
        self.okay = False
        self.ipcon = ipcon

        if not config.UID_PIEZO_SPEAKER_BRICKLET:
            print("Not Configured: Piezo Speaker")
            return

        self.speaker = PiezoSpeaker(config.UID_PIEZO_SPEAKER_BRICKLET, self.ipcon)

        try:
            self.speaker.get_identity()
            print("Found: Piezo Speaker ({0})".format(config.UID_PIEZO_SPEAKER_BRICKLET))
        except:
            print("Not Found: Piezo Speaker ({0})".format(config.UID_PIEZO_SPEAKER_BRICKLET))
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

    def beep_paddle_hit(self):
        if not self.okay:
            return

        self.speaker.beep(100, 500)

    def beep_sirene(self):
        if not self.okay:
            return

        Thread(target=self.sirene, args=(1000,)).start()


class Pong:
    PADDLE_SIZE = 3

# Antialased ball?
#    PONG_COLOR_INDEX_BALL_TOP = 8
#    PONG_COLOR_INDEX_BALL_LEFT = 9
#    PONG_COLOR_INDEX_BALL_RIGHT = 10
#    PONG_COLOR_INDEX_BALL_BOTTOM = 11

    COLORS = [
        (  0,   0,   0), # off
#       ( 10,  10,  10), # grey
        (255,   0,   0), # red
        (255,  80,   0), # orange
        (255, 255,   0), # yellow
        (  0, 255,   0), # green
        (  0,   0, 255), # blue
        (255,   0, 150), # violet
        (255,   0,  40), # purple
        (  0,   0,   0), # ball top
        (  0,   0,   0), # ball left
        (  0,   0,   0), # ball right
        (  0,   0,   0)  # ball bottom
    ]

    SCORE_FONT = {
        0: ["222",
            "202",
            "202",
            "202",
            "222"],
        1: ["020",
            "020",
            "020",
            "020",
            "020"],
        2: ["222",
            "002",
            "222",
            "200",
            "222"],
        3: ["222",
            "002",
            "222",
            "002",
            "222"],
        4: ["202",
            "202",
            "222",
            "002",
            "002"],
        5: ["222",
            "200",
            "222",
            "002",
            "222"],
        6: ["222",
            "200",
            "222",
            "202",
            "222"],
        7: ["222",
            "002",
            "002",
            "002",
            "002"],
        8: ["222",
            "202",
            "222",
            "202",
            "222"],
        9: ["222",
            "202",
            "222",
            "002",
            "002"],
    }

    playfield = [x[:] for x in [[0]*config.LED_COLS]*config.LED_ROWS]
    score = [0, 0]
    paddle_position_x = [4, 15]
    paddle_position_y = [3, 3]
    ball_position = [10, 5]
    ball_direction = [0.1, 0.2]
    timer = None
    loop = True

    def __init__(self, ipcon):
        self.okay = False
        self.ipcon = ipcon

        if not config.UID_LED_STRIP_BRICKLET:
            print("Not Configured: LED Strip (required)")
            return

        self.led_strip = LEDStrip(config.UID_LED_STRIP_BRICKLET, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            print("Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
        except:
            print("Not Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
            return

        self.kp = KeyPress(self.ipcon)
        self.speaker = PongSpeaker(self.ipcon)

        self.okay = True

        self.led_strip.set_frame_duration(40)
        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         self.frame_rendered)

        self.init_game()

    def init_game(self):
        self.new_ball()
        self.paddle_position_y = [3, 3]
        self.score = [0, 0]

    def frame_rendered(self, length):
        self.write_playfield()

    def write_playfield(self):
        if not self.okay:
            return

        field = copy.deepcopy(self.playfield)

        self.add_score_to_playfield(field)
        self.add_paddles_to_playfield(field)
        self.add_ball_to_playfield(field)

        # Reorder LED data into R, G and B channel
        r = []
        g = []
        b = []
        for row in range(config.LED_ROWS):
            col_range = range(config.LED_COLS)
            if row % 2 == 0:
                col_range = reversed(col_range)
            for col in col_range:
                r.append(self.COLORS[field[row][col]][config.R_INDEX])
                g.append(self.COLORS[field[row][col]][config.G_INDEX])
                b.append(self.COLORS[field[row][col]][config.B_INDEX])

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

    def add_score_to_playfield(self, field):
        for row in range(3):
            for col in range(5):
                field[row][col+1] = int(self.SCORE_FONT[self.score[0]][col][row])
                field[row+17][col+1] = int(self.SCORE_FONT[self.score[1]][col][row])

    def add_ball_to_playfield(self, field):
        x = max(0, min(19, int(self.ball_position[0])))
        y = max(0, min(9, int(self.ball_position[1])))
        field[x][y] = config.PONG_COLOR_INDEX_BALL

# Antialased ball?
#        x = max(0, min(19, self.ball_position[0]))
#        y = max(0, min(9, self.ball_position[1]))
#        ix = int(x)
#        iy = int(y)
#        field[ix][iy] = config.PONG_COLOR_INDEX_BALL
#        if ix + 1 < config.LED_ROWS:
#            field[ix+1][iy] = PONG_COLOR_INDEX_BALL_RIGHT
#        if ix - 1 > 0:
#            field[ix-1][iy] = PONG_COLOR_INDEX_BALL_LEFT
#        if iy + 1 < config.LED_COLS:
#            field[ix][iy+1] = PONG_COLOR_INDEX_BALL_TOP
#        if iy - 1 > 0:
#            field[ix][iy-1] = PONG_COLOR_INDEX_BALL_BOTTOM
#
#        dx = x - int(x)
#        dy = x - int(x)
#        self.COLORS[PONG_COLOR_INDEX_BALL_RIGHT] = (0, 255*dx/64, 0)
#        self.COLORS[PONG_COLOR_INDEX_BALL_LEFT] = (0, 255*(1-dx)/64, 0)
#        self.COLORS[PONG_COLOR_INDEX_BALL_TOP] = (0, 255*dy/64, 0)
#        self.COLORS[PONG_COLOR_INDEX_BALL_BOTTOM] = (0, 255*(1-dy)/64, 0)

    def add_paddles_to_playfield(self, field):
        for player in range(2):
            for i in range(self.PADDLE_SIZE):
                field[self.paddle_position_x[player]][self.paddle_position_y[player]+i] = config.PONG_COLOR_INDEX_PLAYER[player]

    def move_paddle(self, player, change):
        new_pos = self.paddle_position_y[player] + change
        if new_pos >= 0 and new_pos <= config.LED_COLS - self.PADDLE_SIZE:
            self.paddle_position_y[player] = new_pos

    def new_ball(self):
        self.ball_position = [(config.LED_ROWS - 1.0) / 2.0, (config.LED_COLS - 1.0) / 2.0]
        self.ball_direction = [random.choice([-0.2, 0.2]), random.choice([random.randrange(1, 9)/10.0, random.randrange(-9, -1)/10.0])]

    def tick(self):
        # Move ball
        for i in range(2):
            self.ball_position[i] += self.ball_direction[i]

        # Wall collision top/bottom
        if self.ball_position[1] < 0 or self.ball_position[1] >= config.LED_COLS:
            self.ball_direction[1] = -self.ball_direction[1]

        # Wall collision left/right
        def hit_left_right(player):
            self.speaker.beep_sirene()
            self.new_ball()

            self.score[player] += 1
            if self.score[player] > 9:
                self.score[player] = 0

        if self.ball_position[0] < 0:
            hit_left_right(1)

        if self.ball_position[0] >= config.LED_ROWS:
            hit_left_right(0)

        # Paddle collision
        def hit_paddle(skew):
            self.speaker.beep_paddle_hit()
            self.ball_direction[0] = -self.ball_direction[0]
            self.ball_direction[1] -= skew
            for i in range(2):
                self.ball_direction[i] *= 1.1 # Increase speed

        if self.ball_direction[0] < 0:
            if self.paddle_position_x[0] + 0.5 <= self.ball_position[0] <= self.paddle_position_x[0] + 1.5:
                if self.paddle_position_y[0] - 0.5 <= self.ball_position[1] <= self.paddle_position_y[0] + self.PADDLE_SIZE + 0.5:
                    paddle_skew = (self.paddle_position_y[0] + self.PADDLE_SIZE/2.0 - self.ball_position[1])/10.0
                    hit_paddle(paddle_skew)

        if self.ball_direction[0] > 0:
            if self.paddle_position_x[1] - 0.5 <= self.ball_position[0] <= self.paddle_position_x[1] + 0.5:
                if self.paddle_position_y[1] - 0.5 <= self.ball_position[1] <= self.paddle_position_y[1] + self.PADDLE_SIZE + 0.5:
                    paddle_skew = (self.paddle_position_y[1] + self.PADDLE_SIZE/2.0 - self.ball_position[1])/10.0
                    hit_paddle(paddle_skew)

    def run_game_loop(self):
        self.frame_rendered(0)

        self.timer = RepeatedTimer(0.1, self.tick)

        while self.loop:
            key = self.kp.read_single_keypress().lower()

            if key == 'a':
                self.move_paddle(0, -1)
            elif key == 's':
                self.move_paddle(0, 1)
            elif key == 'k':
                self.move_paddle(1, -1)
            elif key == 'l':
                self.move_paddle(1, 1)
            elif key == 'r':
                self.init_game()
            elif key == 'q':
                break

        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED, None)
        self.timer.stop()


if __name__ == "__main__":
    # Create IP Connection and connect it
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    # Create Pong object and start game loop
    pong = Pong(ipcon)

    if pong.okay:
        print('Press q to exit')

        pong.run_game_loop()
        pong.kp.kbi.restore_stdin()

    ipcon.disconnect()
