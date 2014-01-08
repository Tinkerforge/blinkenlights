program Fire;

{$ifdef MSWINDOWS}{$apptype CONSOLE}{$endif}
{$ifdef FPC}{$mode OBJFPC}{$H+}{$endif}

uses
  SysUtils, Math, Config, IPConnection, BrickletLEDStrip;

const
  CHUNK_SIZE = 16;
  FIRE_VALUES : array [0..9, 0..19] of byte =
  (
    ( 32,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,  32),
    ( 64,  32,  16,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  16,  32,  64),
    ( 96,  64,  32,  32,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,  32,  32,  64,  96),
    (128,  96,  64,  64,  32,  32,   0,   0,   0,   0,   0,   0,   0,   0,  32,  32,  64,  64,  96, 128),
    (160, 128,  96,  96,  64,  64,  32,  32,   0,   0,   0,   0,  32,  32,  64,  64,  96,  96, 128, 160),
    (192, 160, 128, 128,  96,  96,  64,  64,  32,   0,   0,  32,  64,  64,  96,  96, 128, 128, 160, 192),
    (255, 192, 160, 160, 128, 128,  96,  96,  64,  32,  32,  64,  96,  96, 128, 128, 160, 160, 192, 255),
    (255, 255, 192, 192, 160, 160, 128, 128,  96,  64,  64,  96, 128, 128, 160, 160, 192, 192, 255, 255),
    (255, 255, 255, 255, 192, 192, 160, 160, 128,  96,  96, 128, 160, 160, 192, 192, 255, 255, 255, 255),
    (255, 255, 255, 255, 255, 255, 192, 192, 160, 128, 128, 160, 192, 192, 255, 255, 255, 255, 255, 255)
  );
  FIRE_HUES : array [0..9, 0..19] of byte =
  (
    (1, 3, 4, 5, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 8, 8, 6, 4, 3, 1),
    (1, 2, 3, 3, 5, 6, 7, 7, 8, 8, 8, 8, 9, 9, 8, 7, 5, 3, 2, 1),
    (1, 2, 3, 3, 5, 5, 6, 6, 5, 6, 6, 7, 7, 7, 6, 6, 4, 3, 2, 1),
    (1, 1, 2, 3, 4, 4, 5, 5, 4, 4, 5, 5, 6, 5, 5, 5, 3, 2, 1, 1),
    (1, 1, 2, 2, 4, 4, 4, 4, 4, 4, 5, 5, 4, 4, 4, 4, 2, 2, 1, 1),
    (0, 0, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0),
    (0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
  );

type
  TFire = class
  private
    ipcon: TIPConnection;
    ledStrip: TBrickletLEDStrip;
    line: array [0..(LED_ROWS - 1)] of integer;
    matrix: array [0..(LED_ROWS - 1), 0..(LED_COLS - 1)] of integer;
    leds: array [0..(LED_ROWS - 1), 0..(LED_COLS - 1), 0..2] of byte;
    percent: integer;
  public
    constructor Create;
    procedure HSV2RGB(const h, s, v: byte; out r, g, b: byte);
    function Interpolate2(const x, y: integer): integer;
    function Interpolate1(const x: integer): integer;
    procedure FrameRenderedCB(sender: TBrickletLEDStrip; const length: word);
    procedure FrameUpload;
    procedure FramePrepareNext;
    procedure Execute;
  end;

var
  e: TFire;

constructor TFire.Create;
begin

  inherited Create;
end;

{ Based on http://web.mit.edu/storborg/Public/hsvtorgb.c }
procedure TFire.HSV2RGB(const h, s, v: byte; out r, g, b: byte);
var region, fpart, p, q, t: byte;
begin
  if (s = 0) then begin
    { Color is grayscale }
    r := v;
    g := v;
    b := v;
  end
  else begin
    { Make hue 0-5 }
    region := Floor(h / 43);

    { Find remainder part, make it from 0-255 }
    fpart := (h - (region * 43)) * 6;

    { Calculate temp vars, doing integer multiplication }
    p := (v * (255 - s)) shr 8;
    q := (v * (255 - ((s * fpart) shr 8))) shr 8;
    t := (v * (255 - ((s * (255 - fpart)) shr 8))) shr 8;

    { Assign temp vars based on color cone region }
    case (region) of
    0: begin   r := v; g := t; b := p; end;
    1: begin   r := q; g := v; b := p; end;
    2: begin   r := p; g := v; b := t; end;
    3: begin   r := p; g := q; b := v; end;
    4: begin   r := t; g := p; b := v; end;
    else begin r := v; g := p; b := q; end;
    end;
  end;
end;

function TFire.Interpolate2(const x, y: integer): integer;
var p0, p1, m0, m1: integer;
begin
  p0 := 100 - percent;
  p1 := percent;
  m0 := matrix[x, y];
  m1 := matrix[x, y - 1];

  result := Floor((p0 * m0 + p1 * m1) / 100);
end;

function TFire.Interpolate1(const x: integer): integer;
var p0, p1, m0, m1: integer;
begin
  p0 := 100 - percent;
  p1 := percent;
  m0 := matrix[x, 0];
  m1 := line[x];

  result := Floor((p0*m0 + p1*m1) / 100);
end;

procedure TFire.FrameRenderedCB(sender: TBrickletLEDStrip; const length: word);
begin
  FrameUpload;
  FramePrepareNext;
end;

procedure TFire.FrameUpload;
var r, g, b: array [0..(LED_ROWS * LED_COLS - 1)] of byte;
    rChunk, gChunk, bChunk: array [0..(CHUNK_SIZE - 1)] of byte;
    row, col, colBegin, colEnd, colStep, i, k: integer;
begin
  { Reorder LED data into R, G and B channel }
  i := 0;
  for row := 0 to (LED_ROWS - 1) do begin
    if (row mod 2 = 0) then begin
      colBegin := LED_COLS - 1;
      colEnd := -1;
      colStep := -1;
    end
    else begin
      colBegin := 0;
      colEnd := LED_COLS;
      colStep := 1;
    end;

    col := colBegin;
    while (col <> colEnd) do begin
      r[i] := leds[row, col, R_INDEX];
      g[i] := leds[row, col, G_INDEX];
      b[i] := leds[row, col, B_INDEX];
      i += 1;
      col += colStep;
    end;
  end;

  { Make chunks of size 16 }
  i := 0;
  while (i < LED_ROWS * LED_COLS) do begin
    k := 0;
    while ((k < CHUNK_SIZE) and (i + k < LED_ROWS * LED_COLS)) do begin
      rChunk[k] := r[i + k];
      gChunk[k] := g[i + k];
      bChunk[k] := b[i + k];
      k += 1;
    end;

    try
      ledStrip.SetRGBValues(i, k, rChunk, gChunk, bChunk);
    except
      exit;
    end;

    i += CHUNK_SIZE;
  end;
end;

procedure TFire.FramePrepareNext;
var x, y, start: integer; r, g, b: byte;
begin
  percent += 20;
  if (percent >= 100) then begin
    { Shift up }
    for y := (LED_COLS - 1) downto 1 do begin
      for x := 0 to (LED_ROWS - 1) do begin
        matrix[x, y] := matrix[x, y - 1]
      end;
    end;
    for x := 0 to (LED_ROWS - 1) do begin
      matrix[x, 0] := line[x]
    end;

    { Generate_line }
    start := Min(FIRE_RAND_VALUE_START, FIRE_RAND_VALUE_END);
    for x := 0 to (LED_ROWS - 1) do begin
      line[x] := start + Random(FIRE_RAND_VALUE_END - start);
    end;

    percent := 0;
  end;

  { Make frame }
  for y := (LED_COLS - 1) downto 1 do begin
    for x := 0 to (LED_ROWS - 1) do begin
      HSV2RGB(Floor(FIRE_HUES[y][x] * FIRE_HUE_FACTOR), 255,
              Max(0, Interpolate2(x, y) - FIRE_VALUES[y, x]), r, g, b);
      leds[x, LED_COLS-1-y, 0] := r;
      leds[x, LED_COLS-1-y, 1] := g;
      leds[x, LED_COLS-1-y, 2] := b;
    end;
  end;
  for x := 0 to (LED_ROWS - 1) do begin
    HSV2RGB(Floor(FIRE_HUES[0][x] * FIRE_HUE_FACTOR), 255,
            Max(0, Interpolate1(x)), r, g, b);
    leds[x, LED_COLS-1, 0] := r;
    leds[x, LED_COLS-1, 1] := g;
    leds[x, LED_COLS-1, 2] := b;
  end;
end;

procedure TFire.Execute;
begin
  { Create IP Connection and connect it }
  ipcon := TIPConnection.Create;
  ipcon.Connect(HOST, PORT);

  { Call a getter to check that the Bricklet is avialable }
  ledStrip := TBrickletLEDStrip.Create(UID_LED_STRIP_BRICKLET, ipcon);

  try
    ledStrip.GetFrameDuration;
    WriteLn(Format('Found: LED Strip %s', [UID_LED_STRIP_BRICKLET]));
  except
    WriteLn(Format('Not Found: LED Strip %s', [UID_LED_STRIP_BRICKLET]));
    exit;
  end;

  ledStrip.SetFrameDuration(Floor(1000 / FIRE_FRAME_RATE));

  { Register frame rendered callback to function FrameRenderedCB }
  ledStrip.OnFrameRendered := {$ifdef FPC}@{$endif}FrameRenderedCB;

  { Start rendering }
  FrameRenderedCB(ledStrip, 0);

  WriteLn('Press key to exit');
  ReadLn;
  ipcon.Destroy; { Calls ipcon.Disconnect internally }
end;

begin
  e := TFire.Create;
  e.Execute;
  e.Destroy;
end.
