#!/usr/bin/python3
# (c) Mihai Chiroiu - CDCI (https://ocw.cs.pub.ro/courses/cdci) 

from mininet.net import Mininet, Containernet
from mininet.node import OVSBridge, Node, Controller, Docker
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import debug, info, setLogLevel
from mininet.topo import Topo
from mininet.util import ipAdd, netParse, ipStr, info, waitListening

SWITCHES = ["sw0", "sw1", "sw2", "sw3", "sw4"]
HOSTS = {
    "srv1": {"multi": True, "type": None, "ip": "10.88.205.3/24", "link":
             "sw1", "dimage": "rpi-mn/base"},
    "srv2": {"multi": True, "type": None, "ip": "10.7.6.3/24", "link":
                 "sw2", "dimage": "rpi-mn/base"},
    "srv3": {"multi": True, "type": None, "ip": "10.5.140.3/24", "link":
                 "sw3", "dimage": "rpi-mn/base"},
    "srv4": {"multi": True, "type": None, "ip": "10.155.20.3/24", "link":
                 "sw4", "dimage": "rpi-mn/base"},
    "d1": {"type": Docker, "ip": "10.88.205.2/24", "link": "sw1",
        "dimage": "lab03/dnsserver", "dcmd": "./start_app.sh "},
    "d2": {"type": Docker, "ip": "10.7.6.2/24", "link": "sw2",
        "dimage": "lab03/iot", "dcmd":"./start_app.sh "},
    "d3": {"type": Docker, "ip": "10.155.20.2/24", "link": "sw4",
        "dimage": "dvwa", "dcmd": "./start_app.sh"},
    "attacker": {"type": Docker, "ip": "172.16.0.1/24", "link": "sw0",
                  "dimage": "kali"},
    "dhcpserver": {"type": Docker, "ip": "10.255.255.249/24", "link": "sw0",
                  "dimage": "lab03/dhcpserver", "dcmd": "./start_app.sh"},
    }
ROUTERS = {
    "r1": {"links": [("sw0", "eth1", "10.255.255.1/24"),
                         ("sw1", "eth2", "10.88.205.1/24")]},
    "r2": {"links": [("sw0", "eth1", "10.255.255.2/24"),
                         ("sw2", "eth2", "10.7.6.1/24")]},
    "r3": {"links": [("sw3", "eth2", "10.5.140.1/24")]},
    "r4": {"links": [("sw0", "eth1", "10.255.255.4/24"),
                         ("sw4", "eth3", "10.155.20.1/24")]},
    }
DIRECT_LINKS = [
    (("r3", "r3-eth1", "10.20.25.1/24"),
     ("r4", "r4-eth2", "10.20.25.2/24")),
]
ROUTES = {
    "r1": [("10.7.6.0/24", "10.255.255.2"),     # sw2 via r2
           ("10.5.140.0/24", "10.255.255.4"),   # sw3 via r4
           ("10.155.20.0/24", "10.255.255.4"),  # sw4 via r4
           ("10.20.25.0/24", "10.255.255.4"),   # r3-r4
           ("default", "10.255.255.249")],      # nat
    "r2": [("10.88.205.0/24", "10.255.255.1"),  # sw1 via r1
           ("10.5.140.0/24", "10.255.255.4"),   # sw3 via r4
           ("10.155.20.0/24", "10.255.255.4"),  # sw4 via r4
           ("10.20.25.0/24", "10.255.255.4"),   # r3-r4
           ("default", "10.255.255.249")],

    "r3": [("default", "10.20.25.2")],  # use default gw here

    "r4": [("10.88.205.0/24", "10.255.255.1"),  # sw1 via r1
           ("10.7.6.0/24", "10.255.255.2"),     # sw2 via r2
           ("10.5.140.0/24", "10.20.25.1"),     # sw3 via r3
           ("default", "10.255.255.249")],      # nat
    "d1": [("default", "10.88.205.1")],  # use default gw here
    "d2": [("default", "10.7.6.1")],  # use default gw here
    "d3": [("default", "10.155.20.1")],  # use default gw here
    "dhcpserver": [("10.7.6.0/24", "10.255.255.2"),
        ("10.88.205.0/24", "10.255.255.1"),
        ("10.155.20.0/24", "10.255.255.4"),
        ("10.5.140.0/24", "10.255.255.4")],  # use default gw here
    }
NETWORKS = {
    "lab03": ["dhcpserver","d1", "d2", "d3", "attacker", "srv1", "srv2","srv3", "srv4"],
}

class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        super(LinuxRouter, self).terminate()

