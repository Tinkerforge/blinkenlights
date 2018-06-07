using Tinkerforge;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

class TetrisSegmentDisplay
{
	private static byte[] DIGITS = new byte[] // 0~9,A,b,C,d,E,F
	{
		0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,
		0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71
	};

	private bool okay = false;
	private BrickletSegmentDisplay4x7 display = null;
	private int lineCount = 0;

	public TetrisSegmentDisplay(IPConnection ipcon)
	{
		if (Config.UID_SEGMENT_DISPLAY_4X7_BRICKLET == null)
		{
			System.Console.WriteLine("Not Configured: Segment Display 4x7");
			return;
		}

		display = new BrickletSegmentDisplay4x7(Config.UID_SEGMENT_DISPLAY_4X7_BRICKLET, ipcon);

		try
		{
			string uid;
			string connectedUid;
			char position;
			byte[] hardwareVersion;
			byte[] firmwareVersion;
			int deviceIdentifier;

			display.GetIdentity(out uid, out connectedUid, out position,
			                    out hardwareVersion, out firmwareVersion,
			                    out deviceIdentifier);
			System.Console.WriteLine("Found: Segment Display 4x7 ({0})",
			                         Config.UID_SEGMENT_DISPLAY_4X7_BRICKLET);
		}
		catch (TinkerforgeException)
		{
			System.Console.WriteLine("Not Found: Segment Display 4x7 ({0})",
			                         Config.UID_SEGMENT_DISPLAY_4X7_BRICKLET);
			return;
		}

		okay = true;

		LineCountToDisplay();
	}

	public void IncreaseLineCount(int increaseBy)
	{
		if (!okay)
		{
			return;
		}

		lineCount += increaseBy;

		LineCountToDisplay();
	}

	public void LineCountToDisplay()
	{
		if (!okay)
		{
			return;
		}

		byte[] segments = new byte[]
		{
			DIGITS[lineCount/1000 % 10],
			DIGITS[lineCount/100  % 10],
			DIGITS[lineCount/10   % 10],
			DIGITS[lineCount/1    % 10]
		};

		display.SetSegments(segments, 7, false);
	}
}

class TetrisSpeaker
{
	private bool okay = false;
	private BrickletPiezoSpeaker speaker = null;
	private Thread thread = null;

	public TetrisSpeaker(IPConnection ipcon)
	{
		if (Config.UID_PIEZO_SPEAKER_BRICKLET == null)
		{
			System.Console.WriteLine("Not Configured: Piezo Speaker");
			return;
		}

		speaker = new BrickletPiezoSpeaker(Config.UID_PIEZO_SPEAKER_BRICKLET, ipcon);

		try
		{
			string uid;
			string connectedUid;
			char position;
			byte[] hardwareVersion;
			byte[] firmwareVersion;
			int deviceIdentifier;

			speaker.GetIdentity(out uid, out connectedUid, out position,
			                    out hardwareVersion, out firmwareVersion,
			                    out deviceIdentifier);
			System.Console.WriteLine("Found: Piezo Speaker ({0})",
			                         Config.UID_PIEZO_SPEAKER_BRICKLET);
		}
		catch (TinkerforgeException)
		{
			System.Console.WriteLine("Not Found: Piezo Speaker ({0})",
			                         Config.UID_PIEZO_SPEAKER_BRICKLET);
			return;
		}

		okay = true;
	}

	public void Sirene(int freq)
	{
		if (!okay)
		{
			return;
		}

		for (int j = 0; j < 2; ++j)
		{
			for (int i = 0; i < 25; ++i)
			{
				speaker.Beep(10, freq + i * 20);
				Thread.Sleep(7);
			}

			for (int i = 0; i < 25; ++i)
			{
				speaker.Beep(10, freq + 24 * 20 - i * 20);
				Thread.Sleep(7);
			}
		}
	}

	public void BeepInput()
	{
		if (!okay)
		{
			return;
		}

		speaker.Beep(10, 500);
	}

	public void BeepDeleteLine(int lines)
	{
		if (!okay)
		{
			return;
		}

		thread = new Thread(delegate() { Sirene(1000 * lines); });
		thread.IsBackground = true;
		thread.Start();
	}
}

class Tetris
{
	// 22 rows in playfield, with only 20 columns visible and 2 coloms border
	private static int FIELD_ROWS = Config.LED_ROWS + 4;

