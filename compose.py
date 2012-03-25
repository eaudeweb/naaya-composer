#!/usr/bin/env python

from fabric.api import *
from path import path
import yaml


env.use_ssh_config = True


class Composer(object):

    def __init__(self, root):
        self.root = root

    def _configure(self):
        with self.root.joinpath('config.yaml').open('rb') as f:
            self.config = yaml.load(f)
        env.hosts = [self.config['host']]

    def shell(self):
        open_shell("cd '%s'" % self.config['buildout_path'])

    def bootstrap(self):
        sudo("apt-get install -y python2.6-dev python-virtualenv curl")
        sudo("mkdir '%(buildout_path)s'" % self.config)
        sudo("chown vagrant: '%(buildout_path)s'" % self.config)
        run("virtualenv -p python2.6 "
            "--no-site-packages --distribute "
            "%(buildout_path)s" % self.config)

    def run(self, tasks):
        self._configure()
        for task in tasks:
            execute(getattr(self, task))


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('deployment')
    parser.add_argument('tasks', nargs='*')

    return parser.parse_args()


def main():
    args = parse_args()
    deployment_root = path(args.deployment).abspath()
    try:
        Composer(deployment_root).run(args.tasks)
    finally:
        import fabric.network
        fabric.network.disconnect_all()


if __name__ == '__main__':
    main()
