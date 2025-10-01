from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

def slow_computation(n):
    """Simulate slow computation"""
    delay = random.uniform(1, 3)
    time.sleep(delay)
    return n ** 2, delay

# Method 1: Submit individual tasks
def method_1_individual_submit():
    print("=== Method 1: Individual Submit ===")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit tasks individually
        futures = []
        for i in range(5):
            future = executor.submit(slow_computation, i)
            futures.append(future)
        
        # Collect results in submission order
        for i, future in enumerate(futures):
            result, delay = future.result()
            print(f"Task {i}: {result} (took {delay:.1f}s)")

# Method 2: Using map() - maintains order
# Results collected in batch, no output until all complete
def method_2_map():
    print("\n=== Method 2: Using map() ===")
    
    numbers = [1, 2, 3, 4, 5]
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # map() returns results in the same order as input
        results = executor.map(slow_computation, numbers)
        
        for i, (result, delay) in enumerate(results):
            print(f"Number {numbers[i]}: {result} (took {delay:.1f}s)")

# Method 3: Process results as they complete
def method_3_as_completed():
    print("\n=== Method 3: As Completed ===")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        future_to_number = {
            executor.submit(slow_computation, i): i 
            for i in range(6)
        }
        
        # Process results as they complete (not in order)
        for future in as_completed(future_to_number):
            number = future_to_number[future]
            try:
                result, delay = future.result()
                print(f"Completed: Number {number} -> {result} (took {delay:.1f}s)")
            except Exception as exc:
                print(f"Task {number} generated exception: {exc}")

# Run all methods
if __name__ == "__main__":
    method_1_individual_submit()
    method_2_map()
    method_3_as_completed()