#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import colorsys

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip
from tinkerforge.bricklet_led_strip_v2 import LEDStripV2

import config

letter_forms = '''\
       |       |       |       |       |       |       | |
  XXX  |  XXX  |  XXX  |   X   |       |  XXX  |  XXX  |!|
  X  X |  X  X |  X  X |       |       |       |       |"|
  X X  |  X X  |XXXXXXX|  X X  |XXXXXXX|  X X  |  X X  |#|
 XXXXX |X  X  X|X  X   | XXXXX |   X  X|X  X  X| XXXXX |$|
XXX   X|X X  X |XXX X  |   X   |  X XXX| X  X X|X   XXX|%|
  XX   | X  X  |  XX   | XXX   |X   X X|X    X | XXX  X|&|
  XXX  |  XXX  |   X   |  X    |       |       |       |'|
   XX  |  X    | X     | X     | X     |  X    |   XX  |(|
  XX   |    X  |     X |     X |     X |    X  |  XX   |)|
       | X   X |  X X  |XXXXXXX|  X X  | X   X |       |*|
       |   X   |   X   | XXXXX |   X   |   X   |       |+|
       |       |       |  XXX  |  XXX  |   X   |  X    |,|
       |       |       | XXXXX |       |       |       |-|
       |       |       |       |  XXX  |  XXX  |  XXX  |.|
      X|     X |    X  |   X   |  X    | X     |X      |/|
  XXX  | X   X |X     X|X     X|X     X| X   X |  XXX  |0|
   X   |  XX   | X X   |   X   |   X   |   X   | XXXXX |1|
 XXXXX |X     X|      X| XXXXX |X      |X      |XXXXXXX|2|
 XXXXX |X     X|      X| XXXXX |      X|X     X| XXXXX |3|
X      |X    X |X    X |X    X |XXXXXXX|     X |     X |4|
XXXXXXX|X      |X      |XXXXXX |      X|X     X| XXXXX |5|
 XXXXX |X     X|X      |XXXXXX |X     X|X     X| XXXXX |6|
XXXXXX |X    X |    X  |   X   |  X    |  X    |  X    |7|
 XXXXX |X     X|X     X| XXXXX |X     X|X     X| XXXXX |8|
 XXXXX |X     X|X     X| XXXXXX|      X|X     X| XXXXX |9|
   X   |  XXX  |   X   |       |   X   |  XXX  |   X   |:|
  XXX  |  XXX  |       |  XXX  |  XXX  |   X   |  X    |;|
    X  |   X   |  X    | X     |  X    |   X   |    X  |<|
       |       |XXXXXXX|       |XXXXXXX|       |       |=|
  X    |   X   |    X  |     X |    X  |   X   |  X    |>|
 XXXXX |X     X|      X|   XXX |   X   |       |   X   |?|
 XXXXX |X     X|X XXX X|X XXX X|X XXXX |X      | XXXXX |@|
   X   |  X X  | X   X |X     X|XXXXXXX|X     X|X     X|A|
XXXXXX |X     X|X     X|XXXXXX |X     X|X     X|XXXXXX |B|
 XXXXX |X     X|X      |X      |X      |X     X| XXXXX |C|
XXXXXX |X     X|X     X|X     X|X     X|X     X|XXXXXX |D|
XXXXXXX|X      |X      |XXXXX  |X      |X      |XXXXXXX|E|
XXXXXXX|X      |X      |XXXXX  |X      |X      |X      |F|
 XXXXX |X     X|X      |X  XXXX|X     X|X     X| XXXXX |G|
X     X|X     X|X     X|XXXXXXX|X     X|X     X|X     X|H|
  XXX  |   X   |   X   |   X   |   X   |   X   |  XXX  |I|
      X|      X|      X|      X|X     X|X     X| XXXXX |J|
X    X |X   X  |X  X   |XXX    |X  X   |X   X  |X    X |K|
X      |X      |X      |X      |X      |X      |XXXXXXX|L|
X     X|XX   XX|X X X X|X  X  X|X     X|X     X|X     X|M|
X     X|XX    X|X X   X|X  X  X|X   X X|X    XX|X     X|N|
XXXXXXX|X     X|X     X|X     X|X     X|X     X|XXXXXXX|O|
XXXXXX |X     X|X     X|XXXXXX |X      |X      |X      |P|
 XXXXX |X     X|X     X|X     X|X   X X|X    X | XXXX X|Q|
XXXXXX |X     X|X     X|XXXXXX |X   X  |X    X |X     X|R|
 XXXXX |X     X|X      | XXXXX |      X|X     X| XXXXX |S|
XXXXXXX|   X   |   X   |   X   |   X   |   X   |   X   |T|
X     X|X     X|X     X|X     X|X     X|X     X| XXXXX |U|
X     X|X     X|X     X|X     X| X   X |  X X  |   X   |V|
X     X|X  X  X|X  X  X|X  X  X|X  X  X|X  X  X| XX XX |W|
X     X| X   X |  X X  |   X   |  X X  | X   X |X     X|X|
X     X| X   X |  X X  |   X   |   X   |   X   |   X   |Y|
XXXXXXX|     X |    X  |   X   |  X    | X     |XXXXXXX|Z|
 XXXXX | X     | X     | X     | X     | X     | XXXXX |[|
X      | X     |  X    |   X   |    X  |     X |      X|\|
 XXXXX |     X |     X |     X |     X |     X | XXXXX |]|
   X   |  X X  | X   X |       |       |       |       |^|
       |       |       |       |       |       |XXXXXXX|_|
       |  XXX  |  XXX  |   X   |    X  |       |       |`|
       |   XX  |  X  X | X    X| XXXXXX| X    X| X    X|a|
       | XXXXX | X    X| XXXXX | X    X| X    X| XXXXX |b|
       |  XXXX | X    X| X     | X     | X    X|  XXXX |c|
       | XXXXX | X    X| X    X| X    X| X    X| XXXXX |d|
       | XXXXXX| X     | XXXXX | X     | X     | XXXXXX|e|
       | XXXXXX| X     | XXXXX | X     | X     | X     |f|
       |  XXXX | X    X| X     | X  XXX| X    X|  XXXX |g|
       | X    X| X    X| XXXXXX| X    X| X    X| X    X|h|
       |    X  |    X  |    X  |    X  |    X  |    X  |i|
       |      X|      X|      X|      X| X    X|  XXXX |j|
       | X    X| X   X | XXXX  | X  X  | X   X | X    X|k|
       | X     | X     | X     | X     | X     | XXXXXX|l|
       | X    X| XX  XX| X XX X| X    X| X    X| X    X|m|
       | X    X| XX   X| X X  X| X  X X| X   XX| X    X|n|
       |  XXXX | X    X| X    X| X    X| X    X|  XXXX |o|
       | XXXXX | X    X| X    X| XXXXX | X     | X     |p|
       |  XXXX | X    X| X    X| X  X X| X   X |  XXX X|q|
       | XXXXX | X    X| X    X| XXXXX | X   X | X    X|r|
       |  XXXX | X     |  XXXX |      X| X    X|  XXXX |s|
       |  XXXXX|    X  |    X  |    X  |    X  |    X  |t|
       | X    X| X    X| X    X| X    X| X    X|  XXXX |u|
       | X    X| X    X| X    X| X    X|  X  X |   XX  |v|
       | X    X| X    X| X    X| X XX X| XX  XX| X    X|w|
       | X    X|  X  X |   XX  |   XX  |  X  X | X    X|x|
       |  X   X|   X X |    X  |    X  |    X  |    X  |y|
       | XXXXXX|     X |    X  |   X   |  X    | XXXXXX|z|
  XXX  | X     | X     |XX     | X     | X     |  XXX  |{|
   X   |   X   |   X   |       |   X   |   X   |   X   |||
  XXX  |     X |     X |     XX|     X |     X |  XXX  |}|
 XX    |X  X  X|    XX |       |       |       |       |~|
'''.splitlines()


