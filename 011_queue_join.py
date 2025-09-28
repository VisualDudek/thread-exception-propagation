import threading
import queue
import time

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done() # comment to see that q.join() will block forever
        time.sleep(0.5)

# Turn-on the worker thread.
threading.Thread(target=worker, daemon=True).start()

# Send thirty task requests to the worker.
for item in range(10):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')