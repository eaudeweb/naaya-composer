from fabric.api import *


@task
def shell():
    config = env['composer_config']
    open_shell("cd '%s'" % config['buildout-path'])


@task
def bootstrap():
    config = env['composer_config']
    run("virtualenv -p python2.6 "
        "--no-site-packages --distribute "
        "%(buildout-path)s" % config)


@task
def deploy():
    config = env['composer_config']
    with cd(config['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % config, '.')
        run("'%(python-bin)s' bootstrap.py -d" % config)
        run("bin/buildout")
