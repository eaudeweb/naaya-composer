from fabric.api import *
from path import path
from fabric.contrib.files import exists


fabdir = path(__file__).abspath().dirname()
svn_repo = 'https://svn.eionet.europa.eu/repositories/Zope'
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': path('/var/lib/jenkins/jobs/Reportek-tests-zope213/workspace'),
    'reportek-repo': svn_repo + '/trunk/Products.Reportek',
}

env['hosts'] = ['edw@power.edw.ro']


def _virtualenv(venv_path, python_bin='python2.6'):
    run("virtualenv %s --no-site-packages --distribute --python=%s" %
        (venv_path, python_bin))


def _svn_repo(repo_path, origin_url, update=True):
    if not exists(repo_path/'.svn'):
        run("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            run("svn co '%s' ." % origin_url)

    elif update:
        with cd(repo_path):
            run("svn up")


@task
def ssh():
    open_shell("cd '%(buildout-path)s'" % app)


@task
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        _virtualenv(app['buildout-path'])
    _svn_repo(app['buildout-path']/'src'/'Products.Reportek',
              app['reportek-repo'],
              update=False)
    with cd(app['buildout-path']):
        put('%(fabdir)s/buildout/*' % app, '.')
        run("curl -O 'http://eggshop.eaudeweb.ro/bootstrap.py'")
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")
