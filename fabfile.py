
from fabric.api import local


def test():
    local('py.test')

def build_package():
    test()
    local('python setup sdist')
