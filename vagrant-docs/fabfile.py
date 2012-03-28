import imp
from path import path as ppath
from fabric.api import *
from fabric.contrib.files import exists


fabdir = ppath(__file__).abspath().dirname()
common = imp.load_source('common', fabdir.parent/'common.py')


config = env['composer_config'] = {
    'fabdir': fabdir,
    'buildout-path': ppath('/var/local/naaya'),
    'python-bin': '/usr/bin/python2.6',
    'unix-user': 'vagrant',
    'svn-url': 'https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/Naaya',
}

if not env['hosts']:
    env['hosts'] = ['vagrant@192.168.13.28']
env['key_filename'] = fabdir/'vagrant-id-rsa'


@task
def bootstrap():
    config = env['composer_config']
    sudo("mkdir '%(buildout-path)s'" % config)
    sudo("chown %(unix-user)s: '%(buildout-path)s'" % config)
    run("virtualenv -p python2.6 "
        "--no-site-packages --distribute "
        "%(buildout-path)s" % config)


def _naaya_src():
    if not exists('%(buildout-path)s/src/Naaya' % config):
        run("mkdir -p '%(buildout-path)s/src'" % config)
        with cd('%(buildout-path)s/src' % config):
            run("git clone git://github.com/eaudeweb/Naaya.git -o github")
    else:
        with cd('%(buildout-path)s/src/Naaya' % config):
            run("git fetch github")
            run("git merge github/master --ff-only")


@task
def deploy():
    _naaya_src()
    execute(common.deploy)


shell = common.shell
