from fabric.api import env
from fabric.operations import open_shell


env.use_ssh_config = True
env.hosts = ['vagrant@192.168.13.29']


def shell():
    open_shell()
