import threading
import time

# =====================================
# Example 1: Basic "Hello World" Threading
# =====================================

def say_hello(name):
    print(f"Hello from {name}!")

print("=== Basic Threading ===")
# Create a thread
thread1 = threading.Thread(target=say_hello, args=("Thread 1",))
thread1.start()  # Start the thread
thread1.join()   # Wait for it to finish

print()

# =====================================
# Example 2: Multiple Threads
# =====================================

def count_numbers(name, max_count):
    for i in range(1, max_count + 1):
        print(f"{name}: {i}")
        time.sleep(0.5)  # Pause for half a second

print("=== Multiple Threads ===")
# Create two threads
thread1 = threading.Thread(target=count_numbers, args=("Counter A", 3))
thread2 = threading.Thread(target=count_numbers, args=("Counter B", 3))

# Start both threads
thread1.start()
thread2.start()

# Wait for both to finish
thread1.join()
thread2.join()

print("Both threads finished!")
print()

# =====================================
# Example 3: Without join() - See the difference
# =====================================

def slow_task(name):
    print(f"{name} started")
    time.sleep(2)
    print(f"{name} finished")

print("=== Without join() ===")
thread = threading.Thread(target=slow_task, args=("Slow Thread",))
thread.start()
# No join() here - main continues immediately
print("Main thread continues without waiting")

# Wait a bit to see the slow thread finish
time.sleep(3)
print()
