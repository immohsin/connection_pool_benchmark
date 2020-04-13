# Benchmark for asyncpg with pgbouncer.


import asyncio
import asyncpg
import time
import numpy as np

times = []

# Replace the creds with pgbouncer to benchmark the pgbouncer latency.
creds = {
    "user": "postgres",
    "password": "123456789",
    "host": "localhost",
    "port": "6432",
    "database": "postgres"
}




async def performance_testing():
    async def db():
        start = time.time()

        connection = await asyncpg.connect(**creds)
        await connection.close()
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