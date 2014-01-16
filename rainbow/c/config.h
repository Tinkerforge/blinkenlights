#ifndef CONFIG_H
#define CONFIG_H

// General
#define HOST "localhost"
#define PORT 4223

// Bricklet
#define UID_LED_STRIP_BRICKLET "abc"

// Size of LED Pixel matrix
#define LED_ROWS 20
#define LED_COLS 10

// Position of R, G and B pixel on LED Pixel
#define R_INDEX 2
#define G_INDEX 1
#define B_INDEX 0

// Rainbow Parameters
#define RAINBOW_FRAME_RATE 50 // in Hz, valid range: 10 - 100
#define RAINBOW_STEP 0.002 // valid range: 0.0 - 1.0

#endif // CONFIG_H
