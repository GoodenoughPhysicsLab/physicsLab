from typing import Callable

def culculate_time(func: Callable):
    def res(*args, **kwargs):
        import time

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(end - start)
        return result
    
    return res

def viz(func: Callable):
    def res(*args, **kwargs):
        import viztracer

        tracer = viztracer.VizTracer()
        tracer.start()

        result = func(*args, **kwargs)

        tracer.stop()
        tracer.save()

        return result
    return res