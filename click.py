"""
Provides a Click based switch class
"""

from mininet.node import Switch
from mininet.util import errFail

class ClickUserSwitch(Switch):
    binary = 'click'

    def __init__(self, name, config_file, log_file='/dev/null', inNamespace=True, parameters={}, **params):
        Switch.__init__( self, name, inNamespace=inNamespace, **params )
        self.config_file = config_file
        self.log_file = log_file
        self.params = parameters

    def start(self, controllers):
        cmd = [ClickUserSwitch.binary]
        for name in self.params:
            cmd.append(name + '=' + self.params[name])
        cmd.append(self.config_file)
        if self.log_file:
            cmd.append('> "%s" 2>&1' % self.log_file)
        self.cmd(" ".join(cmd) + " &")

    def stop(self):
        self.cmd('kill %click')
        pass

class ClickKernelSwitch(Switch):
    install_cmd = 'click-install'
    uninstall_cmd = 'click-uninstall'

    def __init__(self, name, config_file, log_file='/dev/null', **params):
        Switch.__init__( self, name, **params )
        self.config_file = config_file
        self.log_file = log_file

    def start(self, controllers):
        pass

    @classmethod
    def batchStartup(cls, switches, run=errFail):
        print("click startup")
        cat = ['cat'] + [s.config_file for s in switches if s.config_file]
        run(' '.join(cat) + ' | ' + cls.install_cmd, shell=True)
        return switches

    @classmethod
    def batchShutdown(cls, switches, run=errFail):
        print("click shutdown")
        run(ClickKernelSwitch.uninstall_cmd)
        return switches

