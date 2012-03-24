import os.path
from fabric.api import *


env.use_ssh_config = True
env.hosts = ['vagrant@192.168.13.29']


LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))


def shell():
    open_shell('cd /var/local/naaya')


def bootstrap():
    sudo('apt-get install python-dev -y')
    sudo('apt-get install python-virtualenv -y')
    sudo('mkdir /var/local/naaya')
    sudo('chown vagrant: /var/local/naaya')
    run('virtualenv -p python2.6 '
        '--no-site-packages --distribute '
        '/var/local/naaya')
    sudo('apt-get install curl -y')

def deploy():
    with cd('/var/local/naaya'):
        paths = put(os.path.join(LOCAL_ROOT, 'buildout') + '/*', '.')
        run('bin/python bootstrap.py -d')
        run('bin/buildout')