	// 10 columns in playfield, 2 column border
	private static int FIELD_COLS = Config.LED_COLS + 2;

	private static int FIELD_ROW_START = 2;
	private static int FIELD_COL_START = 4;

	private static int CHUNK_SIZE = 16;

	private static byte[][] COLORS = new byte[][]
	{
		new byte[] { 10,  10,  10}, // grey
		new byte[] {255,   0,   0}, // red
		new byte[] {255,  80,   0}, // orange
		new byte[] {255, 255,   0}, // yellow
		new byte[] {  0, 255,   0}, // green
		new byte[] {  0,   0, 255}, // blue
		new byte[] {255,   0, 150}, // violet
		new byte[] {255,   0,  40}  // purple
	};

	private static Hashtable TETROMINOS = new Hashtable()
	{
		{
			'_',
			new byte[][][]
			{
				new byte[][] { new byte[] {0}, new byte[] {0}, new byte[] {0}, new byte[] {0} }
			}
		},
		{
			'I',
			new byte[][][]
			{
				new byte[][] { new byte[] {0,0,0,0}, new byte[] {0,0,2,0}, new byte[] {0,0,0,0}, new byte[] {0,2,0,0} },
				new byte[][] { new byte[] {2,2,2,2}, new byte[] {0,0,2,0}, new byte[] {0,0,0,0}, new byte[] {0,2,0,0} },
				new byte[][] { new byte[] {0,0,0,0}, new byte[] {0,0,2,0}, new byte[] {2,2,2,2}, new byte[] {0,2,0,0} },
				new byte[][] { new byte[] {0,0,0,0}, new byte[] {0,0,2,0}, new byte[] {0,0,0,0}, new byte[] {0,2,0,0} }
			}
		},
		{
			'J',
			new byte[][][]
			{
				new byte[][] { new byte[] {6,0,0}, new byte[] {0,6,6}, new byte[] {0,0,0}, new byte[] {0,6,0} },
				new byte[][] { new byte[] {6,6,6}, new byte[] {0,6,0}, new byte[] {6,6,6}, new byte[] {0,6,0} },
				new byte[][] { new byte[] {0,0,0}, new byte[] {0,6,0}, new byte[] {0,0,6}, new byte[] {6,6,0} }
			}
		},
		{
			'L',
			new byte[][][]
			{
				new byte[][] { new byte[] {0,0,5}, new byte[] {0,5,0}, new byte[] {0,0,0}, new byte[] {5,5,0} },
				new byte[][] { new byte[] {5,5,5}, new byte[] {0,5,0}, new byte[] {5,5,5}, new byte[] {0,5,0} },
				new byte[][] { new byte[] {0,0,0}, new byte[] {0,5,5}, new byte[] {5,0,0}, new byte[] {0,5,0} }
			}
		},
		{
			'O',
			new byte[][][]
			{
				new byte[][] { new byte[] {0,0,0,0}, new byte[] {0,0,0,0}, new byte[] {0,0,0,0}, new byte[] {0,0,0,0} },
				new byte[][] { new byte[] {0,1,1,0}, new byte[] {0,1,1,0}, new byte[] {0,1,1,0}, new byte[] {0,1,1,0} },
				new byte[][] { new byte[] {0,1,1,0}, new byte[] {0,1,1,0}, new byte[] {0,1,1,0}, new byte[] {0,1,1,0} }
			}
		},
		{
			'S',
			new byte[][][]
			{
				new byte[][] { new byte[] {0,3,3}, new byte[] {0,3,0}, new byte[] {0,0,0}, new byte[] {3,0,0} },
				new byte[][] { new byte[] {3,3,0}, new byte[] {0,3,3}, new byte[] {0,3,3}, new byte[] {3,3,0} },
				new byte[][] { new byte[] {0,0,0}, new byte[] {0,0,3}, new byte[] {3,3,0}, new byte[] {0,3,0} }
			}
		},
		{
			'T',
			new byte[][][]
			{
				new byte[][] { new byte[] {0,7,0}, new byte[] {0,7,0}, new byte[] {0,0,0}, new byte[] {0,7,0} },
				new byte[][] { new byte[] {7,7,7}, new byte[] {0,7,7}, new byte[] {7,7,7}, new byte[] {7,7,0} },
				new byte[][] { new byte[] {0,0,0}, new byte[] {0,7,0}, new byte[] {0,7,0}, new byte[] {0,7,0} }
			}
		},
		{
			'Z',
			new byte[][][]
			{
				new byte[][] { new byte[] {4,4,0}, new byte[] {0,0,4}, new byte[] {0,0,0}, new byte[] {0,4,0} },
				new byte[][] { new byte[] {0,4,4}, new byte[] {0,4,4}, new byte[] {4,4,0}, new byte[] {4,4,0} },
				new byte[][] { new byte[] {0,0,0}, new byte[] {0,4,0}, new byte[] {0,4,4}, new byte[] {4,0,0} }
			}
		}
	};

