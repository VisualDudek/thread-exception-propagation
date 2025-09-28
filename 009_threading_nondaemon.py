import threading
import time

# =====================================
# shows that main program wait for thread
# to finish, do not exit immediately 
# =====================================

def long_task():
    print("Starting long task")
    for i in range(5):
        print(f"working ... {i}")
        time.sleep(0.5)
    print("ending long task")

def main() -> None:
    print("START main")
    t = threading.Thread(target=long_task, daemon=None)
    t.start()
    t.join() # this is blocking for main, try to un/comment and see the diff
    print("END main")


if __name__ == '__main__':
    main()
