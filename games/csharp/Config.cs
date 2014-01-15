using System.Collections;

class Config
{
	// General
	public static string HOST = "localhost";
	public static int PORT = 4223;

	// Required Bricklets
	public static string UID_LED_STRIP_BRICKLET = "abc";

	// Optional Bricklets (use null as UID if not connected)
	public static string UID_MULTI_TOUCH_BRICKLET = "itS";
	public static string[] UID_DUAL_BUTTON_BRICKLET = new string[] {"dbb", null};
	public static string UID_SEGMENT_DISPLAY_4X7_BRICKLET = "ioiu";
	public static string UID_PIEZO_SPEAKER_BRICKLET = "XYZ";

	// Size of LED Pixel matrix
	public static int LED_ROWS = 20;
	public static int LED_COLS = 10;

	// Position of R, G and B pixel on LED Pixel
	public static int R_INDEX = 2;
	public static int G_INDEX = 1;
	public static int B_INDEX = 0;

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
