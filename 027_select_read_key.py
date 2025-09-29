import select
import sys

# Why this do not work in Cooked Mode?
def efficient_loop():
    for i in range(100):
        ready, _, _ = select.select([sys.stdin], [], [], 0.1)  # Blocks efficiently
        if ready:
            key = sys.stdin.read(1)
            print(f"Key: {key}")
        else: 
            # Timeout occurred - no input
            pass


efficient_loop()