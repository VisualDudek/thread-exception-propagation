import threading
import time

class EfficientWaiting:
    def __init__(self):
        self.data_ready_event = threading.Event()
    
    def waiter(self):
        print("[Waiter] Waiting efficiently...")
        # Blocks the thread without busy-waiting!
        # CPU does other work instead of spinning
        self.data_ready_event.wait()  
        print("[Waiter] Data is ready!")
    
    def producer(self):
        time.sleep(1)
        print("[Producer] Data ready, signaling...")
        self.data_ready_event.set()  # Wake up waiter

efficient = EfficientWaiting()
t1 = threading.Thread(target=efficient.waiter)
t2 = threading.Thread(target=efficient.producer)
t1.start()
t2.start()
t1.join()
t2.join()