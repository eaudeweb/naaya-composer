from fabric.api import *
from path import path


fabdir = path(__file__).abspath().dirname()
svn_repo = 'https://svn.eionet.europa.eu/repositories/Zope'
app = {
    'fabdir': fabdir,
    'buildout-path': path('/var/lib/jenkins/jobs/Reportek-tests/workspace'),
    'reportek-repo': svn_repo + '/trunk/Products.Reportek',
    'python-bin': path('/usr/local/Python-2.7.3/bin/python'),
    'username': 'jenkins',
}

env['hosts'] = ['whiteshark.eea.europa.eu']


def jsudo(*args, **kwargs):
    kwargs['user'] = app['username']
    return sudo(*args, **kwargs)


def exists(some_path):
    cmd = 'test -e "$(echo %s)"' % some_path
    with settings(hide('everything'), warn_only=True):
        return not jsudo(cmd).failed


def _svn_repo(repo_path, origin_url, update=True):
    if not exists(repo_path/'.svn'):
        jsudo("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            jsudo("svn co '%s' ." % origin_url)

    elif update:
        with cd(repo_path):
            jsudo("svn up")


@task
def ssh():
    open_shell("cd '%(buildout-path)s'" % app)


@task
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        with cd(app['buildout-path']):
            jsudo("/usr/local/bin/virtualenv '%s' "
                  "--no-site-packages --distribute --python='%s'" %
                  (app['buildout-path'], app['python-bin']))
    _svn_repo(app['buildout-path']/'src'/'Products.Reportek',
              app['reportek-repo'],
              update=False)
    with cd(app['buildout-path']):
        put('%(fabdir)s/buildout.cfg' % app, '.', use_sudo=True)
        jsudo("curl -O 'http://eggshop.eaudeweb.ro/bootstrap15.py'")
        jsudo("'%(buildout-path)s/bin/python' bootstrap15.py -d" % app)
        jsudo("bin/buildout")
