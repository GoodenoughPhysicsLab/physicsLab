# -*- coding: utf-8 -*-
''' 生成 class User 的所有方法的api的文档
'''
import os
import inspect

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE: str = os.path.join(os.path.dirname(SCRIPT_DIR), "docs", "docsgen", "user-method.md")

import sys
sys.path.append(SCRIPT_DIR)
sys.path.append(os.path.dirname(SCRIPT_DIR))

from physicsLab import web

# TODO 生成markdown目录
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
        method_signature: inspect.Signature = inspect.signature(fn_obj)
        async_method_signature: inspect.Signature = inspect.signature(async_methods['async_' + fn_name])
        assert method_signature.parameters == async_method_signature.parameters, fn_name

        doc: str = fn_obj.__doc__
        context += f"\n## {doc.splitlines()[0]}\n"
        context += f"```Python\ndef {fn_name}{method_signature}\n```\n"
        for line in doc.split('\n')[1:]:
            context += f"{(line + '  ').lstrip()}\n"

        context += f"对应的协程风格的api:\n" \
            f"```Python\n" \
            f"async def {'async_' + fn_name}{async_method_signature}\n" \
            f"```\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(context)

if __name__ == "__main__":
    main()