	private static string[] GAME_OVER_TEXT = new string[]
	{
		"GameOverGameOverGameOverGameOverGameOverGameOverGameOve",
		"                                                       ",
		"         GGGG                      OO                  ",
		"        G   GG                    O  O                 ",
		"        G      aaa  mmm mm   ee   O  O v   v  ee   rr  ",
		"        G  GG     a m  m  m e  e  O  O v   v e  e r  r ",
		"        G    G aaaa m  m  m eeee  O  O  v v  eeee r    ",
		"        G    G a  a m  m  m e     O  O  v v  e    r    ",
		"         GGGG  aaaa m  m  m  eee   OO    v    eee r    ",
		"                                                       ",
		"                                                       ",
		"GameOverGameOverGameOverGameOverGameOverGameOverGameOve"
	};

	private static Hashtable GAME_OVER_COLORS = new Hashtable()
	{
		{' ', 0},
		{'G', 1},
		{'a', 2},
		{'m', 3},
		{'e', 4},
		{'O', 5},
		{'v', 6},
		{'r', 7}
	};

	private BrickletLEDStrip ledStrip = null;
	private BrickletLEDStripV2 ledStripV2 = null;

	private bool okay = false;
	private bool loop = true;
	private char tetrominoCurrent = 'O';
	private int tetrominoForm = 0;
	private int tetrominoPosRow = FIELD_ROW_START;
	private int tetrominoPosCol = FIELD_COL_START;
	private Timer dropTimer = null;
	private byte[][] playfield = new byte[FIELD_ROWS][];
	private char[] randomBag = new char[] {'O', 'I', 'S', 'Z', 'L', 'J', 'T'};
	private int randomBagIndex = 0;
	private bool gameOver = false;
	private int gameOverPosition = 0;
	private KeyPress keyPress = null;
	private TetrisSpeaker speaker = null;
	private TetrisSegmentDisplay display = null;

	public Tetris(IPConnection ipcon)
	{
		for (int row = 0; row < FIELD_ROWS; ++row)
		{
			playfield[row] = new byte[FIELD_COLS];
		}

		randomBagIndex = randomBag.Length - 1;

		// Call a getter to check that the Bricklet is avialable
		if (!Config.IS_LED_STRIP_V2) {
			ledStrip = new BrickletLEDStrip(Config.UID_LED_STRIP_BRICKLET, ipcon);
		}
		else {
			ledStripV2 = new BrickletLEDStripV2(Config.UID_LED_STRIP_BRICKLET, ipcon);
		}

		try
		{
			if (!Config.IS_LED_STRIP_V2) {
				ledStrip.GetFrameDuration();
				System.Console.WriteLine("Found: LED Strip ({0})", Config.UID_LED_STRIP_BRICKLET);
			}
			else {
				ledStripV2.GetFrameDuration();
				System.Console.WriteLine("Found: LED Strip V2 ({0})", Config.UID_LED_STRIP_BRICKLET);
			}
		}
		catch (TinkerforgeException)
		{
			if (!Config.IS_LED_STRIP_V2) {
				System.Console.WriteLine("Not Found: LED Strip ({0})", Config.UID_LED_STRIP_BRICKLET);
			}
			else {
				System.Console.WriteLine("Not Found: LED Strip V2 ({0})", Config.UID_LED_STRIP_BRICKLET);
			}
			return;
		}

		keyPress = new KeyPress(ipcon);
		speaker = new TetrisSpeaker(ipcon);
		display = new TetrisSegmentDisplay(ipcon);
		okay = true;

		if (!Config.IS_LED_STRIP_V2) {
			ledStrip.SetFrameDuration(40);
			ledStrip.FrameRendered += FrameRenderedCB;
		}
		else {
			ledStripV2.SetFrameDuration(40);
			ledStripV2.FrameStartedCallback += FrameRenderedCBV2;
		}

		InitGame();
	}

