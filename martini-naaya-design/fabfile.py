from path import path as ppath
from fabric.api import *
from fabric.contrib.files import exists


app = env.app = {
    'fabdir': ppath(__file__).abspath().dirname(),
    'buildout-path': ppath('/var/local/naaya-design'),
    'naaya-repo': 'https://github.com/eaudeweb/Naaya.git',
    'talkback-repo': 'https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/naaya.content.talkback',
    'photoarchive-repo': 'https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/naaya.photoarchive',
    'forum-repo': 'https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/Products.NaayaForum',
}

env['hosts'] = ['edw@martini.edw.ro']


@task
def ssh():
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

def _svn_repo(repo_path, origin_url, update=True):
    if not exists(repo_path/'.svn'):
        run("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            run("svn co '%s' ." % origin_url)

    elif update:
        with cd(repo_path):
            run("svn up")

@task
def install():
    run("mkdir -p '%(buildout-path)s'" % app)
    _git_repo(app['buildout-path']/'src'/'Naaya', app['naaya-repo'], update=False)
    _svn_repo(app['buildout-path']/'src'/'naaya.photoarchive',
            app['photoarchive-repo'], update=False)
    _svn_repo(app['buildout-path']/'src'/'Products.NaayaForum',
            app['forum-repo'], update=False)
    with cd(app['buildout-path']):
        put('%(fabdir)s/buildout/*' % app, '.')
        if not exists(app['buildout-path']/'bin'/'python'):
            _virtualenv('.')
        if not exists(app['buildout-path']/'bin'/'buildout'):
            run("bin/python bootstrap.py -d")
        run("bin/buildout")


@task
def zopectl(cmd):
    with cd(app['buildout-path']):
        run("bin/zope-instance %s" % cmd, pty=False)


@task
def deploy():
    execute('install')
    execute('zopectl', 'stop')
    execute('zopectl', 'start')

@task
def restart():
    execute('zopectl', 'stop')
    execute('zopectl', 'start')
