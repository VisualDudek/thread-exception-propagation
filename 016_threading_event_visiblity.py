import threading
import time

class VisibilityProblem:
    def __init__(self):
        self.stop_flag = False
        self.counter = 0
    
    def worker(self):
        # Worker thread might cache stop_flag in CPU register
        # and never see the updated value from main thread!
        while not self.stop_flag:
            self.counter += 1
        print(f"[Worker] Stopped after {self.counter} iterations")
    
    def stop(self):
        self.stop_flag = True
        # No guarantee worker thread will see this change immediately
        # Could stay in CPU cache or register

# In theory, the worker might never stop!
problem = VisibilityProblem()
thread = threading.Thread(target=problem.worker)
thread.start()
time.sleep(0.1)
problem.stop()
thread.join(timeout=2)
if thread.is_alive():
    print("WARNING: Thread might still be running!")