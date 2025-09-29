import threading
import time

class ReusableEvent:
    def __init__(self):
        self.event = threading.Event()
    
    def worker(self):
        for round_num in range(3):
            print(f"[Worker] Waiting for round {round_num + 1}...")
            self.event.wait()
            print(f"[Worker] Processing round {round_num + 1}")
            time.sleep(0.5)
            self.event.clear()  # Reset for next round
    
    def controller(self):
        for round_num in range(3):
            # PLAY WITH TIME 
            time.sleep(1)
            print(f"[Controller] Signaling round {round_num + 1}")
            self.event.set()
            time.sleep(0.6)  # Wait for processing

reusable = ReusableEvent()
t1 = threading.Thread(target=reusable.worker)
t2 = threading.Thread(target=reusable.controller)
t1.start()
t2.start()
t1.join()
t2.join()