public class Config {
	// General
	public static final String HOST = "localhost";
	public static final int PORT = 4223;

	// Bricklet
	public static final String UID_LED_STRIP_BRICKLET = "Fjy";

	// Set this to True if LEDStripV2 Bricklet is used
	public static final boolean IS_LED_STRIP_V2 = true;

	// Size of LED Pixel matrix
	public static final int LED_ROWS = 20;
	public static final int LED_COLS = 10;

	// Position of R, G and B pixel on LED Pixel
	public static final int R_INDEX = 0;
	public static final int G_INDEX = 1;
	public static final int B_INDEX = 2;

	// Images Parameters
	public static final int IMAGES_FRAME_RATE = 1; // in Hz, valid range: 1 - 100
}
