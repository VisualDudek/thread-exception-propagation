import threading
import time
import sys


# =====================================
# Without join() - main can exit before thread finish
# ^^^ NOPE not true see next file
# =====================================

def task():
    print(f"Task started")
    time.sleep(2)
    print(f"Task finished")

print("=== Without join() ===")
thread = threading.Thread(target=task,)
thread.start()
# No join() here - main continues immediately AND EXIT
print("Main thread continues without waiting end exit before task in thread finish")

sys.exit()