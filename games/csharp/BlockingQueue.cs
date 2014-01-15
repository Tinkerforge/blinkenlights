using System.Collections;
using System.Threading;

// There is no BlockingQueue in C# version <= 2.0, we make our own to be backward compatible
class BlockingQueue<T>
{
	private readonly Queue queue = new Queue();

	public BlockingQueue()
	{
		lock (queue)
		{
			Monitor.PulseAll(queue);
		}
	}

	public bool Enqueue(T item)
	{
		lock (queue)
		{
			if (item == null)
			{
				return false;
			}

			queue.Enqueue(item);

			if (queue.Count == 1)
			{
				// wake up any blocked dequeue
				Monitor.PulseAll(queue);
			}

			return true;
		}
	}

	public T Dequeue()
	{
		lock (queue)
		{
			while (queue.Count == 0)
			{
				if (!Monitor.Wait(queue, Timeout.Infinite))
				{
					return default(T);
				}
			}

			return (T)queue.Dequeue();
		}
	}
}
