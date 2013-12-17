<?php

require_once('Tinkerforge/IPConnection.php');
require_once('Tinkerforge/BrickletLEDStrip.php');
require_once(__DIR__ . '/Config.php');

use Tinkerforge\IPConnection;
use Tinkerforge\BrickletLEDStrip;

// based on http://web.mit.edu/storborg/Public/hsvtorgb.c
function hsv2rgb($h, $s, $v)
{
    if($s == 0) {
        // color is grayscale
        return array(v, v, v);
    }

    // make hue 0-5
    $region = (int)($h / 43);

    // find remainder part, make it from 0-255
    $fpart = ($h - ($region * 43)) * 6;

    // calculate temp vars, doing integer multiplication
    $p = ($v * (255 - $s)) >> 8;
    $q = ($v * (255 - (($s * $fpart) >> 8))) >> 8;
    $t = ($v * (255 - (($s * (255 - $fpart)) >> 8))) >> 8;

    // assign temp vars based on color cone region
    switch($region) {
    case 0:  $r = $v; $g = $t; $b = $p; break;
    case 1:  $r = $q; $g = $v; $b = $p; break;
    case 2:  $r = $p; $g = $v; $b = $t; break;
    case 3:  $r = $p; $g = $q; $b = $v; break;
    case 4:  $r = $t; $g = $p; $b = $v; break;
    default: $r = $v; $g = $p; $b = $q; break;
    }

    return array($r, $g, $b);
}

class Text
{
    const CHUNK_SIZE = 16;

