using Tinkerforge;
using System.Threading;
using System.Collections;

class MultiTouchInput
{
	private BlockingQueue<char> keyQueue = null;
	private BrickletMultiTouch multiTouch = null;
	private Timer touchTimer = null;
	private int currentState = 0;
	private int[] currentStateCounter = new int[] {0,0,0,0,0,0,0,0,0,0,0,0};

	public MultiTouchInput(IPConnection ipcon, BlockingQueue<char> keyQueue)
	{
		this.keyQueue = keyQueue;

		if (Config.UID_MULTI_TOUCH_BRICKLET == null)
		{
			System.Console.WriteLine("Not Configured: Multi Touch");
			return;
		}

		multiTouch = new BrickletMultiTouch(Config.UID_MULTI_TOUCH_BRICKLET, ipcon);

		try
		{
			multiTouch.GetElectrodeSensitivity();
			System.Console.WriteLine("Found: Multi Touch ({0})",
			                         Config.UID_MULTI_TOUCH_BRICKLET);
		}
		catch (TinkerforgeException)
		{
			System.Console.WriteLine("Not Found: Multi Touch ({0})",
			                         Config.UID_MULTI_TOUCH_BRICKLET);
			return;
		}

		multiTouch.TouchState += TouchStateCB;

		touchTimer = new Timer(delegate(object state) { TouchTick(); }, null, 100, 100);
	}

	private void TouchStateCB(BrickletMultiTouch sender, int touchState)
	{
		int changedState = currentState ^ touchState;

		currentState = touchState;

		StateToQueue(changedState & currentState);
	}

	private void StateToQueue(int state)
	{
		for (int i = 0; i < 12; ++i)
		{
			if ((state & (1 << i)) != 0 && Config.KEYMAP_MULTI_TOUCH.Contains(i))
			{
				keyQueue.Enqueue((char)Config.KEYMAP_MULTI_TOUCH[i]);
			}
		}
	}

	private void TouchTick()
	{
		int state = 0;

		for (int i = 0; i < 12; ++i)
		{
			if ((currentState & (1 << i)) != 0)
			{
				currentStateCounter[i] += 1;
			}
			else
			{
				currentStateCounter[i] = 0;
			}

			if (currentStateCounter[i] > 5)
			{
				state |= (1 << i);
			}
		}

		if (state != 0)
		{
			StateToQueue(state);
		}
	}
}

class KeyBoardInput
{
	public KeyBoardInput(BlockingQueue<char> keyQueue)
	{
		Thread keyBoardThread = new Thread(delegate()
		{
			while (true) {
				char key = System.Char.ToLower(System.Console.ReadKey(true).KeyChar);

				keyQueue.Enqueue(key);
			}
		});

		keyBoardThread.IsBackground = true;
		keyBoardThread.Start();
	}
}

class KeyPress
{
	private BlockingQueue<char> keyQueue = new BlockingQueue<char>();
	private KeyBoardInput keyBoardInput = null;
	private MultiTouchInput multiTouchInput = null;

	public KeyPress(IPConnection ipcon)
	{
		keyBoardInput = new KeyBoardInput(keyQueue);
		multiTouchInput = new MultiTouchInput(ipcon, keyQueue);
	}

	public char ReadSingleKeypress()
	{
		return keyQueue.Dequeue();
	}
}
