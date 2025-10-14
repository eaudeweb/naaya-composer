from path import path as ppath
from fabric.api import env

env.hosts = ['edw@pigeon.eea.europa.eu']

env.app['forum_repo'] = ppath('/var/local/naaya/forum')
env.app['projects_repo'] = ppath('/var/local/naaya/projects')
env.app['archives_repo'] = ppath('/var/local/naaya/archives')

__all__ = ()
