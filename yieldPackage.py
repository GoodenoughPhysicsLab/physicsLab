#coding=utf-8
import os
import git

if __name__ == '__main__':

    string = input('upgrade package to pypi?(y/n)')
    if string == 'y':
        os.system('D:')
        os.system('cd D:\\program physicsLab')
        os.system('py setup.py sdist bdist_wheel')
        # os.system('twine upload hub/dist/*')
        # 更新python包
        # pip install --upgrade xxx

    string = input('push file to hub?(y/n)')
    if string == 'y':
        repo = git.Git("D:\\program physicsLab")
        repo.checkout('master')
        repo.merge('dev')
        repo.push('gitee', 'master')
        repo.push('github', 'master')
        repo.checkout('dev')
