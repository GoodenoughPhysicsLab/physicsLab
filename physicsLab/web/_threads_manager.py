# -*- coding: utf-8 -*-
''' .webutils.py has used ThreadPoolExecutor everywhere.
    But, I have met some problems and found a solution:
        https://www.bilibili.com/video/BV1au411q7LN/?spm_id_from=333.999.0.0

    However, I can't apply this simple solution to built-in ThreadPoolExecutor.
    That's why I write this module.
'''
import os
import time
import queue
import threading
from physicsLab.typehint import Optional, Callable, Set, Self

class _Task:
    class _WaitingResult:
        def __new__(cls):
            return cls

    def __init__(self, func: Callable, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.func_res = self._WaitingResult

    def run(self):
        self.func_res = self.func(*self.args, **self.kwargs)

    def result(self):
        while self.func_res is self._WaitingResult:
            pass
        return self.func_res

def _office(tasks: queue.SimpleQueue):
    ''' workers work here '''
    while True:
        while tasks.empty():
            time.sleep(0.1)
        task = tasks.get_nowait()
        if task is _EndOfQueue:
            tasks.put_nowait(_EndOfQueue)
            break
        task.run()

class _EndOfQueue:
    def __new__(cls):
        return cls

class ThreadsManager:
    def __init__(self, max_workers: Optional[int] = None) -> None:
        assert isinstance(max_workers, int) and max_workers > 0 \
            or max_workers is None

        if max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        self.max_workers = max_workers
        self.workers: Set[threading.Thread] = set()
        self.tasks = queue.SimpleQueue()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.tasks.put(_EndOfQueue)
        for worker in self.workers:
            while worker.is_alive():
                worker.join(timeout=1)

    def submit(self, func: Callable, *args, **kwargs) -> _Task:
        assert callable(func)

        task = _Task(func, *args, **kwargs)
        self.tasks.put_nowait(task)
        if len(self.workers) < self.max_workers:
            worker = threading.Thread(target=_office, args=(self.tasks,), daemon=True)
            self.workers.add(worker)
            worker.start()
        return task
