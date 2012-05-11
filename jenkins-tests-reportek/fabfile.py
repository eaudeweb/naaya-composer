from fabric.api import *
from path import path
from fabric.contrib.files import exists


fabdir = path(__file__).abspath().dirname()
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': path('/var/lib/jenkins/jobs/Reportek-tests-zope210/workspace'),
    'reportek-repo': 'https://github.com/eaudeweb/Products.Reportek.git',
    'reportek-branch': 'alexm',
}

env['hosts'] = ['edw@power.edw.ro']


def _virtualenv(venv_path, python_bin='python2.6'):
    run("virtualenv %s --no-site-packages --distribute --python=%s" %
        (venv_path, python_bin))


def _git_repo(repo_path, origin_url, update=True, branch='master'):
    if not exists(repo_path/'.git'):
        run("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            run("git clone '%s' ." % origin_url)
            run("git checkout %s" % branch)

    elif update:
        with cd(repo_path):
            run("git fetch origin")
            run("git merge origin/%s --ff-only" % branch)


@task
def ssh():
    open_shell("cd '%(buildout-path)s'" % app)


@task
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        _virtualenv(app['buildout-path'], python_bin='python2.4')
    _git_repo(app['buildout-path']/'src'/'Products.Reportek',
              app['reportek-repo'],
              branch=app['reportek-branch'])
    with cd(app['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % app, '.')
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")
