import random
import asyncio
from pb_ble import get_virtual_ble

async def broadcast_random_value():
    # Assuming get_virtual_ble is an async function that returns a context manager for the virtual BLE
    async with await get_virtual_ble(broadcast_channel=2) as vble:
        # Broadcast a random number on channel 2
        val = random.randint(0, 3)
        await vble.broadcast(val)
        # Stop after 10 seconds
        await asyncio.sleep(10)

# Run the async function
asyncio.run(broadcast_random_value())