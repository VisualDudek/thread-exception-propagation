import threading
import time
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

def main():
    # Queue for communication between threads
    input_queue = Queue()
    stop_event = threading.Event()
    
    # Create and start threads
    input_t = threading.Thread(target=input_thread, args=(input_queue,), daemon=True)
    heartbeat_t = threading.Thread(target=heartbeat_thread, args=(stop_event,), daemon=True)
    
    input_t.start()
    heartbeat_t.start()
    
    print("Program started. Type 'quit' to exit.")
    print("Heartbeat will print every 2 seconds...")
    
    # Main thread checks for user input from queue
    while True:
        if not input_queue.empty():
            user_input = input_queue.get()
            print(f"You entered: {user_input}")
            
            if user_input.lower() == 'quit':
                print("Shutting down...")
                stop_event.set()
                break
        
        time.sleep(0.1)  # Small sleep to prevent busy-waiting
    
    # Wait for threads to finish
    heartbeat_t.join(timeout=3)
    print("Program terminated.")

if __name__ == "__main__":
    main()