class Text:
    leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]
    text_position = 0
    rainbow_length = 32
    rainbow_index = 0

    def __init__(self, ipcon):
        self.letter_table = {}

        for form in letter_forms:
            if '|' in form:
                self.letter_table[form[-2]] = form[:-3].split('|')

        self.set_new_text('Starter Kit: Blinkenlights')

        self.okay = False
        self.ipcon = ipcon

        if not config.UID_LED_STRIP_BRICKLET:
            print("Not Configured: LED Strip or LED Strip V2 (required)")
            return

        if not config.IS_LED_STRIP_V2:
            self.led_strip = LEDStrip(config.UID_LED_STRIP_BRICKLET, self.ipcon)
        else:
            self.led_strip = LEDStripV2(config.UID_LED_STRIP_BRICKLET, self.ipcon)

        try:
            self.led_strip.get_frame_duration()
            if not config.IS_LED_STRIP_V2:
                print("Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
            else:
                print("Found: LED Strip V2 ({0})".format(config.UID_LED_STRIP_BRICKLET))
        except:
            if not config.IS_LED_STRIP_V2:
                print("Not Found: LED Strip ({0})".format(config.UID_LED_STRIP_BRICKLET))
            else:
                print("Not Found: LED Strip V2({0})".format(config.UID_LED_STRIP_BRICKLET))
            return

        self.okay = True

        self.update_frame_rate()
        if not config.IS_LED_STRIP_V2:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                             self.frame_rendered)
        else:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_STARTED,
                                             self.frame_rendered)

        self.led_strip.set_channel_mapping(config.CHANNEL_MAPPING)

    def stop_rendering(self):
        if not self.okay:
            return

        if not config.IS_LED_STRIP_V2:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                             None)
        else:
            self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_STARTED,
                                             None)

    def update_frame_rate(self):
        if not self.okay:
            return

        self.led_strip.set_frame_duration(int(1000.0 / config.TEXT_FRAME_RATE))

    def set_new_text(self, text):
        text = '   ' + text
        self.text_cols = ['','','','','','','']

        for col in range(len(self.text_cols)):
            for c in text:
                try:
                    self.text_cols[col] += self.letter_table[c][col]
                except:
                    self.text_cols[col] += ' '

        self.text_position = 0

    def frame_rendered(self, _):
        self.frame_upload()
        self.frame_prepare_next()

    def frame_upload(self):
        if not self.okay:
            return

        # Reorder LED data into R, G and B channel
        r = []
        g = []
        b = []
        frame = []

        for row in range(config.LED_ROWS):
            col_range = range(config.LED_COLS)
            if row % 2 == 0:
                col_range = reversed(col_range)
            for col in col_range:
                r.append(self.leds[row][col][0])
                g.append(self.leds[row][col][1])
                b.append(self.leds[row][col][2])
                frame.append(self.leds[row][col][0])
                frame.append(self.leds[row][col][1])
                frame.append(self.leds[row][col][2])

        if not config.IS_LED_STRIP_V2:
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
        else:
            try:
                self.led_strip.set_led_values(0, frame)
            except:
                return

    def frame_prepare_next(self):
        self.leds = [x[:] for x in [[(0, 0, 0)]*config.LED_COLS]*config.LED_ROWS]

        if not config.TEXT_COLOR:
            r, g, b = colorsys.hsv_to_rgb(1.0*self.rainbow_index/self.rainbow_length, 1, 0.1)
            r, g, b = int(r*255), int(g*255), int(b*255)
            self.rainbow_index = (self.rainbow_index + 1) % self.rainbow_length
        else:
            r, g, b = config.TEXT_COLOR

        for col in range(len(self.text_cols)):
            for row in range(config.LED_ROWS):
                if self.text_cols[col][(self.text_position+row) % len(self.text_cols[0])] == 'X':
                    self.leds[row][col + config.TEXT_TOP_OFFSET] = (r, g, b)
                else:
                    self.leds[row][col + config.TEXT_TOP_OFFSET] = (0, 0, 0)

        self.text_position += 1


if __name__ == "__main__":
    # Create IP Connection and connect it
    ipcon = IPConnection()
    ipcon.connect(config.HOST, config.PORT)

    # Create Text object and start rendering
    text = Text(ipcon)

    if len(sys.argv) > 1:
        text.set_new_text(' '.join(sys.argv[1:]))

    text.frame_rendered(0)

    raw_input('Press enter to exit\n') # Use input() in Python 3

    ipcon.disconnect()
