import asyncio
import psutil
import os
from datetime import datetime

async def cpu_monitor_task():
    """Monitor CPU usage of current process"""
    process = psutil.Process(os.getpid())
    while True:
        cpu_percent = process.cpu_percent(interval=1)
        memory_info = process.memory_info()
        print(f"[CPU MONITOR] CPU: {cpu_percent}% | Memory: {memory_info.rss / 1024 / 1024:.2f} MB")
        await asyncio.sleep(5)

async def input_task():
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input)
        print(f"You entered: {user_input}")
        if user_input.lower() == 'quit':
            return user_input

async def heartbeat_task():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[HEARTBEAT] {timestamp}")
        await asyncio.sleep(2)

async def main():
    print("Program started with CPU monitoring. Type 'quit' to exit.")
    
    input_coro = asyncio.create_task(input_task())
    heartbeat_coro = asyncio.create_task(heartbeat_task())
    cpu_monitor_coro = asyncio.create_task(cpu_monitor_task())
    
    await input_coro
    
    heartbeat_coro.cancel()
    cpu_monitor_coro.cancel()
    
    for task in [heartbeat_coro, cpu_monitor_coro]:
        try:
            await task
        except asyncio.CancelledError:
            pass
    
    print("Program terminated.")

if __name__ == "__main__":
    asyncio.run(main())