	public bool IsOkay()
	{
		return okay;
	}

	private void InitGame()
	{
		tetrominoCurrent = 'O';
		tetrominoForm = 0;
		tetrominoPosRow = FIELD_ROW_START;
		tetrominoPosCol = FIELD_COL_START;

		// Add border to playfield and clear the rest
		for (int col = 0; col < FIELD_COLS; ++col)
		{
			playfield[0][col] = 255;
		}

		for (int row = 1; row < FIELD_ROWS - 1; ++row)
		{
			playfield[row][0] = 255;

			for (int col = 1; col < FIELD_COLS - 1; ++col)
			{
				playfield[row][col] = 0;
			}

			playfield[row][FIELD_COLS - 1] = 255;
		}

		for (int col = 0; col < FIELD_COLS; ++col)
		{
			playfield[FIELD_ROWS - 1][col] = 255;
		}

		// Initialize current tetronimo randomly
		tetrominoCurrent = GetRandomTetromino();
		gameOver = false;

		if (dropTimer != null)
		{
			dropTimer.Change(1000, 1000);
		}
	}

	private void FrameRenderedCB(BrickletLEDStrip sender, int length)
	{
		WritePlayfield();
	}

	private void FrameRenderedCBV2(BrickletLEDStripV2 sender, int length)
	{
		WritePlayfield();
	}

	private static System.Random random = new System.Random();

	// http://en.wikipedia.org/wiki/Fisher-Yates_shuffle
	private static void Shuffle<T> (T[] array)
	{
		for (int i = array.Length - 1; i > 0; --i)
		{
			int k = random.Next(i + 1);
			T temp = array[i];

			array[i] = array[k];
			array[k] = temp;
		}
	}

	// See http://tetris.wikia.com/wiki/Random_Generator for
	// details of random bag implementation according to tetris specification
	private char GetRandomTetromino()
	{
		randomBagIndex += 1;

		if (randomBagIndex >= randomBag.Length)
		{
			randomBagIndex = 0;

			Shuffle(randomBag);
		}

		return randomBag[randomBagIndex];
	}

	private void AddTetrominoToField(byte[][] field, int posRow, int posCol, char tetromino, int form)
	{
		byte[][][] tetrominoData = (byte[][][])TETROMINOS[tetromino];

		for (int indexCol = 0; indexCol < tetrominoData.Length; ++indexCol)
		{
			for (int indexRow = 0; indexRow < tetrominoData[indexCol][form].Length; ++indexRow)
			{
				byte color = tetrominoData[indexCol][form][indexRow];

				if (color != 0)
				{
					int row = posRow + indexRow;
					int col = posCol + indexCol;

					if (row >= 0 && row < FIELD_ROWS && col >= 0 && col < FIELD_COLS)
					{
						field[row][col] = color;
					}
				}
			}
		}
	}

	private bool TetrominoFits(byte[][] field, int posRow, int posCol, char tetromino, int form)
	{
		byte[][][] tetrominoData = (byte[][][])TETROMINOS[tetromino];

		for (int indexCol = 0; indexCol < tetrominoData.Length; ++indexCol)
		{
			for (int indexRow = 0; indexRow < tetrominoData[indexCol][form].Length; ++indexRow)
			{
				byte color = tetrominoData[indexCol][form][indexRow];

				if (color != 0)
				{
					int row = posRow + indexRow;
					int col = posCol + indexCol;

					if (row >= 0 && row < FIELD_ROWS && col >= 0 && col < FIELD_COLS)
					{
						if (field[row][col] != 0)
						{
							return false;
						}
					}
				}
			}
		}

		return true;
	}

	private static T DeepCopy<T>(T obj)
	{
		MemoryStream stream = new MemoryStream();
		BinaryFormatter formatter = new BinaryFormatter();

		formatter.Serialize(stream, obj);
		stream.Position = 0;

		return (T)formatter.Deserialize(stream);
	}

