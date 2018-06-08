using System.Collections;
using Tinkerforge;

class Config
{
	// General
	public static string HOST = "localhost";
	public static int PORT = 4223;

	// Required Bricklets
	public static string UID_LED_STRIP_BRICKLET = "Fjy";

	// Optional Bricklets (use null as UID if not connected)
	public static string UID_MULTI_TOUCH_BRICKLET = null;//"itS";
	public static string[] UID_DUAL_BUTTON_BRICKLET = new string[] {null, null};//new string[] {"zgh", "j2M"};
	public static string UID_SEGMENT_DISPLAY_4X7_BRICKLET = null;//"ioiu";
	public static string UID_PIEZO_SPEAKER_BRICKLET = null;//"XYZ";

	// Set this to True if LEDStripV2 Bricklet is used
	public static bool IS_LED_STRIP_V2 = true;

	// Size of LED Pixel matrix
	public static int LED_ROWS = 20;
	public static int LED_COLS = 10;

	// Position of R, G and B pixel on LED Pixel
	public static byte CHANNEL_MAPPING = BrickletLEDStrip.CHANNEL_MAPPING_RGB;

	// Pong Parameters
	public static byte[] PONG_COLOR_INDEX_PLAYER = new byte[] {1, 5};
	public static byte PONG_COLOR_INDEX_BALL = 4;

	// Keymaps
	public static Hashtable KEYMAP_MULTI_TOUCH = new Hashtable()
	{
		{0, 'a'},
		{1, 's'},
		{2, 'd'},
		{3, 'k'},
		{4, 'l'},
		{5, 'q'}
	};

	public static Hashtable KEYMAP_DUAL_BUTTON = new Hashtable()
	{
		{0, 'a'},
		{1, 's'},
		{2, 'k'},
		{3, 'l'}
	};
}
