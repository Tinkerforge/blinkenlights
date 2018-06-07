unit Config;

{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

interface

const
  { General }
  HOST = 'localhost';
  PORT = 4223;

  { Bricklet }
  UID_LED_STRIP_BRICKLET = 'Fjy'; { Change to your UID }

  {Set this to True if LEDStripV2 Bricklet is used }
  IS_LED_STRIP_V2 = true;

  { Size of LED Pixel matrix }
  LED_ROWS = 20;
  LED_COLS = 10;

  { Position of R, G and B pixel on LED Pixel }
  R_INDEX = 0;
  G_INDEX = 1;
  B_INDEX = 2;

  { Fire Parameters }
  FIRE_FRAME_RATE = 50; { in Hz, valid range: 10 - 100 }
  FIRE_HUE_FACTOR = 1.2; { valid range: 0.1 - 5.0 }
  FIRE_RAND_VALUE_START = 64; { valid range: 0 - 255 }
  FIRE_RAND_VALUE_END = 255; { valid range: 1 - 255 }

implementation

end.
