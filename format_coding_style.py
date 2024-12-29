import os

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    for root, dirs, files in os.walk("physicsLab"):
        try:
            dirs.remove("__pycache__")
        except ValueError:
            pass

        for file in files:
            with open(os.path.join(root, file), encoding="utf-8") as f:
                lines = f.read().splitlines()

            if len(lines) == 0 or lines[0] != "# -*- coding: utf-8 -*-":
                lines.insert(0, "# -*- coding: utf-8 -*-")

            context: str = ""
            for line_num, line in enumerate(lines):
                while line.endswith(' '):
                    line = line[:-1]

                if len(line) > 120:
                    print(f"{os.path.join(root, file)} {line_num + 1}: this line is TOO LONG({len(line)}/120)")

                context += line + '\n'
            context = context[:-1]
            while context.endswith('\n'):
                context = context[:-1]
            if not context.endswith('\n'):
                context += '\n'
            with open(f"{root}/{file}", "w", encoding="utf-8") as f:
                f.write(context)

if __name__ == "__main__":
    main()
