#ifndef CONFIG_H
#define CONFIG_H

#include "bricklet_led_strip.h"

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
#define CHANNEL_MAPPING LED_STRIP_CHANNEL_MAPPING_RGB

// Rainbow Parameters
#define RAINBOW_FRAME_RATE 50 // in Hz, valid range: 10 - 100
#define RAINBOW_STEP 0.002 // valid range: 0.0 - 1.0

#endif // CONFIG_H
