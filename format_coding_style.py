import os

def main():
    for root, dirs, files in os.walk("physicsLab"):
        try:
            dirs.remove("__pycache__")
        except ValueError:
            pass

        for file in files:
            with open(f"{root}/{file}", encoding="utf-8") as f:
                lines = f.read().splitlines()

            context: str = ""
            for line_num, line in enumerate(lines):
                while line.endswith(' '):
                    line = line[:-1]

                if len(line) > 110:
                    print(f"{root}/{file} {line_num + 1}: this line is TOO LONG({len(line)}/110)")

                context += line + '\n'
            context = context[:-1]
            with open(f"{root}/{file}", "w", encoding="utf-8") as f:
                f.write(context)

if __name__ == "__main__":
    main()
