from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random


def task_may_fail(n, should_fail=False):
    """Simulate a task that may fail"""
    delay = random.uniform(1, 3)
    time.sleep(delay)
    if should_fail: 
        raise ValueError(f"Intentional failure for input {n}")
    print(f"Task {n}: {n ** 2} (took {delay:.1f}s)")
    return n ** 2, delay


def method_1_individual_submit():
    print("=== Method 1: Individual Submit ===")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks individually
        futures = []
        for i in range(3):
            future = executor.submit(task_may_fail, i)
            futures.append(future)

        future = executor.submit(task_may_fail, 3, should_fail=True)
        futures.append(future)
        future = executor.submit(task_may_fail, 4, should_fail=False)
        futures.append(future)
        
        # Collect results in submission order
        # for i, future in enumerate(futures):
        #     result, delay = future.result()
        #     print(f"Task {i}: {result} (took {delay:.1f}s)")

if __name__ == "__main__":
    method_1_individual_submit()