	private void WritePlayfield()
	{
		int j = 0;

		if (!okay)
		{
			return;
		}

		byte[][] field = DeepCopy(playfield);

		if (!gameOver)
		{
			AddTetrominoToField(field, tetrominoPosRow, tetrominoPosCol,
			                    tetrominoCurrent, tetrominoForm);
		}

		// Reorder LED data into R, G and B channel
		byte[] r = new byte[Config.LED_ROWS * Config.LED_COLS];
		byte[] g = new byte[Config.LED_ROWS * Config.LED_COLS];
		byte[] b = new byte[Config.LED_ROWS * Config.LED_COLS];
		byte[] frame = new byte[Config.LED_ROWS * Config.LED_COLS * 3];

		for (int row = FIELD_ROWS - 2, i = 0; row > 2; --row)
		{
			int colBegin;
			int colEnd;
			int colStep;

			if (row % 2 == 0)
			{
				colBegin = FIELD_COLS - 2;
				colEnd = 0;
				colStep = -1;
			}
			else
			{
				colBegin = 1;
				colEnd = FIELD_COLS - 1;
				colStep = 1;
			}

			for (int col = colBegin; col != colEnd; col += colStep, ++i)
			{
				j = i * 3;

				r[i] = COLORS[field[row][col]][Config.R_INDEX];
				g[i] = COLORS[field[row][col]][Config.G_INDEX];
				b[i] = COLORS[field[row][col]][Config.B_INDEX];
				frame[j] = COLORS[field[row][col]][Config.R_INDEX];
				j++;
				frame[j] = COLORS[field[row][col]][Config.G_INDEX];
				j++;
				frame[j] = COLORS[field[row][col]][Config.B_INDEX];
			}
		}

		if (!Config.IS_LED_STRIP_V2) {
			// Make chunks of size 16
			byte[] rChunk = new byte[CHUNK_SIZE];
			byte[] gChunk = new byte[CHUNK_SIZE];
			byte[] bChunk = new byte[CHUNK_SIZE];

			for (int i = 0; i < Config.LED_ROWS * Config.LED_COLS; i += CHUNK_SIZE)
			{
				byte k;

				for (k = 0; k < CHUNK_SIZE && i + k < Config.LED_ROWS * Config.LED_COLS; ++k)
				{
					rChunk[k] = r[i + k];
					gChunk[k] = g[i + k];
					bChunk[k] = b[i + k];
				}

				try
				{
					ledStrip.SetRGBValues(i, k, rChunk, gChunk, bChunk);
				}
				catch (TinkerforgeException)
				{
					break;
				}
			}
		}
		else {
			ledStripV2.SetLEDValues(0, frame);
		}
	}

	private void ClearLines(List<int> rowsToClear)
	{
		if (!okay)
		{
			return;
		}

		dropTimer.Change(Timeout.Infinite, Timeout.Infinite);

		Hashtable rowsSave = new Hashtable();

		foreach (int toClear in rowsToClear)
		{
			rowsSave[toClear] = playfield[toClear];
		}

		display.IncreaseLineCount(rowsToClear.Count);
		speaker.BeepDeleteLine(rowsToClear.Count);

		byte[] clearedRow = new byte[FIELD_COLS];

		clearedRow[0] = 255;
		clearedRow[FIELD_COLS - 1] = 255;

		for (int i = 1; i < FIELD_COLS - 1; ++i)
		{
			clearedRow[i] = 0;
		}

		for (int i = 0; i < 6; ++i)
		{
			if (i % 2 == 0)
			{
				foreach (int toClear in rowsToClear)
				{
					playfield[toClear] = DeepCopy(clearedRow);
				}
			}
			else
			{
				foreach (int toClear in rowsToClear)
				{
					playfield[toClear] = (byte[])rowsSave[toClear];
				}
			}

			Thread.Sleep(100);
		}

		foreach (int toClear in rowsToClear)
		{
			for (int row = toClear; row > 0; --row)
			{
				playfield[row] = playfield[row - 1];
			}

			playfield[1] = DeepCopy(clearedRow);
		}

		dropTimer.Change(1000, 1000);
	}

	private void CheckForLinesToClear()
	{
		List<int> rowsToClear = new List<int>();

		for (int row = 1; row < playfield.Length - 1; ++row)
		{
			bool toClear = true;

			for (int col = 1; col < playfield[row].Length - 1; ++col)
			{
				if (playfield[row][col] == 0)
				{
					toClear = false;
					break;
				}
			}

			if (toClear)
			{
				rowsToClear.Add(row);
			}
		}

		if (rowsToClear.Count > 0)
		{
			ClearLines(rowsToClear);
		}
	}

