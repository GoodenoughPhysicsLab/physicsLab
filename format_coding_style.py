import os

def is_all_blank(line: str) -> str:
    for char in line:
        if char != ' ':
            return False
    return True

if __name__ == "__main__":
    for root, dirs, files in os.walk("physicsLab"):
        dirs.remove("__pycache__")

        for file in files:
            with open(f"{root}/{file}", encoding="utf-8") as f:
                lines = f.read().splitlines()

            context: str = ""
            for line in lines:
                if is_all_blank(line):
                    context += '\n'
                else:
                    context += line + '\n'
            context = context[:-1]
            with open(f"{root}/{file}", "w", encoding="utf-8") as f:            
                f.write(context)