# 将import了physicsLab的文件的第一行添加上 #coding=utf-8
def utf8_coding(func):
    def result(string: str) -> None:
        try:
            import sys
            s = ''
            with open(sys.argv[0], encoding='utf-8') as f:
                s = f.read()
            if not s.replace('\n', '').startswith('#coding=utf-8'):
                with open(sys.argv[0], 'w', encoding='utf-8') as f:
                    if s.startswith('\n'):
                        f.write(f'#coding=utf-8{s}')
                    else:
                        f.write(f'#coding=utf-8\n{s}')
        except:
            pass
        func(string)
    return result