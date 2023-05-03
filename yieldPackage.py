#coding=utf-8
import os
import git
import viztracer as vt # 研究git包用的

if __name__ == "__main__":
    string = input("upgrade package to pypi?(y/n)")
    if string == "y":
        os.system("cd D:\\program_physicsLab")
        os.system("D:")
        os.system("py setup.py sdist bdist_wheel")
        # os.system("twine upload dist/*")
        # 更新python包
        # pip install --upgrade xxx

    string = input("push file to hub?(y/n)")
    if string == "y":
        tracer = vt.VizTracer()
        tracer.start()

        repo = git.Git("D:\\program physicsLab")
        repo.checkout("master")
        repo.merge("--squash", "dev")
        # commit
        commitStr = None
        while True:
            commitStr = input("input commit massage: ")
            if commitStr is not None:
                break
        repo.commit("-m", commitStr)

        repo.push("gitee", "master")
        repo.push("github", "master")
        repo.checkout("dev")
        repo.merge("master")

        tracer.stop()
        tracer.save()
