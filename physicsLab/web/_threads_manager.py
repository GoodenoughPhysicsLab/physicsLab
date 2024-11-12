# -*- coding: utf-8 -*-
''' .webutils.py has used ThreadPoolExecutor everywhere.
    But, I have met some problems and found a solution:
        https://www.bilibili.com/video/BV1au411q7LN/?spm_id_from=333.999.0.0

    However, I can't apply this simple solution to built-in ThreadPoolExecutor.
    That's why I write this module.
'''
import os
import threading
from physicsLab.typehint import Optional, Callable, Set, Self

class _Task(threading.Thread):
    def __init__(self, func: Callable, *args, **kwargs) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        super().__init__(target=func, args=args, kwargs=kwargs)
        self.daemon = True

    def run(self):
        self.func_res = self.func(*self.args, **self.kwargs)

    def result(self):
        while self.is_alive():
            self.join(timeout=2)
        return self.func_res

class ThreadsManager: # TODO: makes it a thread-pool
    def __init__(self, max_workers: Optional[int] = None) -> None:
        assert isinstance(max_workers, int) or max_workers is None

        if max_workers is not None and max_workers < 1:
            raise ValueError("max_workers must be greater than 0")
        elif max_workers is None:
            max_workers = min(32, (os.cpu_count() or 1) + 4)
        self.max_workers = max_workers

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    def submit(self, func: Callable, *args, **kwargs) -> _Task:
        assert callable(func)

        thread = _Task(func, *args, **kwargs)
        thread.start()
        return thread
