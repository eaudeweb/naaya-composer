from fabric.api import *
from path import path
from fabric.contrib.files import exists


fabdir = path(__file__).abspath().dirname()
svnurl = 'https://svn.eionet.europa.eu/repositories/Zope'
app = env.app = {
    'fabdir': fabdir,
    'buildout-path': path('/var/local/cdr-zope213'),
    'reportek-repo': svnurl + '/trunk/Products.Reportek',
}

#env['hosts'] = ['edw@akvavit.edw.ro']
env['use_ssh_config'] = True
env['hosts'] = ['edw@akvavit']


### debian packages:
# sudo bzip2 curl
# git git-core git-svn subversion
# build-essential python2.6 python2.6-dev python-virtualenv
# libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev


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
              app['reportek-repo'],
              update=False)
    _svn_repo(products_path/'XMLRPCMethod',     svnurl+'/trunk/XMLRPCMethod')
    _svn_repo(products_path/'SmallObligations', svnurl+'/trunk/SmallObligations')
    _svn_repo(products_path/'RDFGrabber',       svnurl+'/trunk/RDFGrabber')

    with cd(app['buildout-path']):
        put('%(fabdir)s/buildout/*' % app, '.')
        run("curl -O 'http://eggshop.eaudeweb.ro/bootstrap.py'")
        run("'%(buildout-path)s/bin/python' bootstrap.py -d" % app)
        run("bin/buildout")


@task
def zopectl(cmd):
    with cd(app['buildout-path']):
        run("bin/zope-instance %s" % cmd, pty=False)
