from StringIO import StringIO
from fabric.api import *
from fabric.contrib.files import exists
from path import path


env.update({
    'hosts': ['vulture'],
    'use_ssh_config': True,
    'virtualenv_bin': path('/usr/local/bin/virtualenv'),
    'sarge_home': path('/var/local/sarge'),
    'sentry_venv': path('/var/local/sarge/var/sentry-venv'),
    'sarge_bin': path('/var/local/sarge/var/sarge-venv/bin/sarge'),
})


def sarge(cmd):
    sarge_base = ("'%(sarge_bin)s' '%(sarge_home)s' " % env)
    return sudo(sarge_base + cmd)


def version_paths(version_folder):
    return {
        'sentry_version_folder': version_folder,
    }


@task
def ssh():
    open_shell()


@task
def virtualenv():
    if not exists(env['sentry_venv'] / 'bin' / 'python'):
        run("'%(virtualenv_bin)s' --distribute '%(sentry_venv)s'" % env)

    put("requirements.txt", str(env['sentry_venv']))
    run("%(sentry_venv)s/bin/pip install "
        "-r %(sentry_venv)s/requirements.txt"
        % env)


@task
def install():
    put('settings.py', str(env['sentry_version_folder'] / 'settings.py'))

    put(StringIO("exec %(sentry_venv)s/bin/sentry "
                 "--config=%(sentry_version_folder)s/settings.py "
                 "start\n" % env),
        str(env['sentry_version_folder'] / 'start.sh'), mode=0755)

    put(StringIO("{}"), str(env['sentry_version_folder'] / 'sargeapp.yaml'))


@task
def deploy():
    version_folder = path(sarge("new_version sentry"))
    with settings(**version_paths(version_folder)):
        sudo("chown -R '%(user)s': '%(sentry_version_folder)s'" % env)
        execute('install')
        sudo("chown -R zope: '%(sentry_version_folder)s'" % env)
    sarge("activate_version sentry '%s'" % version_folder)
