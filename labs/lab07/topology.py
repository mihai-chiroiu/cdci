#!/usr/bin/python3
# (c) Mihai Chiroiu - CDCI (https://ocw.cs.pub.ro/courses/cdci) 

from mininet.net import Mininet, Containernet
from mininet.node import Host, OVSBridge, Node, Controller, Docker, UserSwitch, OVSSwitch
from mininet.nodelib import NAT
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Intf
from subprocess import call
import subprocess

def myNetwork():
    net = Containernet(controller=Controller)

    info( '*** Adding controller\n' )
    net.addController(name='c0')

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1')

    info( '*** Add hosts\n')
    # attacker 2 docker containers
    mn_args = {
        "network_mode": "none",
        "dimage": "exam_docker",
        "dcmd": "./start_app.sh",
        "ip": "192.168.16.2/24",
    }
    H1 = net.addDocker('h1', **mn_args)
    mn_args = {
        "network_mode": "none",
        "dimage": "exam_docker",
        "dcmd": "./start_app.sh",
        "ip": "192.168.16.3/24",
    }
    H2 = net.addDocker('h2', **mn_args)
    mn_args = {
        "network_mode": "none",
        "dimage": "lab07/snort",
        "dcmd": None,
        "ip": "192.168.16.100/24",
    }
    H3 = net.addDocker('IDS', **mn_args)

    info( '*** Add links\n')
    net.addLink( H1, s1 )
    net.addLink( H2, s1 )
    net.addLink( H3, s1 )

    info ('*** Add Internet access\n')
    mn_args = {
        "ip": "192.168.16.1/24",
    }
    nat = net.addHost( 'nat0', cls=NAT, inNamespace=False, subnet='192.168.16.0/24', **mn_args )
    # Connect the nat to the switch
    net.addLink( nat, s1 )

    info( '*** Starting network\n')
    net.start()
    H1.cmd('ip r a default via 192.168.16.1')
    H2.cmd('ip r a default via 192.168.16.1')

    # port mirroring all from s1 to IDS
    cmd = '''ovs-vsctl del-port s1-eth3'''
    results = subprocess.run(cmd, shell=True, universal_newlines=True, check=True).stdout
    print (results)

    cmd = '''ovs-vsctl add-port s1 s1-eth3 -- --id=@p get port s1-eth3 -- --id=@m create mirror name=m0 select-all=true output-port=@p -- set bridge s1 mirrors=@m'''
    results = subprocess.run(cmd, shell=True, universal_newlines=True, check=True).stdout

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
