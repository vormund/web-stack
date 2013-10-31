import os, time, sys
from util import run

class VagrantWrapper(object):
    """ Small wrapper around some commonly used vagrant operations """

    def vagrant(self, operation):
        run('vagrant %s' % operation)

    def up(self):
        self.vagrant('up')

        # Wait for VirtualBox tools to come online
        if not os.environ.get('VAGRANT_DEFAULT_PROVIDER') or os.environ.get('VAGRANT_DEFAULT_PROVIDER') == 'virtualbox':            
            # Wait for VirtualBox to restart
            time.sleep(30)

            while run('vagrant ssh --command "pgrep -f VBoxService"', returncode=True, echo=False):
                sys.stdout.write(".")
            print "."

        self.vagrant('reload')

    def destroy(self):
        self.vagrant('destroy')
