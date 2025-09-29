import threading
import time

print("=== Boolean Approach (Inefficient) ===")
class BooleanApproach:
    def __init__(self):
        self.should_stop = False
    
    def worker(self):
        iterations = 0
        while not self.should_stop:
            iterations += 1
            time.sleep(0.001)  # Must poll frequently
        print(f"Boolean: {iterations} iterations")

boolean_ex = BooleanApproach()
thread = threading.Thread(target=boolean_ex.worker)
start = time.time()
thread.start()
time.sleep(0.1)
boolean_ex.should_stop = True
thread.join()
print(f"Boolean time: {time.time() - start:.3f}s\n")

print("=== Event Approach (Efficient) ===")
class EventApproach:
    def __init__(self):
        self.stop_event = threading.Event()
    
    def worker(self):
        iterations = 0
        while not self.stop_event.is_set():
            iterations += 1
            # PLAY WITH THIS
            # self.stop_event.wait(timeout=0.001)  # Efficient waiting
            self.stop_event.wait()
        print(f"Event: {iterations} iterations")

event_ex = EventApproach()
thread = threading.Thread(target=event_ex.worker)
start = time.time()
thread.start()
time.sleep(0.1)
event_ex.stop_event.set()
thread.join()
print(f"Event time: {time.time() - start:.3f}s")