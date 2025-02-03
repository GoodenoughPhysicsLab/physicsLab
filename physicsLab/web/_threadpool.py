# -*- coding: utf-8 -*-
''' 在 Python3.14之前, Thread.join 在 Windows 上会阻塞异常的传播, 详见:
        https://www.bilibili.com/video/BV1au411q7LN/?spm_id_from=333.999.0.0

    因此, 我无法直接使用ThreadPoolExecutor, 我就自己写了一个线程池
'''
import queue
from threading import Thread
from enum import Enum, unique
from physicsLab._typing import List, Callable, Self, Any

class CanceledError(Exception):
    ''' Task have been canceled '''
    pass

class _EndOfQueue:
    def __new__(cls):
        return _EndOfQueue

@unique
class _Status(Enum):
    ''' task's status '''
    wait = 0
    running = 1
    done = 2
    cancelled = 3

class _Task:
    def __init__(self, func: Callable, args: tuple, kwargs: dict) -> None:
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.res: Any = None
        self.exception = None
        self.status: _Status = _Status.wait

    def has_result(self) -> bool:
        return self.status == _Status.done

    def result(self):
        if self.status == _Status.cancelled:
            raise CanceledError
        while not self.has_result():
            pass

        if self.exception is not None:
            raise self.exception
        else:
            return self.res

class ThreadPool:
    def __init__(self, *, max_workers: int) -> None:
        ''' @param max_workers: 最大线程数
        '''
        if not isinstance(max_workers, int):
            raise TypeError
        if max_workers <= 0:
            raise ValueError

        self.max_workers = max_workers
        self.task_queue = queue.SimpleQueue()
        self.threads: List[Thread] = []

    def _office(self):
        ''' workers work here '''
        while True:
            try:
                _task = self.task_queue.get_nowait()
            except queue.Empty:
                continue
            if _task is _EndOfQueue:
                self.task_queue.put_nowait(_EndOfQueue)
                return
            _task.status = _Status.running
            try:
                _task.res = _task.func(*_task.args, **_task.kwargs)
            except Exception as e:
                _task.exception = e
            finally:
                _task.status = _Status.done

    def submit(self, func, *args, **kwargs) -> _Task:
        ''' submit a task
            @param func: function to be submitted
        '''
        if not callable(func):
            raise TypeError

        task = _Task(func, args, kwargs)
        self.task_queue.put_nowait(task)
        if len(self.threads) < self.max_workers:
            worker = Thread(target=self._office, daemon=True)
            self.threads.append(worker)
            worker.start()

        return task

    def submit_end(self) -> None:
        ''' users should call this method after all tasks are submitted
        '''
        self.task_queue.put_nowait(_EndOfQueue)

    def wait(self) -> None:
        ''' blocking until all tasks are done
        '''
        for thread in self.threads:
            while thread.is_alive():
                thread.join(timeout=2)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.wait()
