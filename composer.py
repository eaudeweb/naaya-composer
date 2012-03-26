from fabric.api import *
import yaml


def composer_for_path(root):
    with root.joinpath('config.yaml').open('rb') as f:
        config = yaml.load(f)
    return Composer(root, config)


class Composer(object):

    def __init__(self, root, config):
        self.root = root
        self.config = config

    def _configure(self):
        env.hosts = [self.config['host']]

    def shell(self):
        open_shell("cd '%s'" % self.config['buildout_path'])

    def bootstrap(self):
        if self.config['python_system_26']:
            sudo("apt-get install -y python2.6-dev python-virtualenv")
        sudo("mkdir '%(buildout_path)s'" % self.config)
        sudo("chown vagrant: '%(buildout_path)s'" % self.config)
        run("virtualenv -p python2.6 "
            "--no-site-packages --distribute "
            "%(buildout_path)s" % self.config)

    def deploy(self):
        with cd(self.config['buildout_path']):
            paths = put('%s/buildout/*' % self.root, '.')
            run('bin/python bootstrap.py -d')
            run('bin/buildout')

    def run(self, tasks):
        self._configure()
        for task in tasks:
            execute(getattr(self, task))
