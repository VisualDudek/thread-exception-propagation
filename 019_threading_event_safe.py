import threading
import time

# SAFE - Using threading.Event
class SafeWorker:
    def __init__(self):
        self.stop_event = threading.Event()  # Thread-safe event
        
    def worker(self):
        print("[Worker] Starting...")
        while not self.stop_event.is_set():  # Thread-safe check
            print("[Worker] Working...")
            time.sleep(0.5)
        print("[Worker] Stopped")
    
    def stop(self):
        print("[Main] Signaling stop...")
        self.stop_event.set()  # Thread-safe signal

safe = SafeWorker()
thread = threading.Thread(target=safe.worker)
thread.start()

time.sleep(2)
safe.stop()
thread.join()