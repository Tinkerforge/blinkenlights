using Tinkerforge;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization.Formatters.Binary;
using System.IO;

class PongSpeaker
{
	private bool okay = false;
	private BrickletPiezoSpeaker speaker = null;
	private Thread thread = null;

	public PongSpeaker(IPConnection ipcon)
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

	public void BeepPaddleHit()
	{
		if (!okay)
		{
			return;
		}

		speaker.Beep(100, 500);
	}

	public void BeepSirene()
	{
		if (!okay)
		{
			return;
		}

		thread = new Thread(delegate() { Sirene(1000); });
		thread.IsBackground = true;
		thread.Start();
	}
}

class Pong
{
	private static int PADDLE_SIZE = 3;
	private static int CHUNK_SIZE = 16;

	private static byte[][] COLORS = new byte[][]
	{
		new byte[] {  0,   0,   0}, // off
//		new byte[] { 10,  10,  10}, // grey
		new byte[] {255,   0,   0}, // red
		new byte[] {255,  80,   0}, // orange
		new byte[] {255, 255,   0}, // yellow
		new byte[] {  0, 255,   0}, // green
		new byte[] {  0,   0, 255}, // blue
		new byte[] {255,   0, 150}, // violet
		new byte[] {255,   0,  40}, // purple
	};

