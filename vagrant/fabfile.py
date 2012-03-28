import imp
from path import path as ppath
from fabric.api import *
from fabric.contrib.files import exists


fabdir = ppath(__file__).abspath().dirname()
common = imp.load_source('common', fabdir.parent/'common.py')


config = env['composer_config'] = {
    'fabdir': fabdir,
    'buildout-path': ppath('/var/local/naaya'),
    'unix-user': 'vagrant',
}

if not env['hosts']:
    env['hosts'] = ['vagrant@192.168.13.29']
env['key_filename'] = fabdir/'vagrant-id-rsa'


@task
def initialize():
    config = env['composer_config']
    sudo("mkdir '%(buildout-path)s'" % config)
    sudo("chown %(unix-user)s: '%(buildout-path)s'" % config)
    execute(common.initialize)


shell = common.shell
deploy = common.deploy
