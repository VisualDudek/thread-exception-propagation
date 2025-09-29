import threading
import time

# UNSAFE - Using simple boolean
class UnsafeWorker:
    def __init__(self):
        self.should_stop = False  # Simple boolean
        
    def worker(self):
        print("[Worker] Starting...")
        while not self.should_stop:  # Reading boolean
            print("[Worker] Working...")
            time.sleep(0.5)
        print("[Worker] Stopped")
    
    def stop(self):
        print("[Main] Setting stop flag...")
        self.should_stop = True  # Writing boolean

# This SEEMS to work but has potential issues
unsafe = UnsafeWorker()
thread = threading.Thread(target=unsafe.worker)
thread.start()

time.sleep(2)
unsafe.stop()
thread.join()