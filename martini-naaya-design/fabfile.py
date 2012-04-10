import imp
from path import path as ppath
from fabric.api import *
from fabric.contrib.files import exists


fabdir = ppath(__file__).abspath().dirname()
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': ppath('/var/local/naaya-design'),
    'naaya-repo': 'https://github.com/eaudeweb/Naaya.git',
}

env['hosts'] = ['edw@martini.edw.ro']


@task
def shell():
    open_shell("cd '%(buildout-path)s'" % app)


def _virtualenv(venv_path, python_bin='python2.6'):
    run("virtualenv %s --no-site-packages --distribute --python=%s" %
        (venv_path, python_bin))


def _git_repo(repo_path, origin_url, update=True):
    if not exists(repo_path/'.git'):
        run("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            run("git clone '%s' ." % origin_url)

    elif update:
        with cd(repo_path):
            run("git fetch origin")
            run("git merge origin/master --ff-only")


@task
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        _virtualenv(app['buildout-path'])
    _git_repo(app['buildout-path']/'src'/'Naaya', app['naaya-repo'],
              update=False)
    with cd(app['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % app, '.')
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")


@task
def zopectl(cmd):
    with cd(app['buildout-path']):
        run("bin/zope-instance %s" % cmd)
