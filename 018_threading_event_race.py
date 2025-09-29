import threading
import time

class RaceCondition:
    def __init__(self):
        self.should_process = False
        self.data = None
    
    def worker(self):
        while True:
            if self.should_process:  # Check flag
                # RACE: Main thread might modify data here!
                print(f"[Worker] Processing: {self.data}")
                self.should_process = False
                time.sleep(0.1)
    
    def set_data(self, value):
        self.data = value
        # RACE: Worker might read old data before this executes!
        self.should_process = True

# Race condition possible
race = RaceCondition()
thread = threading.Thread(target=race.worker, daemon=True)
thread.start()

race.set_data("First")
# time.sleep(0.05) # PLAY WITH THIS
race.set_data("Second")  # Might overwrite before worker processes "First"
time.sleep(0.5)