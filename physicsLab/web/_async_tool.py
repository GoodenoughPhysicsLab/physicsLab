# -*- coding: utf-8 -*-
import asyncio
import queue
import threading
from abc import abstractmethod
from physicsLab._typing import Iterator, final

class _EndOfQueue:
    def __new__(cls):
        return cls

class AsyncTool:
    @abstractmethod
    async def __aiter__(self):
        raise NotImplementedError

    @final
    async def _async_main(self):
        async for res in self:
            self._results.put_nowait(res)
        self._results.put_nowait(_EndOfQueue)

    def __iter__(self) -> Iterator[dict]:
        self._results = queue.SimpleQueue()
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
