import imp
from path import path as ppath
from fabric.api import *
from fabric.contrib.files import exists


fabdir = ppath(__file__).abspath().dirname()
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': ppath('/var/lib/jenkins/jobs/Naaya-tests-naaya-additional/workspace'),
    'trunk-eggs-repo': 'https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/',
    'bundles-repos': ['https://svn.eionet.europa.eu/repositories/Naaya/trunk/eggs/NaayaBundles-DESTINET/', ]
}

env['hosts'] = ['edw@power.edw.ro']


@task
def ssh():
    open_shell("cd '%(buildout-path)s'" % app)


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
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        _virtualenv(app['buildout-path'])
    _svn_repo(app['buildout-path']/'src'/'trunk-eggs', app['trunk-eggs-repo'])
    for bundle_repo in app['bundles-repos']:
        bundle_package = bundle_repo.strip('/').rsplit('/', 1)[-1]
        _svn_repo(app['buildout-path']/'src'/'bundles'/bundle_package, bundle_repo)
    with cd(app['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % app, '.')
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")
