from fabric.api import *
import yaml


def composer_for_path(root):
    with root.joinpath('config.yaml').open('rb') as f:
        config = yaml.load(f)
    if 'composer' in config:
        [file_name, cls_name] = config['composer'].split(':')
        module = {}
        execfile(root.joinpath(file_name), module)
        cls = module[cls_name]
    else:
        cls = Composer
    return cls(root, config)


class Composer(object):

    def __init__(self, root, config):
        self.root = root
        self.config = config

    def shell(self):
        open_shell("cd '%s'" % self.config['buildout-path'])

    def bootstrap(self):
        sudo("mkdir '%(buildout-path)s'" % self.config)
        sudo("chown %(unix-user)s: '%(buildout-path)s'" % self.config)
        run("virtualenv -p python2.6 "
            "--no-site-packages --distribute "
            "%(buildout-path)s" % self.config)

    def deploy(self):
        with cd(self.config['buildout-path']):
            paths = put('%s/buildout/*' % self.root, '.')
            run('bin/python bootstrap.py -d')
            run('bin/buildout')

    def run(self, tasks):
        for task in tasks:
            execute(getattr(self, task), hosts=[self.config['host']])
