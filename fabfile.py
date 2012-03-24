from fabric.api import env
from fabric.operations import open_shell, run, sudo


env.use_ssh_config = True
env.hosts = ['vagrant@192.168.13.29']


def shell():
    open_shell()


def bootstrap():
    sudo('apt-get install python-virtualenv -y')
    sudo('mkdir /var/local/naaya')
    sudo('chown vagrant: /var/local/naaya')
    run('virtualenv -p python2.6 '
        '--no-site-packages --distribute '
        '/var/local/naaya')
