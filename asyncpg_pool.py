
# Benchmark for asyncpg connection pool.

import asyncio
import asyncpg
import time
import numpy as np

times = []

creds = {
    "user": "postgres",
    "password": "123456789",
    "host": "localhost",
    "port": "5432",
    "database": "postgres"
}


async def performance_testing():
    pool = await asyncpg.create_pool(creds, max_size=50, min_size=50)
    async def db():
        start = time.time()
        async with pool.acquire() as connection:
            pass
        end = time.time()
        times.append((end - start))
    tasks = [db() for _ in range(2000)]
    await asyncio.gather(*tasks)

   

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(performance_testing())
    loop.close()

    print("number of request", len(times))
    print(f'p50 stands at: {np.percentile(times, 50):.2f}s')
    print(f'p75 stands at: {np.percentile(times, 75):.2f}s')
    print(f'p90 stands at: {np.percentile(times, 90):.2f}s')
    print(f'p95 stands at: {np.percentile(times, 95):.2f}s')
    print(f'p99 stands at: {np.percentile(times, 99):.2f}s')