class CDCITopology():
    def configure_routes(self, net):
        """ Configures routes on all routers. """
        for rname, routes in ROUTES.items():
            rx = net[rname]
            for (route, via) in routes:
                info ("%s route for %s via %s\n" % (rname, route, via))
                rx.cmd('ip route del %s; '
                       'ip route add %s via %s' %
                       (route, route, via))
                rx.cmd('sysctl net.ipv4.ip_forward=1')

    def configure_network(self, net, net_name, multi_count):
        """ Starts the specified network (and all devices inside). """
        net.addController('c0')
        # Initialize the base devices: switches and routers
        for switch_name in SWITCHES:
            net.addSwitch(switch_name, cls=OVSBridge)

        for router_name, options in ROUTERS.items():
            net.addHost(router_name, cls=LinuxRouter, ip=options["links"][0][2])
            # add the links between routers and switches
            for other_name, intf_name, intf_ip in options["links"]:
                intf_name = router_name + "-" + intf_name
                net.addLink(other_name, router_name, intfName2=intf_name,
                             params2={'ip': intf_ip})
        for link_dev1, link_dev2 in DIRECT_LINKS:
            net.addLink(link_dev1[0], link_dev2[0],
                         intfName1=link_dev1[1], intfName2=link_dev2[1],
                         params1={'ip': link_dev1[2]},
                         params2={'ip': link_dev2[2]})

        hosts = NETWORKS[net_name]
        for host_name in hosts:
            host = HOSTS[host_name]
            if host.get("multi", False):
                for i in range(multi_count):
                    print("Starting instance %s-%i..." % (host_name, i+1))
                    self._add_host(net, net_name, host_name, host, idx=i)
            else:
                # only 1 instance is required
                print("Starting instance %s..." % host_name)
                self._add_host(net, net_name, host_name, host)
        return True

    def stop_network(self, net, name):
        """ Stops the specified network (and all its devices). """

        print("Stopping network %s..." % name)
        hosts = self.NETWORKS[name]
        for host_name in hosts:
            # for multi hosts, the names contain the index of the instance
            net[host_name].stop(deleteIntfs=True)
        
        return False

    def _add_host(self, net, net_name, host_name, options, idx=0):
        """ Starts the specified host at runtime (after the base topology has
            been initialized). """

        host_ip = options.get("ip")
        is_multi = options.get("multi", False)
        host_name_i = host_name
        if is_multi:
            host_name_i = host_name + "-" + str(idx + 1)
            host_base, host_prefix = netParse(host_ip)
            host_ip = ipAdd((host_base & 0xFF) + idx, ipBaseNum=host_base,
                            prefixLen=host_prefix)
            host_ip += "/%i" % host_prefix

        if options.get("type") is Docker:
            # code to use ContainerNet (comment Docker code instead)
            mn_args = {
                "network_mode": "none",
                "dimage": options.get("dimage", "ubuntu"),
                "dcmd": options.get("dcmd", None),
                "ip": host_ip,
            }
            net.addDocker(host_name_i, **mn_args)
        else:
            # code to use ContainerNet (comment Docker code instead)
            mn_args = {
                "ip": host_ip,
            }
            net.addHost(host_name_i, **mn_args)
            
        # link the container to its switch
        net.addLink(host_name_i, options["link"], params1={'ip': host_ip})
        # restart the switch to configure the new link
        debug ("%s" % (options["link"]))

    def start_sshd(self,net, net_name, multi_count=1):
        # do not detach, but run in background (so it will get killed when
        # container stops)
        hosts = NETWORKS[net_name]
        for host_name in hosts:
            options = HOSTS[host_name]
            if options.get("type") is None:
                if options.get("multi", False):
                    for i in range(multi_count):
                        host_name_i = host_name + "-" + str(i + 1)
                        host = net[host_name_i]
                        host.cmd("/usr/sbin/sshd -D -o UseDNS=no -u0 &")
                        debug("Starting SSHD on host")
                        waitListening(client=host, server=host, port=22, timeout=5)
                else:
                    host = net[host_name]
                    host.cmd("/usr/sbin/sshd -D -o UseDNS=no -u0 &")
                    debug("Starting SSHD on host")
                    waitListening(client=host, server=host, port=22, timeout=5)

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    topo = CDCITopology()
    net = Containernet(controller=Controller)
    topo.configure_network(net, "lab03",1)
    net.start()
    topo.start_sshd(net, "lab03",1)
    topo.configure_routes(net)
    print("Host connections:")
    #dumpNodeConnections(net.hosts)
    CLI(net)
    net.stop()

