import select
import sys
import time

# Version 1: Using select with timeout (efficient)
def efficient_loop():
    for i in range(100):
        ready, _, _ = select.select([sys.stdin], [], [], 0.1)  # Blocks efficiently
        if ready:
            break

# Version 2: Busy waiting (inefficient)
def wasteful_loop():
    for i in range(100_000):
        # Check every iteration - burns CPU!
        time.sleep(0.00001)  # Even with sleep, wastes more CPU
        pass

# Run 'top' or 'htop' in another terminal to see CPU usage difference
efficient_loop()  # CPU: ~0%
# wasteful_loop()  # CPU: higher %