	private static byte[][][] SCORE_FONT = new byte[][][]
	{
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {0, 2, 0},
		               new byte[] {0, 2, 0},
		               new byte[] {0, 2, 0},
		               new byte[] {0, 2, 0},
		               new byte[] {0, 2, 0}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {2, 2, 2},
		               new byte[] {2, 0, 0},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {2, 0, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {0, 0, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {2, 0, 0},
		               new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {2, 0, 0},
		               new byte[] {2, 2, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {0, 0, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2}},
		new byte[][] { new byte[] {2, 2, 2},
		               new byte[] {2, 0, 2},
		               new byte[] {2, 2, 2},
		               new byte[] {0, 0, 2},
		               new byte[] {0, 0, 2}}
	};

	private BrickletLEDStrip ledStrip = null;
	private bool okay = false;
	private bool loop = true;
	private Timer timer = null;
	private byte[][] playfield = new byte[Config.LED_ROWS][];
	private int[] score = new int[] {0, 0};
	private int[] paddlePositionX = new int[] {4, 15};
	private int[] paddlePositionY = new int[] {3, 3};
	private double[] ballPosition = new double[] {10, 5};
	private double[] ballDirection = new double[] {0.1, 0.2};
	private KeyPress keyPress = null;
	private PongSpeaker speaker = null;

	public Pong(IPConnection ipcon)
	{
		for (int row = 0; row < Config.LED_ROWS; ++row)
		{
			playfield[row] = new byte[Config.LED_COLS];
		}

		// Call a getter to check that the Bricklet is avialable
		ledStrip = new BrickletLEDStrip(Config.UID_LED_STRIP_BRICKLET, ipcon);

		try
		{
			ledStrip.GetFrameDuration();
			System.Console.WriteLine("Found: LED Strip ({0})", Config.UID_LED_STRIP_BRICKLET);
		}
		catch (TinkerforgeException)
		{
			System.Console.WriteLine("Not Found: LED Strip ({0})", Config.UID_LED_STRIP_BRICKLET);
			return;
		}

		keyPress = new KeyPress(ipcon);
		speaker = new PongSpeaker(ipcon);
		okay = true;

		ledStrip.SetFrameDuration(40);
		ledStrip.FrameRendered += FrameRenderedCB;

		InitGame();
	}

	public bool IsOkay()
	{
		return okay;
	}

	private void InitGame()
	{
		NewBall();

		paddlePositionY[0] = 3;
		paddlePositionY[1] = 3;
		score[0] = 0;
		score[1] = 0;
	}

	private void FrameRenderedCB(BrickletLEDStrip sender, int length)
	{
		WritePlayfield();
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
		if (!okay)
		{
			return;
		}

		byte[][] field = DeepCopy(playfield);

		AddScoreToPlayfield(field);
		AddPaddlesToPlayfield(field);
		AddBallToPlayfield(field);

		// Reorder LED data into R, G and B channel
		byte[] r = new byte[Config.LED_ROWS * Config.LED_COLS];
		byte[] g = new byte[Config.LED_ROWS * Config.LED_COLS];
		byte[] b = new byte[Config.LED_ROWS * Config.LED_COLS];

		for (int row = 0, i = 0; row < Config.LED_ROWS; ++row)
		{
			int colBegin;
			int colEnd;
			int colStep;

			if (row % 2 == 0)
			{
				colBegin = Config.LED_COLS - 1;
				colEnd = -1;
				colStep = -1;
			}
			else
			{
				colBegin = 0;
				colEnd = Config.LED_COLS;
				colStep = 1;
			}

			for (int col = colBegin; col != colEnd; col += colStep, ++i)
			{
				r[i] = COLORS[field[row][col]][Config.R_INDEX];
				g[i] = COLORS[field[row][col]][Config.G_INDEX];
				b[i] = COLORS[field[row][col]][Config.B_INDEX];
			}
		}

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

	private void AddScoreToPlayfield(byte[][] field)
	{
		for (int row = 0; row < 3; ++row)
		{
			for (int col = 0; col < 5; ++col)
			{
				field[row][col+1] = SCORE_FONT[score[0]][col][row];
				field[row+17][col+1] = SCORE_FONT[score[1]][col][row];
			}
		}
	}

	private void AddBallToPlayfield(byte[][] field)
	{
		int x = System.Math.Max(0, System.Math.Min(19, (int)(ballPosition[0])));
		int y = System.Math.Max(0, System.Math.Min(9, (int)(ballPosition[1])));

		field[x][y] = Config.PONG_COLOR_INDEX_BALL;
	}

	private void AddPaddlesToPlayfield(byte[][] field)
	{
		for (int player = 0; player < 2; ++player)
		{
			for (int i = 0; i < PADDLE_SIZE; ++i)
			{
				field[paddlePositionX[player]][paddlePositionY[player] + i] = Config.PONG_COLOR_INDEX_PLAYER[player];
			}
		}
	}

	private void MovePaddle(int player, int change)
	{
		int newPos = paddlePositionY[player] + change;

		if (newPos >= 0 && newPos <= Config.LED_COLS - PADDLE_SIZE)
		{
			paddlePositionY[player] = newPos;
		}
	}

	private static System.Random random = new System.Random();

	private void NewBall()
	{
		ballPosition[0] = (Config.LED_ROWS - 1.0) / 2.0;
		ballPosition[1] = (Config.LED_COLS - 1.0) / 2.0;

		ballDirection[0] = random.NextDouble() > 0.5 ? -0.2 : 0.2;
		ballDirection[1] = random.NextDouble() > 0.5 ? random.NextDouble() * 0.8 + 0.1 : random.NextDouble() * -0.8 - 0.1;
	}

	private void HitLeftRight(int player)
	{
		speaker.BeepSirene();

		NewBall();

		score[player] += 1;

		if (score[player] > 9)
		{
			score[player] = 0;
		}
	}

	private void HitPaddle(double skew)
	{
		speaker.BeepPaddleHit();

		ballDirection[0] = -ballDirection[0];
		ballDirection[1] -= skew;

		for (int i = 0; i < 2; ++i)
		{
			ballDirection[i] *= 1.1; // Increase speed
		}
	}

	private void Tick()
	{
		// Move ball
		for (int i = 0; i < 2; ++i)
		{
			ballPosition[i] += ballDirection[i];
		}

		// Wall collision top/bottom
		if (ballPosition[1] < 0 || ballPosition[1] >= Config.LED_COLS)
		{
			ballDirection[1] = -ballDirection[1];
		}

		// Wall collision left/right
		if (ballPosition[0] < 0)
		{
			HitLeftRight(1);
		}

		if (ballPosition[0] >= Config.LED_ROWS)
		{
			HitLeftRight(0);
		}

		// Paddle collision
		if (ballDirection[0] < 0)
		{
			if (paddlePositionX[0] + 0.5 <= ballPosition[0] && ballPosition[0] <= paddlePositionX[0] + 1.5)
			{
				if (paddlePositionY[0] - 0.5 <= ballPosition[1] && ballPosition[1] <= paddlePositionY[0] + PADDLE_SIZE + 0.5)
				{
					double paddleSkew = (paddlePositionY[0] + PADDLE_SIZE/2.0 - ballPosition[1])/10.0;
					HitPaddle(paddleSkew);
				}
			}
		}

		if (ballDirection[0] > 0)
		{
			if (paddlePositionX[1] - 0.5 <= ballPosition[0] && ballPosition[0] <= paddlePositionX[1] + 0.5)
			{
				if (paddlePositionY[1] - 0.5 <= ballPosition[1] && ballPosition[1] <= paddlePositionY[1] + PADDLE_SIZE + 0.5)
				{
					double paddleSkew = (paddlePositionY[1] + PADDLE_SIZE/2.0 - ballPosition[1])/10.0;
					HitPaddle(paddleSkew);
				}
			}
		}
	}

	public void RunGameLoop()
	{
		FrameRenderedCB(ledStrip, 0);

		timer = new Timer(delegate(object state) { Tick(); }, null, 100, 100);

		while (loop)
		{
			char key = keyPress.ReadSingleKeypress();

			switch (key)
			{
			case 'a':
				MovePaddle(0, -1);
				break;

			case 's':
				MovePaddle(0, 1);
				break;

			case 'k':
				MovePaddle(1, -1);
				break;

			case 'l':
				MovePaddle(1, 1);
				break;

			case 'r':
				InitGame();
				break;

			case 'q':
				loop = false;
				break;
			}
		}

		ledStrip.FrameRendered -= FrameRenderedCB;
		timer.Change(Timeout.Infinite, Timeout.Infinite);
	}

	private static Pong pong;

	static void Main()
	{
		// Create IP Connection and connect it
		IPConnection ipcon = new IPConnection();
		ipcon.Connect(Config.HOST, Config.PORT);

		// Create Tetris object and start game loop
		pong = new Pong(ipcon);

		if (pong.IsOkay()) {
			System.Console.WriteLine("Press q to exit");
			pong.RunGameLoop();
		}

		ipcon.Disconnect();
	}
}
