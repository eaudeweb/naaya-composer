from fabric.api import *
from path import path
from fabric.contrib.files import exists


fabdir = path(__file__).abspath().dirname()
svn_repo = 'https://svn.eionet.europa.eu/repositories/Zope'
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': path('/var/local/cdr-zope213'),
    'reportek-repo': svn_repo + '/trunk/Products.Reportek',
}

env['hosts'] = ['edw@martini.edw.ro']


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


def _svn_repo(repo_path, origin_url, update=True):
    if not exists(repo_path/'.svn'):
        run("mkdir -p '%s'" % repo_path)
        with cd(repo_path):
            run("svn co '%s' ." % origin_url)

    elif update:
        with cd(repo_path):
            run("svn up")


def _product(product_path, tgz_url):
    if not exists(product_path.parent):
        run("mkdir -p '%s'" % product_path.parent)
    if not exists(app['buildout-path']/'products'/product_path):
        with cd(app['buildout-path']/'products'):
            run("curl '%s' | tar xzf -" % tgz_url)


@task
def ssh():
    open_shell("cd '%(buildout-path)s'" % app)


@task
def deploy():
    if not exists(app['buildout-path']/'bin'/'python'):
        _virtualenv(app['buildout-path'])

    products_path = app['buildout-path']/'products'
    _svn_repo(app['buildout-path']/'src'/'Products.Reportek',
              app['reportek-repo'])
    _product(products_path/'LDAPUserFolder',
             "http://eggshop.eaudeweb.ro/LDAPUserFolder-cdr2.tgz")
    _svn_repo(products_path/'XMLRPCMethod',     svn_repo + '/trunk/XMLRPCMethod')
    _svn_repo(products_path/'SmallObligations', svn_repo + '/trunk/SmallObligations')
    _svn_repo(products_path/'RDFGrabber',       svn_repo + '/trunk/RDFGrabber')

    with cd(app['buildout-path']):
        paths = put('%(fabdir)s/buildout/*' % app, '.')
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")


@task
def zopectl(cmd):
    with cd(app['buildout-path']):
        run("bin/zope-instance %s" % cmd, pty=False)
