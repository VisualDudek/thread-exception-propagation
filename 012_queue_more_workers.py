import threading
import queue
import time

q = queue.Queue()

def worker(name):
    while True:
        item = q.get()
        print(f'Thread #{name} working on {item}')
        print(f'Thread #{name} finished {item}')
        q.task_done()
        time.sleep(0.5)

# Turn-on the worker thread.
threading.Thread(target=worker, args=[1], daemon=True).start()
threading.Thread(target=worker, args=[2], daemon=True).start()
# Why int in tuple do not work ?
# threading.Thread(target=worker, args=(1), daemon=True).start()

# Send thirty task requests to the worker.
for item in range(10):
    q.put(item)

# Block until all tasks are done.
q.join()
print('All work completed')