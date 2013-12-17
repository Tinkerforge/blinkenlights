#include <stdio.h>

#include "ip_connection.h"
#include "bricklet_led_strip.h"
#include "config.h"

uint8_t leds[LED_ROWS*LED_COLS][3] = {{0}};
uint8_t rainbow[LED_ROWS*LED_COLS][3] = {{0}};
float rainbow_position = 0;

// based on http://web.mit.edu/storborg/Public/hsvtorgb.c
void hsv_to_rgb(uint8_t h, uint8_t s, uint8_t v, uint8_t *r, uint8_t *g, uint8_t *b) {
	uint8_t region, fpart, p, q, t;

	if(s == 0) {
		// color is grayscale
		*r = *g = *b = v;
		return;
	}

	// make hue 0-5
	region = h / 43;

	// find remainder part, make it from 0-255
	fpart = (h - (region * 43)) * 6;

	// calculate temp vars, doing integer multiplication
	p = (v * (255 - s)) >> 8;
	q = (v * (255 - ((s * fpart) >> 8))) >> 8;
	t = (v * (255 - ((s * (255 - fpart)) >> 8))) >> 8;

	// assign temp vars based on color cone region
	switch(region) {
	case 0:  *r = v; *g = t; *b = p; break;
	case 1:  *r = q; *g = v; *b = p; break;
	case 2:  *r = p; *g = v; *b = t; break;
	case 3:  *r = p; *g = q; *b = v; break;
	case 4:  *r = t; *g = p; *b = v; break;
	default: *r = v; *g = p; *b = q; break;
	}
}

void frame_upload(LEDStrip *led_strip) {
	#define CHUNK_SIZE 16

	uint8_t r_chunk[CHUNK_SIZE];
	uint8_t g_chunk[CHUNK_SIZE];
	uint8_t b_chunk[CHUNK_SIZE];
	int i, k;

	for(i = 0; i < LED_ROWS*LED_COLS; i += CHUNK_SIZE) {
		for(k = 0; k < CHUNK_SIZE && i + k < LED_ROWS*LED_COLS; ++k) {
			r_chunk[k] = leds[i + k][R_INDEX];
			g_chunk[k] = leds[i + k][G_INDEX];
			b_chunk[k] = leds[i + k][B_INDEX];
		}

		if (led_strip_set_rgb_values(led_strip, i, k, r_chunk, g_chunk, b_chunk) < 0) {
			break;
		}
	}
}

void frame_prepare_next(void) {
	int offset = (int)rainbow_position % (LED_ROWS*LED_COLS);
	int count = LED_ROWS*LED_COLS - offset;

	memcpy(leds, &rainbow[offset], count * 3);
	memcpy(&leds[count], rainbow, offset * 3);

	rainbow_position += (LED_ROWS*LED_COLS) * RAINBOW_SPEED / 4.0;
}

// Frame rendered callback, is called when a new frame was rendered
void cb_frame_rendered(uint16_t length, void *user_data) {
	(void)length; // avoid unused parameter warning

	LEDStrip *led_strip = (LEDStrip *)user_data;

	frame_upload(led_strip);
	frame_prepare_next();
}

int main(void) {
	// Create IP connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Create device object
	LEDStrip led_strip;
	led_strip_create(&led_strip, UID_LED_STRIP_BRICKLET, &ipcon);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
		fprintf(stderr, "Could not connect\n");
		exit(1);
	}
	// Don't use device before ipcon is connected

	// Call a getter to check that the Bricklet is avialable
	uint16_t frame_duration;
	if(led_strip_get_frame_duration(&led_strip, &frame_duration) < 0) {
		fprintf(stderr, "Not Found: LED Strip (%s)\n", UID_LED_STRIP_BRICKLET);
		exit(1);
	}

	printf("Found: LED Strip (%s)\n", UID_LED_STRIP_BRICKLET);

	// Set frame duration to 20ms (50 frames per second)
	led_strip_set_frame_duration(&led_strip, 1000 / RAINBOW_FRAME_RATE);

	// Register frame rendered callback to function cb_frame_rendered
	led_strip_register_callback(&led_strip,
	                            LED_STRIP_CALLBACK_FRAME_RENDERED,
	                            (void *)cb_frame_rendered,
	                            (void *)&led_strip);

	int i;
	for(i = 0; i < LED_ROWS*LED_COLS; ++i) {
		hsv_to_rgb(255 * i / (LED_ROWS*LED_COLS), 255, 25, &rainbow[i][0], &rainbow[i][1], &rainbow[i][2]);
	}

	// Set initial rgb values to get started
	cb_frame_rendered(0, (void *)&led_strip);

	printf("Press key to exit\n");
	getchar();
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
}
