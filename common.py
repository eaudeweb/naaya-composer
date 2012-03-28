from fabric.api import *
from fabric.contrib.files import exists


@task
def shell():
    config = env['composer_config']
    open_shell("cd '%s'" % config['buildout-path'])


def _virtualenv(venv_path, python_bin='python2.6'):
    run("virtualenv %s --no-site-packages --distribute --python=%s" %
        (venv_path, python_bin))


@task
def initialize():
    _virtualenv(env['composer_config']['buildout-path'])


@task
def deploy():
    config = env['composer_config']
    if not exists(config['buildout-path']):
        execute('initialize')
    with cd(config['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % config, '.')
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % config)
        run("bin/buildout")
