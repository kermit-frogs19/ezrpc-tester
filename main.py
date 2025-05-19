from ezRPC import Producer
import asyncio
import time


async def main():
    delay = 90
    batch_size = 100
    batches_amount = 30

    print(f"Starting test in {delay} second(s)...")
    for second in range(delay):
        await asyncio.sleep(1)
        print(f"{delay - second}", end="-")

    print("\n---STARTING THE TEST---")

    durations: list[float] = []


    # initial test
    for i in range(batches_amount):
        print(f"\n\nStarting batch #{i+1}")
        client = Producer("https://nyc3.vadim-seliukov-quic-server.com:8000", use_tls=False)

        for _ in range(5):
            await client.call("dummy")

        # here the timer start
        start = time.perf_counter()
        for _ in range(batch_size):
            await client.call("dummy")
        end = time.perf_counter()
        duration = end - start
        durations.append(duration)
        print(f"Batch {i+1}: {batch_size} requests took {duration:.6f} seconds. Average time per request: {duration / batch_size:.6f} seconds")     # here the timer end

        await client.close()

    print(f"\n[SUMMARY] {batches_amount} batches × {batch_size} requests")
    print(f"\n[SUMMARY] Collected results: {durations}")
    print(f"[SUMMARY] Total average time per {batch_size} request(s): {sum(durations) / len(durations)} seconds")
    print(f"[SUMMARY] Total average time per single request: {sum(durations) / len(durations) / batch_size} seconds")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
