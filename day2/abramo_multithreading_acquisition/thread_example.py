# Multithreading example in Python
# Author: Jacopo Abramo, 26.09.2023

from napari.qt.threading import thread_worker
from napari.qt.threading import WorkerBase

MAX_COUNT = 100_000_000
NUM_THREADS = 8

@thread_worker
def long_count(N: int) -> None:
    print(f"Starting thread: Counting from {N} to 0...")
    while N > 0:
        N -= 1
    print(f"Done! Counter is {N}")

workers = [long_count(MAX_COUNT // NUM_THREADS) for _ in range(NUM_THREADS)]

for worker in workers:
    worker.start()

WorkerBase.await_workers()