    private $letterForms = array(
    '       |       |       |       |       |       |       | ',
    '  XXX  |  XXX  |  XXX  |   X   |       |  XXX  |  XXX  |!',
    '  X  X |  X  X |  X  X |       |       |       |       |"',
    '  X X  |  X X  |XXXXXXX|  X X  |XXXXXXX|  X X  |  X X  |#',
    ' XXXXX |X  X  X|X  X   | XXXXX |   X  X|X  X  X| XXXXX |$',
    'XXX   X|X X  X |XXX X  |   X   |  X XXX| X  X X|X   XXX|%',
    '  XX   | X  X  |  XX   | XXX   |X   X X|X    X | XXX  X|&',
    '  XXX  |  XXX  |   X   |  X    |       |       |       |\'',
    '   XX  |  X    | X     | X     | X     |  X    |   XX  |(',
    '  XX   |    X  |     X |     X |     X |    X  |  XX   |)',
    '       | X   X |  X X  |XXXXXXX|  X X  | X   X |       |*',
    '       |   X   |   X   | XXXXX |   X   |   X   |       |+',
    '       |       |       |  XXX  |  XXX  |   X   |  X    |,',
    '       |       |       | XXXXX |       |       |       |-',
    '       |       |       |       |  XXX  |  XXX  |  XXX  |.',
    '      X|     X |    X  |   X   |  X    | X     |X      |/',
    '  XXX  | X   X |X     X|X     X|X     X| X   X |  XXX  |0',
    '   X   |  XX   | X X   |   X   |   X   |   X   | XXXXX |1',
    ' XXXXX |X     X|      X| XXXXX |X      |X      |XXXXXXX|2',
    ' XXXXX |X     X|      X| XXXXX |      X|X     X| XXXXX |3',
    'X      |X    X |X    X |X    X |XXXXXXX|     X |     X |4',
    'XXXXXXX|X      |X      |XXXXXX |      X|X     X| XXXXX |5',
    ' XXXXX |X     X|X      |XXXXXX |X     X|X     X| XXXXX |6',
    'XXXXXX |X    X |    X  |   X   |  X    |  X    |  X    |7',
    ' XXXXX |X     X|X     X| XXXXX |X     X|X     X| XXXXX |8',
    ' XXXXX |X     X|X     X| XXXXXX|      X|X     X| XXXXX |9',
    '   X   |  XXX  |   X   |       |   X   |  XXX  |   X   |:',
    '  XXX  |  XXX  |       |  XXX  |  XXX  |   X   |  X    |;',
    '    X  |   X   |  X    | X     |  X    |   X   |    X  |<',
    '       |       |XXXXXXX|       |XXXXXXX|       |       |=',
    '  X    |   X   |    X  |     X |    X  |   X   |  X    |>',
    ' XXXXX |X     X|      X|   XXX |   X   |       |   X   |?',
    ' XXXXX |X     X|X XXX X|X XXX X|X XXXX |X      | XXXXX |@',
    '   X   |  X X  | X   X |X     X|XXXXXXX|X     X|X     X|A',
    'XXXXXX |X     X|X     X|XXXXXX |X     X|X     X|XXXXXX |B',
    ' XXXXX |X     X|X      |X      |X      |X     X| XXXXX |C',
    'XXXXXX |X     X|X     X|X     X|X     X|X     X|XXXXXX |D',
    'XXXXXXX|X      |X      |XXXXX  |X      |X      |XXXXXXX|E',
    'XXXXXXX|X      |X      |XXXXX  |X      |X      |X      |F',
    ' XXXXX |X     X|X      |X  XXXX|X     X|X     X| XXXXX |G',
    'X     X|X     X|X     X|XXXXXXX|X     X|X     X|X     X|H',
    '  XXX  |   X   |   X   |   X   |   X   |   X   |  XXX  |I',
    '      X|      X|      X|      X|X     X|X     X| XXXXX |J',
    'X    X |X   X  |X  X   |XXX    |X  X   |X   X  |X    X |K',
    'X      |X      |X      |X      |X      |X      |XXXXXXX|L',
    'X     X|XX   XX|X X X X|X  X  X|X     X|X     X|X     X|M',
    'X     X|XX    X|X X   X|X  X  X|X   X X|X    XX|X     X|N',
    'XXXXXXX|X     X|X     X|X     X|X     X|X     X|XXXXXXX|O',
    'XXXXXX |X     X|X     X|XXXXXX |X      |X      |X      |P',
    ' XXXXX |X     X|X     X|X     X|X   X X|X    X | XXXX X|Q',
    'XXXXXX |X     X|X     X|XXXXXX |X   X  |X    X |X     X|R',
    ' XXXXX |X     X|X      | XXXXX |      X|X     X| XXXXX |S',
    'XXXXXXX|   X   |   X   |   X   |   X   |   X   |   X   |T',
    'X     X|X     X|X     X|X     X|X     X|X     X| XXXXX |U',
    'X     X|X     X|X     X|X     X| X   X |  X X  |   X   |V',
    'X     X|X  X  X|X  X  X|X  X  X|X  X  X|X  X  X| XX XX |W',
    'X     X| X   X |  X X  |   X   |  X X  | X   X |X     X|X',
    'X     X| X   X |  X X  |   X   |   X   |   X   |   X   |Y',
    'XXXXXXX|     X |    X  |   X   |  X    | X     |XXXXXXX|Z',
    ' XXXXX | X     | X     | X     | X     | X     | XXXXX |[',
    'X      | X     |  X    |   X   |    X  |     X |      X|\\',
    ' XXXXX |     X |     X |     X |     X |     X | XXXXX |]',
    '   X   |  X X  | X   X |       |       |       |       |^',
    '       |       |       |       |       |       |XXXXXXX|_',
    '       |  XXX  |  XXX  |   X   |    X  |       |       |`',
    '       |   XX  |  X  X | X    X| XXXXXX| X    X| X    X|a',
    '       | XXXXX | X    X| XXXXX | X    X| X    X| XXXXX |b',
    '       |  XXXX | X    X| X     | X     | X    X|  XXXX |c',
    '       | XXXXX | X    X| X    X| X    X| X    X| XXXXX |d',
    '       | XXXXXX| X     | XXXXX | X     | X     | XXXXXX|e',
    '       | XXXXXX| X     | XXXXX | X     | X     | X     |f',
    '       |  XXXX | X    X| X     | X  XXX| X    X|  XXXX |g',
    '       | X    X| X    X| XXXXXX| X    X| X    X| X    X|h',
    '       |    X  |    X  |    X  |    X  |    X  |    X  |i',
    '       |      X|      X|      X|      X| X    X|  XXXX |j',
    '       | X    X| X   X | XXXX  | X  X  | X   X | X    X|k',
    '       | X     | X     | X     | X     | X     | XXXXXX|l',
    '       | X    X| XX  XX| X XX X| X    X| X    X| X    X|m',
    '       | X    X| XX   X| X X  X| X  X X| X   XX| X    X|n',
    '       |  XXXX | X    X| X    X| X    X| X    X|  XXXX |o',
    '       | XXXXX | X    X| X    X| XXXXX | X     | X     |p',
    '       |  XXXX | X    X| X    X| X  X X| X   X |  XXX X|q',
    '       | XXXXX | X    X| X    X| XXXXX | X   X | X    X|r',
    '       |  XXXX | X     |  XXXX |      X| X    X|  XXXX |s',
    '       |  XXXXX|    X  |    X  |    X  |    X  |    X  |t',
    '       | X    X| X    X| X    X| X    X| X    X|  XXXX |u',
    '       | X    X| X    X| X    X| X    X|  X  X |   XX  |v',
    '       | X    X| X    X| X    X| X XX X| XX  XX| X    X|w',
    '       | X    X|  X  X |   XX  |   XX  |  X  X | X    X|x',
    '       |  X   X|   X X |    X  |    X  |    X  |    X  |y',
    '       | XXXXXX|     X |    X  |   X   |  X    | XXXXXX|z',
    '  XXX  | X     | X     |XX     | X     | X     |  XXX  |{',
    '   X   |   X   |   X   |       |   X   |   X   |   X   ||',
    '  XXX  |     X |     X |     XX|     X |     X |  XXX  |}',
    ' XX    |X  X  X|    XX |       |       |       |       |~');

