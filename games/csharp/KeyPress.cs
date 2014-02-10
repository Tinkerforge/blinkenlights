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

		multiTouch.SetElectrodeSensitivity(100);
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

class DualButtonInput
{
	private BlockingQueue<char> keyQueue = null;
	private BrickletDualButton dualButton1 = null;
	private BrickletDualButton dualButton2 = null;
	private Timer pressTimer = null;
	private int currentState = 0;
	private int[] currentStateCounter = new int[] {0,0,0,0};

	public DualButtonInput(IPConnection ipcon, BlockingQueue<char> keyQueue)
	{
		this.keyQueue = keyQueue;

		byte buttonL;
		byte buttonR;

		if (Config.UID_DUAL_BUTTON_BRICKLET[0] == null)
		{
			System.Console.WriteLine("Not Configured: Dual Button 1");
		}
		else
		{
			dualButton1 = new BrickletDualButton(Config.UID_DUAL_BUTTON_BRICKLET[0], ipcon);

			try
			{
				dualButton1.GetButtonState(out buttonL, out buttonR);
				System.Console.WriteLine("Found: Dual Button 1 ({0})",
				                         Config.UID_DUAL_BUTTON_BRICKLET[0]);
			}
			catch (TinkerforgeException)
			{
				System.Console.WriteLine("Not Found: Dual Button 1 ({0})",
				                         Config.UID_DUAL_BUTTON_BRICKLET[0]);
			}

			dualButton1.StateChanged += StateChanged1CB;
		}

		if (Config.UID_DUAL_BUTTON_BRICKLET[1] == null)
		{
			System.Console.WriteLine("Not Configured: Dual Button 2");
		}
		else
		{
			dualButton2 = new BrickletDualButton(Config.UID_DUAL_BUTTON_BRICKLET[1], ipcon);

			try
			{
				dualButton2.GetButtonState(out buttonL, out buttonR);
				System.Console.WriteLine("Found: Dual Button 2 ({0})",
				                         Config.UID_DUAL_BUTTON_BRICKLET[0]);
			}
			catch (TinkerforgeException)
			{
				System.Console.WriteLine("Not Found: Dual Button 2 ({0})",
				                         Config.UID_DUAL_BUTTON_BRICKLET[0]);
			}

			dualButton2.StateChanged += StateChanged2CB;
		}

		pressTimer = new Timer(delegate(object state) { PressTick(); }, null, 100, 100);
	}

	private void StateChanged1CB(BrickletDualButton sender, byte buttonL, byte buttonR, byte ledL, byte ledR)
	{
		int l = buttonL == BrickletDualButton.BUTTON_STATE_PRESSED ? 1 : 0;
		int r = buttonR == BrickletDualButton.BUTTON_STATE_PRESSED ? 1 : 0;
		int state = (l << 0) | (r << 1);
		int changedState = (currentState ^ state) & 3 /* 0b0011 */;

		currentState = state;

		StateToQueue(changedState & currentState);
	}

	private void StateChanged2CB(BrickletDualButton sender, byte buttonL, byte buttonR, byte ledL, byte ledR)
	{
		int l = buttonL == BrickletDualButton.BUTTON_STATE_PRESSED ? 1 : 0;
		int r = buttonR == BrickletDualButton.BUTTON_STATE_PRESSED ? 1 : 0;
		int state = (l << 2) | (r << 3);
		int changedState = (currentState ^ state) & 12 /* 0b1100 */;

		currentState = state;

		StateToQueue(changedState & currentState);
	}

	private void StateToQueue(int state)
	{
		for (int i = 0; i < 4; ++i)
		{
			if ((state & (1 << i)) != 0 && Config.KEYMAP_DUAL_BUTTON.Contains(i))
			{
				keyQueue.Enqueue((char)Config.KEYMAP_DUAL_BUTTON[i]);
			}
		}
	}

	private void PressTick()
	{
		int state = 0;

		for (int i = 0; i < 4; ++i)
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
	private MultiTouchInput multiTouchInput = null;
	private DualButtonInput dualButtonInput = null;
	private KeyBoardInput keyBoardInput = null;

	public KeyPress(IPConnection ipcon)
	{
		multiTouchInput = new MultiTouchInput(ipcon, keyQueue);
		dualButtonInput = new DualButtonInput(ipcon, keyQueue);
		keyBoardInput = new KeyBoardInput(keyQueue);
	}

	public char ReadSingleKeypress()
	{
		return keyQueue.Dequeue();
	}
}
