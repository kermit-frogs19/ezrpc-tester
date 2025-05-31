from ezRPC import Producer
import asyncio
import time
import grpc
import ping_pb2
import ping_pb2_grpc
import requests
import httpx


# try:
#     import uvloop
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#     print("system: Using uvloop for asyncio event loop")
# except ImportError:
#     uvloop = None
#     print("system: Failed to import/connect uvloop for asyncio event loop")


async def main_requests():
    print("STARTING REQUESTS TEST\n")
    delay = 30
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
        # channel = grpc.insecure_channel("nyc3.seliukov.com:50051")
        # stub = ping_pb2_grpc.PingerStub(channel)
        # client = Producer("https://nyc3.seliukov.com:8000", use_tls=False, timeout=None)

        for _ in range(5):
            # stub.Ping(ping_pb2.Empty())
            requests.post(url="http://nyc3.seliukov.com:5000/ping", json={"key": "value"}, timeout=None)

            # await client.ping()

        # here the timer start
        start = time.perf_counter()
        for _ in range(batch_size):
            requests.post(url="http://nyc3.seliukov.com:5000/ping", json={"key": "value"}, timeout=None)

            # stub.Ping(ping_pb2.Empty())
            # await client.ping()
        end = time.perf_counter()
        duration = end - start
        durations.append(duration)
        print(f"Batch {i+1}: {batch_size} requests took {duration:.6f} seconds. Average time per request: {duration / batch_size:.6f} seconds")     # here the timer end

        # channel.close()
        # await client.close()

    print(f"\n[SUMMARY] Library REQUESTS {batches_amount} batches × {batch_size} requests")
    print(f"\n[SUMMARY] Collected results: {durations}")
    print(f"[SUMMARY] Total average time per {batch_size} request(s): {sum(durations) / len(durations)} seconds")
    print(f"[SUMMARY] Total average time per single request: {sum(durations) / len(durations) / batch_size} seconds")

async def main_httpx():
    print("STARTING HTTPX TEST\n")
    delay = 30
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
        print(f"\n\nStarting batch #{i + 1}")
        # channel = grpc.insecure_channel("nyc3.seliukov.com:50051")
        # stub = ping_pb2_grpc.PingerStub(channel)
        # client = Producer("https://nyc3.seliukov.com:8000", use_tls=False, timeout=None)
        async_client = httpx.AsyncClient(timeout=None)

        for _ in range(5):
            # stub.Ping(ping_pb2.Empty())
            await async_client.post(url="http://nyc3.seliukov.com:5000/ping")
            # await client.ping()

        # here the timer start
        start = time.perf_counter()
        for _ in range(batch_size):
            # stub.Ping(ping_pb2.Empty())
            # await client.ping()
            await async_client.post(url="http://nyc3.seliukov.com:5000/ping")

        end = time.perf_counter()
        duration = end - start
        durations.append(duration)
        print(f"Batch {i + 1}: {batch_size} requests took {duration:.6f} seconds. Average time per request: {duration / batch_size:.6f} seconds")  # here the timer end

        # channel.close()
        # await client.close()
        await async_client.aclose()

    print(f"\n[SUMMARY] library HTTPX {batches_amount} batches × {batch_size} requests")
    print(f"\n[SUMMARY] Collected results: {durations}")
    print(f"[SUMMARY] Total average time per {batch_size} request(s): {sum(durations) / len(durations)} seconds")
    print(f"[SUMMARY] Total average time per single request: {sum(durations) / len(durations) / batch_size} seconds")


async def main():
    await main_requests()
    await main_httpx()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
