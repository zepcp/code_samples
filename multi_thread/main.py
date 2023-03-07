"""
python -m main -o thread
python -m main -o process
python -m main -o pool
"""
from argparse import ArgumentParser
from multiprocessing import Process, Pool
from threading import Thread
import time


def thread_execution(thread_id: int) -> None:
    print(f"Thread {thread_id} started")
    time.sleep(2)
    print(f"Thread {thread_id} ended")
    return


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--option", '-o', choices=["thread", "process", "pool"], required=True)
    args = parser.parse_args()

    if args.option == "thread":
        print("Using threading.Thread...")
        for i in range(3):
            thread = Thread(target=thread_execution, args=(i,))
            thread.start()
    elif args.option == "process":
        print("Using multiprocessing.Process...")
        for i in range(3):
            p = Process(target=thread_execution, args=(i,))
            p.start()
    elif args.option == "pool":
        print("Using multiprocessing.Pool...")
        p = Pool(processes=3)
        p.map(thread_execution, [1, 2, 3])