    private $letterTable = array();
    private $leds = array();
    private $textPosition = 0;
    private $rainbowIndex = 0;
    private $rainbowLength = 32;
    private $textCols = array();

    public function __construct($ipcon)
    {
        // Create lookup table from letter forms array
        foreach ($this->letterForms as $form) {
            if (strpos($form, '|') !== FALSE) {
                $this->letterTable[substr($form, -1)] = explode('|', substr($form, 0, strlen($form) - 2));
            }
        }

        $this->setNewText('Starter Kit: Blinkenlights');

        $this->okay = FALSE;
        $this->ipcon = $ipcon;

        if (!Config\UID_LED_STRIP_BRICKLET) {
            echo "Not Configured: LED Strip (required)\n";
            return;
        }

        $this->ledStrip = new BrickletLEDStrip(Config\UID_LED_STRIP_BRICKLET, $this->ipcon);

        try {
            $this->ledStrip->getFrameDuration();
            echo "Found: LED Strip (" . Config\UID_LED_STRIP_BRICKLET . ")\n";
        } catch (Exception $e) {
            echo "Not Found: LED Strip (" . Config\UID_LED_STRIP_BRICKLET . ")\n";
            return;
        }

        $this->okay = TRUE;

        $this->frameClear();

        // Set frame duration to 40ms (25 frames per second)
        $this->ledStrip->setFrameDuration(1000 / Config\TEXT_FRAME_RATE);

        // Register frame rendered callback to function cb_frame_rendered
        $this->ledStrip->registerCallback(BrickletLEDStrip::CALLBACK_FRAME_RENDERED,
                                          array($this, 'cb_frameRendered'));
    }

