import queue
import threading
import time
import random

def producer(q, producer_id):
    for i in range(5):
        item = f"Item-{producer_id}-{i}"
        q.put(item)
        print(f"Producer {producer_id} produced: {item}")
        time.sleep(random.uniform(0.1, 0.5))
    
def consumer(q, consumer_id):
    while True:
        try:
            # Get item with timeout to avoid infinite blocking
            item = q.get(timeout=2)
            print(f"Consumer {consumer_id} consumed: {item}")
            time.sleep(random.uniform(0.1, 0.3))  # Simulate work
            q.task_done()
        except queue.Empty:
            print(f"Consumer {consumer_id} timed out, exiting")
            break

# Create queue and threads
work_queue = queue.Queue()

# Start producers
producers = []
for i in range(2):
    p = threading.Thread(target=producer, args=(work_queue, i))
    p.start()
    producers.append(p)

# Start consumers
consumers = []
for i in range(3):
    c = threading.Thread(target=consumer, args=(work_queue, i))
    c.daemon = True  # Dies when main thread dies
    c.start()
    consumers.append(c)

# Wait for producers to finish
for p in producers:
    p.join()

# Wait for all items to be processed
work_queue.join()
print("All work completed!")