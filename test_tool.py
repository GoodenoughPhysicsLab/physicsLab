import time
import subprocess
from typing import Callable

def timer_dec(func: Callable):
    def res(*args, **kwargs):
        import time

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(end - start)
        return result
    
    return res

class Timer:
    def __enter__(self):
        self.start = time.time()
    
    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is None:
            self.end = time.time()
            print("time:", self.end - self.start)


def viz_dec(func: Callable):
    def res(*args, **kwargs):
        import viztracer as viz

        tracer = viz.VizTracer()
        tracer.start()

        result = func(*args, **kwargs)

        tracer.stop()
        tracer.save()
        subprocess.call(["vizviewer", "result.json"])

        return result
    return res

class Viz:
    def __enter__(self):
        import viztracer as viz

        self.tracer = viz.VizTracer()
        self.tracer.start()

    def __exit__(self, exc_type, exc_val, traceback):
        self.tracer.stop()
        self.tracer.save()
        subprocess.call(["vizviewer", "result.json"])