	private void NewTetromino()
	{
		AddTetrominoToField(playfield, tetrominoPosRow, tetrominoPosCol,
		                    tetrominoCurrent, tetrominoForm);
		tetrominoCurrent = '_';

		CheckForLinesToClear();

		tetrominoCurrent = GetRandomTetromino();
		tetrominoPosRow = FIELD_ROW_START;
		tetrominoPosCol = FIELD_COL_START;
		tetrominoForm = 0;

		if (!TetrominoFits(playfield, tetrominoPosRow, tetrominoPosCol,
		                   tetrominoCurrent, tetrominoForm))
		{
			gameOver = true;
			gameOverPosition = 0;
			dropTimer.Change(150, 150);
		}
	}

	private void NextGameOverStep()
	{
		for (int row = 0; row < GAME_OVER_TEXT.Length; ++row)
		{
			for (int col = 0; col < Config.LED_COLS; ++col)
			{
				int k = (gameOverPosition + col) % GAME_OVER_TEXT[0].Length;
				playfield[7 + row][1 + col] = (byte)(int)GAME_OVER_COLORS[GAME_OVER_TEXT[row][k]];
			}
		}

		gameOverPosition += 1;
	}

	private void DropTetromino()
	{
		if (gameOver)
		{
			NextGameOverStep();
			return;
		}

		if (TetrominoFits(playfield, tetrominoPosRow + 1,
		                  tetrominoPosCol, tetrominoCurrent,
		                  tetrominoForm))
		{
			tetrominoPosRow += 1;
		}
		else
		{
			NewTetromino();
		}
	}

	private void MoveTetromino(int row, int col, int form)
	{
		if (gameOver)
		{
			return;
		}

		if (TetrominoFits(playfield, tetrominoPosRow + row, tetrominoPosCol + col,
		                  tetrominoCurrent, form))
		{
			tetrominoPosRow += row;
			tetrominoPosCol += col;
			tetrominoForm = form;

			if (row > 0)
			{
				// restart drop timer, so we don't drop two tetrominos in a row
				dropTimer.Change(1000, 1000);
			}
		}
		else if (row == 1) // user is at bottom and hits button to go down again
		{
			NewTetromino();
		}
	}

	private static int PositiveMod(int value, int modulus)
	{
		return ((value % modulus) + modulus) % modulus;
	}

	public void RunGameLoop()
	{
		if (!Config.IS_LED_STRIP_V2) {
			FrameRenderedCB(ledStrip, 0);
		}
		else {
			FrameRenderedCBV2(ledStripV2, 0);
		}

		dropTimer = new Timer(delegate(object state) { DropTetromino(); }, null, 1000, 1000);

		while (loop)
		{
			char key = keyPress.ReadSingleKeypress();

			switch (key)
			{
			case 'a':
				speaker.BeepInput();
				MoveTetromino(0, -1, tetrominoForm);
				break;

			case 'd':
				speaker.BeepInput();
				MoveTetromino(0, 1, tetrominoForm);
				break;

			case 's':
				speaker.BeepInput();
				MoveTetromino(1, 0, tetrominoForm);
				break;

			case 'k':
				speaker.BeepInput();
				MoveTetromino(0, 0, PositiveMod(tetrominoForm - 1, 4));
				break;

			case 'l':
				speaker.BeepInput();
				MoveTetromino(0, 0, PositiveMod(tetrominoForm + 1, 4));
				break;

			case 'r':
				InitGame();
				break;

			case 'q':
				loop = false;
				break;
			}
		}

		if (!Config.IS_LED_STRIP_V2) {
			ledStrip.FrameRendered -= FrameRenderedCB;
		}
		else {
			ledStripV2.FrameStartedCallback -= FrameRenderedCBV2;
		}

		dropTimer.Change(Timeout.Infinite, Timeout.Infinite);
	}

	private static Tetris tetris;

	static void Main()
	{
		// Create IP Connection and connect it
		IPConnection ipcon = new IPConnection();
		ipcon.Connect(Config.HOST, Config.PORT);

		// Create Tetris object and start game loop
		tetris = new Tetris(ipcon);

		if (tetris.IsOkay()) {
			System.Console.WriteLine("Press q to exit");
			tetris.RunGameLoop();
		}

		ipcon.Disconnect();
	}
}
