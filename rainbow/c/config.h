#ifndef CONFIG_H
#define CONFIG_H

// General
#define HOST "localhost"
#define PORT 4223

// Bricklet
#define UID_LED_STRIP_BRICKLET "Fjy"

// Set this to 1 is LEDStripV2 Bricklet is used
#define IS_LED_STRIP_V2 1

// Size of LED Pixel matrix
#define LED_ROWS 20
#define LED_COLS 10

// Position of R, G and B pixel on LED Pixel
#define R_INDEX 0
#define G_INDEX 1
#define B_INDEX 2

// Rainbow Parameters
#define RAINBOW_FRAME_RATE 50 // in Hz, valid range: 10 - 100
#define RAINBOW_STEP 0.002 // valid range: 0.0 - 1.0

#endif // CONFIG_H
