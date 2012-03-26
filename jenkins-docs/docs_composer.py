from fabric.api import *
from fabric.contrib.files import exists
import composer


class DocsComposer(composer.Composer):

    def bootstrap(self):
        run("virtualenv -p python2.6 "
            "--no-site-packages --distribute "
            "%(buildout-path)s" % self.config)

    def _naaya_src(self):
        if not exists('%(buildout-path)s/src/Naaya' % self.config):
            run("mkdir -p '%(buildout-path)s/src'" % self.config)
            with cd('%(buildout-path)s/src' % self.config):
                run("git clone git://github.com/eaudeweb/Naaya.git -o github")
        else:
            with cd('%(buildout-path)s/src/Naaya' % self.config):
                run("git fetch github")
                run("git merge github/master --ff-only")

    def deploy(self):
        self._naaya_src()
        super(DocsComposer, self).deploy()
