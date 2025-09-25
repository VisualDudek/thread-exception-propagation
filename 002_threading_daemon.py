import threading
import time


# =====================================
# Dy default threads are non-demon
# you need explicite set daemon True
#
# t.join() blocking until givent t thread finish
# =====================================

def long_task():
    for i in range(10):
        print(f"Woriking... {i}")
        time.sleep(0.5)

thread = threading.Thread(
    target=long_task,
    daemon=True, # None by default, None a nie False !!!
    )

thread.start()
# thread.join() 

print("Main started")
time.sleep(2)
print("Main program ending")

