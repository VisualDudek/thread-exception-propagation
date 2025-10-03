import asyncio
from datetime import datetime

async def input_task():
    """Async task that handles user input"""
    loop = asyncio.get_event_loop()
    while True:
        # Run input() in executor to avoid blocking the event loop
        user_input = await loop.run_in_executor(None, input)
        print(f"You entered: {user_input}")
        
        if user_input.lower() == 'quit':
            return user_input

async def heartbeat_task():
    """Async task that prints timestamp every 2 seconds"""
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[HEARTBEAT] {timestamp}")
        await asyncio.sleep(2)

async def main():
    print("Program started. Type 'quit' to exit.")
    print("Heartbeat will print every 2 seconds...")
    
    # Create tasks
    input_coro = asyncio.create_task(input_task())
    heartbeat_coro = asyncio.create_task(heartbeat_task())
    
    # Wait for input task to complete (when user types 'quit')
    await input_coro
    
    # Cancel heartbeat task
    heartbeat_coro.cancel()
    try:
        await heartbeat_coro
    except asyncio.CancelledError:
        pass
    
    print("Program terminated.")

if __name__ == "__main__":
    asyncio.run(main())