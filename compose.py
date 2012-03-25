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

    def run(self):
        self._configure()
        execute(self.shell)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('deployment')

    return parser.parse_args()


def main():
    args = parse_args()
    deployment_root = path(args.deployment).abspath()
    Composer(deployment_root).run()


if __name__ == '__main__':
    main()
