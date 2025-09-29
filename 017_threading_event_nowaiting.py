import threading
import time

# With boolean - inefficient busy-waiting
class BooleanWaiting:
    def __init__(self):
        self.data_ready = False
        self.couter = 0
    
    def waiter(self):
        print("[Waiter] Waiting for data...")
        # Busy-wait - wastes CPU!
        while not self.data_ready:
            # time.sleep(0.01)  # Still checking 100 times per second!
            self.couter += 1
        print(f"[Waiter] Data is ready! waisting CPU {self.couter} times")
    
    def producer(self):
        time.sleep(1)
        print("[Producer] Data ready")
        self.data_ready = True

boolean_wait = BooleanWaiting()
t1 = threading.Thread(target=boolean_wait.waiter)
t2 = threading.Thread(target=boolean_wait.producer)
t1.start()
t2.start()
t1.join()
t2.join()