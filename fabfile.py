import os.path
from fabric.api import *


env.use_ssh_config = True
env.hosts = ['vagrant@192.168.13.29']


@task
def shell():
    open_shell('cd /var/local/naaya')


@task
def bootstrap():
    sudo('apt-get install python-dev -y')
    sudo('apt-get install python-virtualenv -y')
    sudo('mkdir /var/local/naaya')
    sudo('chown vagrant: /var/local/naaya')
    run('virtualenv -p python2.6 '
        '--no-site-packages --distribute '
        '/var/local/naaya')
    sudo('apt-get install curl -y')


@task
def deploy():
    with cd('/var/local/naaya'):
        paths = put('buildout/*', '.')
        run('bin/python bootstrap.py -d')
        run('bin/buildout')
