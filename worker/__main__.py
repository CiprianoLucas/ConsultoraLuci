import asyncio

from worker import worker_loop

if __name__ == "__main__":
    asyncio.run(worker_loop())
