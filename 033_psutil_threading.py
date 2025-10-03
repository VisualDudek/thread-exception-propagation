import threading
import time
import psutil
import os
from datetime import datetime
from queue import Queue

def input_thread(input_queue):
    """Thread that wraps input() to make it non-blocking"""
    while True:
        user_input = input()
        input_queue.put(user_input)
        if user_input.lower() == 'quit':
            break

def heartbeat_thread(stop_event):
    """Thread that prints timestamp every 2 seconds"""
    while not stop_event.is_set():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[HEARTBEAT] {timestamp}")
        time.sleep(2)

def cpu_monitor_thread(stop_event):
    """Thread that monitors CPU and memory usage"""
    process = psutil.Process(os.getpid())
    
    while not stop_event.is_set():
        # Get CPU percentage (interval=1 means measure over 1 second)
        cpu_percent = process.cpu_percent(interval=1)
        
        # Get memory info
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / 1024 / 1024  # Convert to MB
        
        # Get thread count
        num_threads = process.num_threads()
        
        print(f"[CPU MONITOR] CPU: {cpu_percent:5.1f}% | Memory: {memory_mb:6.2f} MB | Threads: {num_threads}")
        
        # Sleep for remaining time (total 5 sec between reports)
        time.sleep(4)

def main():
    # Queue for communication between threads
    input_queue = Queue()
    stop_event = threading.Event()
    
    # Get initial process info
    process = psutil.Process(os.getpid())
    print(f"Process ID: {process.pid}")
    print(f"Process Name: {process.name()}")
    print("=" * 70)
    
    # Create and start threads
    input_t = threading.Thread(target=input_thread, args=(input_queue,), daemon=True)
    heartbeat_t = threading.Thread(target=heartbeat_thread, args=(stop_event,), daemon=True)
    cpu_monitor_t = threading.Thread(target=cpu_monitor_thread, args=(stop_event,), daemon=True)
    
    input_t.start()
    heartbeat_t.start()
    cpu_monitor_t.start()
    
    print("Program started. Type 'quit' to exit.")
    print("Heartbeat will print every 2 seconds...")
    print("CPU monitoring will print every 5 seconds...")
    print("=" * 70)
    
    # Main thread checks for user input from queue
    while True:
        if not input_queue.empty():
            user_input = input_queue.get()
            print(f"[INPUT] You entered: {user_input}")
            
            if user_input.lower() == 'quit':
                print("Shutting down...")
                stop_event.set()
                break

        # PLAY WITH sleep time -> CPU usage
        # Small sleep to prevent busy-waiting
        time.sleep(0.1)
        # time.sleep(0) 
    
    # Wait for threads to finish
    heartbeat_t.join(timeout=3)
    cpu_monitor_t.join(timeout=3)
    
    print("=" * 70)
    print("Program terminated.")

if __name__ == "__main__":
    main()