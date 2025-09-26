from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import traceback

def task_that_fails(task_id, delay, should_fail=True):
    """Task that might raise an exception"""
    print(f"Task {task_id} starting...")
    time.sleep(delay)  # Simulate some work
    
    if should_fail:
        if task_id == 1:
            raise ValueError(f"Task {task_id}: Something went wrong!")
        elif task_id == 2:
            raise ConnectionError(f"Task {task_id}: Network failed!")
        elif task_id == 3:
            raise FileNotFoundError(f"Task {task_id}: File not found!")
    
    return f"Task {task_id} completed successfully"

def demonstrate_exception_handling():
    """Show how ThreadPoolExecutor handles exceptions"""
    
    print("=== BASIC EXCEPTION HANDLING ===")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks - some will fail
        future1 = executor.submit(task_that_fails, 1, 1, True)   # Will fail
        future2 = executor.submit(task_that_fails, 2, 1, True)   # Will fail  
        future3 = executor.submit(task_that_fails, 3, 0, False)  # Will succeed
        
        futures = [future1, future2, future3]
        
        # Check what happens to futures when exceptions occur
        # time.sleep(2)  # Wait for tasks to complete
        
        for i, future in enumerate(as_completed(futures), 1):
            print(f"\nFuture {i} status:")
            print(f"  done(): {future.done()}")
            print(f"  cancelled(): {future.cancelled()}")
            
            # The exception is stored IN the future, not raised in the worker thread
            try:
                result = future.result()
                print(f"  result: {result}")
            except Exception as e:
                print(f"  exception: {type(e).__name__}: {e}")

demonstrate_exception_handling()