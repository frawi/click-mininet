#!/usr/bin/python

"""
This example shows how to create an empty Mininet object
(without a topology object) and add nodes to it manually.
"""

import sys
import os
import os.path

os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path.append('..')

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from click import ClickKernelSwitch, ClickUserSwitch

def emptyNet():

    "Create an empty network and add nodes to it."

    net = Mininet( controller=Controller, switch=ClickUserSwitch, link=TCLink )
    setLogLevel('debug')

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1')
    h2 = net.addHost( 'h2')

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1', config_file='switch.click', log_file='s1.log', parameters=dict(HOST='s1-eth1', NETWORK='s1-eth2') )
    s2 = net.addSwitch( 's2', config_file='switch.click', log_file='s2.log', parameters=dict(HOST='s2-eth2', NETWORK='s2-eth1') )

    info( '*** Creating links\n' )
    l1 = net.addLink( h1, s1 )
    l2 = net.addLink( s1, s2 )
    l3 = net.addLink( h2, s2 )
    l2.intf1.ifconfig("mtu", "50000")
    l2.intf2.ifconfig("mtu", "50000")

    info( '*** Starting network\n')
    net.start()

    info( '*** Running CLI\n' )
    CLI( net )

    info( '*** Stopping network' )
    #ClickKernelSwitch.batchShutdown([s1])
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()

