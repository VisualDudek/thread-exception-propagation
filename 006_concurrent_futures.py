from concurrent.futures import ThreadPoolExecutor
import time

def slow_task(task_id, duration):
    print(f"Task {task_id} starting (will take {duration}s)")
    time.sleep(duration)
    print(f"Task {task_id} completed!")
    return f"Result from task {task_id}"

def demonstrate_blocking_behavior():
    """Show that future.result() is blocking"""
    
    print("=== BLOCKING BEHAVIOR DEMO ===")
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit all tasks at once (non-blocking)
        print("Submitting all tasks...")
        future1 = executor.submit(slow_task, 1, 3)  # 3 seconds
        future2 = executor.submit(slow_task, 2, 1)  # 1 second  
        future3 = executor.submit(slow_task, 3, 2)  # 2 seconds
        print("All tasks submitted! Now calling result()...")
        
        # These result() calls are BLOCKING
        start_time = time.time()
        
        print("\nCalling future1.result() - will block for 3 seconds:")
        result1 = future1.result()  # ⏰ BLOCKS until task 1 completes (3s)
        print(f"Got result1: {result1} (waited {time.time() - start_time:.1f}s)")
        
        print("\nCalling future2.result() - task 2 already finished:")
        result2 = future2.result()  # ⚡ Returns immediately (task already done)
        print(f"Got result2: {result2} (total time: {time.time() - start_time:.1f}s)")
        
        print("\nCalling future3.result() - task 3 already finished:")
        result3 = future3.result()  # ⚡ Returns immediately (task already done)
        print(f"Got result3: {result3} (total time: {time.time() - start_time:.1f}s)")

demonstrate_blocking_behavior()