#!/usr/bin/env python
# -*- coding: utf-8 -*

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_led_strip import LEDStrip

import colorsys

import config

letterforms = '''\
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


class ScrollingText:
    HOST = 'localhost'
    PORT = 4223
    UID = 'abc'
    
    COLOR = None # = Rainbow
#    COLOR = (255, 0, 0) # = Red 

    SPEED = 40 # in ms per step

    # Position of R, G and B pixel on LED Pixel
    R = 2
    G = 1
    B = 0

    LED_ROWS = 20
    LED_COLS = 10

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

    leds = [x[:] for x in [[(0, 0, 0)]*LED_COLS]*LED_ROWS]
    
    text_position = 0
    
    rainbow_length = 32
    rainbow_index = 0

    def __init__(self, ipcon):
        self.table = {}
        for form in letterforms:
            if '|' in form:
                self.table[form[-2]] = form[:-3].split('|')
        self.rows = len(self.table.values()[0])
        
        self.new_text('Starter Kit: Blinkenlights')
        
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
            self.UID = None
            return

        self.update_speed()
        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         self.frame_rendered)

    def stop_rendering(self):
        self.led_strip.register_callback(self.led_strip.CALLBACK_FRAME_RENDERED,
                                         None)

    def new_text(self, text_to_display):
        text_to_display = '   ' + text_to_display
        self.text = ['','','','','','','']
            
        for row in range(self.rows):
            for c in text_to_display:
                try:
                    self.text[row] += self.table[c][row]
                except:
                    self.text[row] += ' '
                    
        self.text_position = 0

    def update_speed(self):
        self.led_strip.set_frame_duration(self.SPEED)

    def frame_rendered(self, _):
        self.frame_upload()
        self.frame_prepare_next()
        
    def frame_upload(self):
        r = []
        g = []
        b = []
        for col in range(self.LED_ROWS):
            row_range = range(self.LED_COLS)
            if col % 2 == 0:
                row_range = reversed(row_range)
            for row in row_range:
                r.append(self.leds[col][row][self.R])
                g.append(self.leds[col][row][self.G])
                b.append(self.leds[col][row][self.B])

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

            self.led_strip.set_rgb_values(i*16, length, r_chunk[i], g_chunk[i], b_chunk[i])

    def frame_prepare_next(self):
        self.leds = [x[:] for x in [[(0, 0, 0)]*self.LED_COLS]*self.LED_ROWS]
        
        if self.COLOR == None:
            r, g, b = colorsys.hsv_to_rgb(1.0*self.rainbow_index/self.rainbow_length, 1, 0.1)
            r, g, b = int(r*255), int(g*255), int(b*255)
            self.rainbow_index = (self.rainbow_index + 1) % self.rainbow_length
        else:
            r, g, b = self.COLOR

        for col in range(len(self.text)):
            for row in range(self.LED_ROWS):
                if self.text[col][(self.text_position+row) % len(self.text[0])] == 'X':
                    self.leds[row][col] = (r, g, b)
                else:
                    self.leds[row][col] = (0, 0, 0)

        self.text_position += 1
