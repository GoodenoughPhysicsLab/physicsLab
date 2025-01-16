# -*- coding: utf-8 -*-
import os
import inspect

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE: str = os.path.join(os.path.dirname(SCRIPT_DIR), "docs", "docsgen", "user-method.md")

import sys
sys.path.append(os.path.dirname(SCRIPT_DIR))

from physicsLab import web

def main():
    async_methods: dict = {}
    for co_fn_name, co_fn_obj in inspect.getmembers(web.User, inspect.iscoroutinefunction):
        async_methods[co_fn_name] = co_fn_obj

    context: str = ""

    for fn_name, fn_obj in inspect.getmembers(
            web.User,
            predicate=lambda obj: inspect.isfunction(obj) \
                and not obj.__name__.startswith('_') \
                and not obj.__name__.startswith("async")
    ):
        doc: str = fn_obj.__doc__
        context += f"\n## {doc.splitlines()[0]}\n"
        context += f"```Python\ndef {fn_name}{inspect.signature(fn_obj)}\n```\n"
        for line in doc.split('\n')[1:]:
            context += f"{(line + '  ').lstrip()}\n"

        context += f"\n对应的协程风格的api:\n" \
            f"```Python\n" \
            f"async def {'async_' + fn_name}{inspect.signature(async_methods['async_' + fn_name])}\n" \
            f"```\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(context)

if __name__ == "__main__":
    main()
