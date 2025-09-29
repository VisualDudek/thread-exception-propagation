import threading
import time

class TimeoutExample:
    def __init__(self):
        self.event = threading.Event()
    
    def waiter_with_timeout(self):
        print("[Waiter] Waiting up to 2 seconds...")
        
        if self.event.wait(timeout=2.0):  # Wait max 2 seconds
            print("[Waiter] Event occurred!")
        else:
            print("[Waiter] Timeout - giving up")
    
    def slow_producer(self):
        time.sleep(3)  # Takes too long
        self.event.set()

timeout_ex = TimeoutExample()
t1 = threading.Thread(target=timeout_ex.waiter_with_timeout)
t2 = threading.Thread(target=timeout_ex.slow_producer)
t1.start()
t2.start()
t1.join()
t2.join()