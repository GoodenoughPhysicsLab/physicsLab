# -*- coding: utf-8 -*-
''' 生成所有元件的文档
'''
import os
import inspect

SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE: str = os.path.join(os.path.dirname(SCRIPT_DIR), "docs", "docsgen", "elements.md")

import sys
sys.path.append(SCRIPT_DIR)
sys.path.append(os.path.dirname(SCRIPT_DIR))

from physicsLab import *

def get_all_elements(root):
    for cls in root.__subclasses__():
        if len(cls.__subclasses__()) == 0:
            yield cls
        else:
            yield from get_all_elements(cls)

def main():
    context = ""

    circuit_table: str = ""
    circuit_detailed_info: str = ""
    for cls in get_all_elements(CircuitBase):
        circuit_detailed_info += f'''
## <h2 id="{cls.__name__}"> {cls.__name__} </h2>
```Python
class {cls.__name__}(CircuitBase):
    def __init__{inspect.signature(cls.__init__)}
```
'''
        if cls.__init__.__doc__ is not None:
            for line in cls.__init__.__doc__.splitlines():
                circuit_detailed_info += f"{line.strip()}  \n"

        pins = []
        for name, obj in inspect.getmembers(cls):
            if isinstance(obj, property):
                property_type = obj.fget.__annotations__.get('return')
                if isinstance(property_type, type(Pin)):
                    pins.append(name)
            elif (inspect.isfunction(obj) or inspect.ismethod(obj)) and not name.startswith('_'):
                circuit_detailed_info += f'''
### {name}
```Python
    def {name}{inspect.signature(obj)}
```
'''
                if obj.__doc__ is not None:
                    for line in obj.__doc__.splitlines():
                        circuit_detailed_info += f"{line.strip()}  \n"

        circuit_table += f'''
    <tr>
        <td> <a href="#{cls.__name__}">{cls.zh_name()}</a> </td>
        <td>{cls.__name__}</td>
        <td>{pins}</td>
    </tr>'''

    context += f'''
## 电学元件

<table border="1">
<thead>
    <tr>
        <th>中文名</th>
        <th>类名</th>
        <th>引脚</th>
    </tr>
</thead> <tbody>{circuit_table}
</tbody>
</table>
'''

    planet_table = ""
    with Experiment(OpenMode.crt, "__test__", ExperimentType.Celestial, force_crt=True) as expe:
        for cls in get_all_elements(PlanetBase):
            planet_table += f'''
    <tr>
        <td>{cls(0, 0, 0).data['Name']}</td>
        <td>{cls.__name__}</td>
    </tr>'''
        expe.close(delete=True)

    context += f'''
## 天体

<table border="1">
<thead>
    <tr>
        <th>中文名</th>
        <th>类名</th>
    </tr>
</thead> <tbody>{planet_table}
</tbody>
</table>
'''

    context += circuit_detailed_info

    with open(OUTPUT_FILE, 'w', encoding="utf-8") as f:
        f.write(context)

if __name__ == "__main__":
    main()
