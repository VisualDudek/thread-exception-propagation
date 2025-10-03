import asyncio
import cProfile
import pstats
from datetime import datetime

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
    print("Program started. Type 'quit' to exit.")
    input_coro = asyncio.create_task(input_task())
    heartbeat_coro = asyncio.create_task(heartbeat_task())
    await input_coro
    heartbeat_coro.cancel()
    try:
        await heartbeat_coro
    except asyncio.CancelledError:
        pass
    print("Program terminated.")

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    
    asyncio.run(main())
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 functions