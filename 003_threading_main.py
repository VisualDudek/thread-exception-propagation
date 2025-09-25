import threading
import time


# =====================================
# Main thread is NOT daemon
# =====================================


print(f"Main thread properties: {threading.current_thread().daemon}")