    // Splits text into characters and looks them up in the letter forms table
    public function setNewText($text)
    {
        $text = '   ' . $text;
        $this->textCols = array('', '', '', '', '', '', '');

        for ($col = 0; $col < count($this->textCols); $col++) {
            foreach (str_split($text) as $c) {
                $this->textCols[$col] .= $this->letterTable[$c][$col];
            }
        }
    }

    // Frame rendered callback, is called when a new frame was rendered
    public function cb_frameRendered($length)
    {
        $this->frameUpload();
        $this->framePrepareNext();
    }

    function frameClear()
    {
        for ($row = 0; $row < Config\LED_ROWS; $row++) {
            $this->leds[$row] = array();

            for ($col = 0; $col < Config\LED_COLS; $col++) {
                $this->leds[$row][$col] = array(0, 0, 0);
            }
        }
    }

    function frameUpload()
    {
        if (!$this->okay) {
            return;
        }

        $r = array();
        $g = array();
        $b = array();

        // Reorder LED data into R, G and B channel
        for ($row = 0; $row < Config\LED_ROWS; $row++) {
            if ($row % 2 == 0) {
                $colBegin = Config\LED_COLS - 1;
                $colEnd = -1;
                $colStep = -1;
            } else {
                $colBegin = 0;
                $colEnd = Config\LED_COLS;
                $colStep = 1;
            }

            for ($col = $colBegin; $col != $colEnd; $col += $colStep) {
                $r[] = $this->leds[$row][$col][Config\R_INDEX];
                $g[] = $this->leds[$row][$col][Config\G_INDEX];
                $b[] = $this->leds[$row][$col][Config\B_INDEX];
            }
        }

        // Make chunks of size 16
        for ($i = 0; $i < Config\LED_ROWS*Config\LED_COLS; $i += Text::CHUNK_SIZE) {
            $rChunk = array();
            $gChunk = array();
            $bChunk = array();

            for ($k = 0; $k < Text::CHUNK_SIZE && $i + $k < Config\LED_ROWS*Config\LED_COLS; $k++) {
                $rChunk[$k] = $r[$i + $k];
                $gChunk[$k] = $g[$i + $k];
                $bChunk[$k] = $b[$i + $k];
            }

            // Fill up chunks with zeros
            for ($j = $k; $j < Text::CHUNK_SIZE; $j++) {
                $rChunk[$j] = 0;
                $gChunk[$j] = 0;
                $bChunk[$j] = 0;
            }

            $this->ledStrip->setRGBValues($i, $k, $rChunk, $gChunk, $bChunk);
        }
    }

    function framePrepareNext()
    {
        $this->frameClear();

        if (Config\TEXT_COLOR_R == NULL) {
            $rgb = hsv2rgb(255.0*$this->rainbowIndex/$this->rainbowLength, 255, 25);
            $this->rainbowIndex = ($this->rainbowIndex + 1) % $this->rainbowLength;
        } else {
            $rgb = array(Config\TEXT_COLOR_R, Config\TEXT_COLOR_G, Config\TEXT_COLOR_B);
        }

        for ($col = 0; $col < count($this->textCols); $col++) {
            for ($row = 0; $row < Config\LED_ROWS; $row++) {
                if ($this->textCols[$col][($this->textPosition+$row) % strlen($this->textCols[0])] == 'X') {
                    $this->leds[$row][$col + 1] = $rgb;
                } else {
                    $this->leds[$row][$col + 1] = array(0, 0, 0);
                }
            }
        }

        $this->textPosition += 1;
    }
}

$ipcon = new IPConnection(); // Create IP connection
$ipcon->connect(Config\HOST, Config\PORT); // Connect to brickd

$text = new Text($ipcon);

if (isset($argv) && count($argv) > 1) {
    unset($argv[0]);
    $text->setNewText(implode(' ', $argv));
}

// Set initial rgb values to get started
$text->cb_frameRendered(0);

echo "Press ctrl+c to exit\n";
$ipcon->dispatchCallbacks(-1); // Dispatch callbacks forever

?>
