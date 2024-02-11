import os

def main():
    for root, dirs, files in os.walk("physicsLab"):
        dirs.remove("__pycache__")

        for file in files:
            with open(f"{root}/{file}", encoding="utf-8") as f:
                lines = f.read().splitlines()

            context: str = ""
            for line in lines:
                while line.endswith(' '):
                    line = line[:-1]

                context += line + '\n'
            context = context[:-1]
            with open(f"{root}/{file}", "w", encoding="utf-8") as f:
                f.write(context)

if __name__ == "__main__":
    main()