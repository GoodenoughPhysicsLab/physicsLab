import os
import git

if __name__ == '__main__':
    repo = git.Git("/hub")
    repo.checkout('master')
    repo.merge('dev')
    repo.push('gitee', 'master')
    repo.push('github', 'master')
    repo.checkout('dev')

    input('update setup.py?')

    os.system('D:')
    os.system('cd D:\\program physicsLab\\hub')
    os.system('py setup.py sdist bdist_wheel')
    # os.system('twine upload dist/*')
