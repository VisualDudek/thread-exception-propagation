import threading
import time

class MultipleWaiters:
    def __init__(self):
        self.start_event = threading.Event()
    
    def worker(self, worker_id):
        print(f"[Worker {worker_id}] Ready, waiting for start signal...")
        self.start_event.wait()  # All workers wait
        print(f"[Worker {worker_id}] Started!")
    
    def coordinator(self):
        time.sleep(1)
        print("[Coordinator] Starting all workers at once!")
        self.start_event.set()  # Wake ALL waiters simultaneously

multi = MultipleWaiters()
workers = [threading.Thread(target=multi.worker, args=(i,)) for i in range(5)]
coordinator = threading.Thread(target=multi.coordinator)

for w in workers:
    w.start()
coordinator.start()

for w in workers:
    w.join()
coordinator.join()