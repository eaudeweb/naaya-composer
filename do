#!/usr/bin/env python

from path import path
import fabric.api
import fabric.network
import composer


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('deployment')
    parser.add_argument('tasks', nargs='*')

    return parser.parse_args()


def main():
    args = parse_args()
    deployment_root = path(args.deployment).abspath()
    c = composer.composer_for_path(deployment_root)
    fabric.api.env.use_ssh_config = True
    try:
        c.run(args.tasks)
    finally:
        fabric.network.disconnect_all()


if __name__ == '__main__':
    main()
