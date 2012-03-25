#!/usr/bin/env python

from path import path
import fabric


class Composer(object):

    def __init__(self, root):
        self.root = root

    def run(self):
        print "composing from %s" % self.root


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
