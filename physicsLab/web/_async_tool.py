# -*- coding: utf-8 -*-
''' .webutils.py has used ThreadPoolExecutor everywhere.
    But, I have met some problems and found a solution:
        https://www.bilibili.com/video/BV1au411q7LN/?spm_id_from=333.999.0.0

    However, I can't apply this simple solution to built-in ThreadPoolExecutor.
    That's why I write this module.
'''
import asyncio
import queue
import threading

class _EndOfQueue:
    def __new__(cls):
        return cls

class AsyncTool:
    def __init__(self):
        self._results = queue.SimpleQueue()

    def _put_res(self, res):
        self._results.put_nowait(res)

    def _put_end(self):
        self._results.put_nowait(_EndOfQueue)

    def __iter__(self):
        t = threading.Thread(target=asyncio.run, args=(self._async_main(),), daemon=True)
        t.start()
        while True:
            if self._results.qsize() == 0:
                continue

            res = self._results.get_nowait()
            if res is _EndOfQueue:
                break
            yield res

        while t.is_alive():
            t.join(timeout=2)
