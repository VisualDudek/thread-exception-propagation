from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


def task_may_fail(n, should_fail=False):
    """Simulate a task that may fail"""
    delay = random.uniform(1, 3)
    time.sleep(delay)
    if should_fail: 
        raise ValueError(f"Intentional failure for input {n}")
    return n ** 2, delay


# Method 2: Using map() - maintains order
# Results collected in batch, no output until all complete
def method_2_map():
    print("\n=== Method 2: Using map() ===")
    
    numbers = [1, 2, 3, 4, 5]
    fails = [False, False, True, False, True]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # map() returns results in the same order as input
        results = executor.map(task_may_fail, numbers, fails)

        for i, (result, delay) in enumerate(results):
            print(f"Number {numbers[i]}: {result} (took {delay:.1f}s)")

if __name__ == "__main__":
    method_2_map()