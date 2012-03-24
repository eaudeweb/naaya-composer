from fabric.api import env, cd
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
    sudo('apt-get install curl -y')
    with cd('/var/local/naaya'):
        for name in ['bootstrap.py',
                     'buildout.cfg',
                     'naaya.cfg',
                     'versions-zope-2.12.18.cfg',
                     'versions.cfg']:
            url = ('https://svn.eionet.europa.eu/repositories/Naaya'
                   '/buildout/Naaya/zope212/' + name)
            run('curl -O ' + url)
        run('bin/python bootstrap.py -d')
