from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node, OVSBridge
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink

class LinuxRouter(Node):
    """Host w Mininecie udający router (włącza IP forwarding)"""
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class OstatecznaTopo(Topo):
    def build(self, **_opts):

        r9 = self.addNode('r9', cls=LinuxRouter, ip='10.0.100.1/24')
        r7 = self.addNode('r7', cls=LinuxRouter, ip='10.0.100.2/24')
        self.addLink(r9, r7, intfName1='r9-eth1', intfName2='r7-eth1')



        switch1 = self.addSwitch('s1')
        self.addLink(switch1, r9, intfName2='r9-eth2', params2={'ip': '10.0.1.254/24'})
        
        attacker = self.addHost('attacker', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
        legit_pc2 = self.addHost('legit_pc2', ip='10.0.1.2/24', defaultRoute='via 10.0.1.254')
        self.addLink(attacker, switch1)
        self.addLink(legit_pc2, switch1)




        s_srv0 = self.addSwitch('s_srv0')
        self.addLink(s_srv0, r9, intfName2='r9-eth3', params2={'ip': '10.0.2.254/24'})
        server0 = self.addHost('server0', ip='10.0.2.1/24', defaultRoute='via 10.0.2.254')
        self.addLink(server0, s_srv0)



        switch2 = self.addSwitch('s2')
        self.addLink(switch2, r7, intfName2='r7-eth2', params2={'ip': '10.0.3.254/24'})
        legit_pc3 = self.addHost('legit_pc3', ip='10.0.3.1/24', defaultRoute='via 10.0.3.254')
        self.addLink(legit_pc3, switch2)



        s_srv1 = self.addSwitch('s_srv1')
        self.addLink(s_srv1, r7, intfName2='r7-eth3', params2={'ip': '10.0.4.254/24'})
        server1 = self.addHost('server1', ip='10.0.4.1/24', defaultRoute='via 10.0.4.254')
        self.addLink(server1, s_srv1)



        switch0 = self.addSwitch('s0')
        
        self.addLink(switch0, r7, intfName2='r7-eth4', params2={'ip': '10.0.5.254/24'}, bw=10)
        
        victim_pc0 = self.addHost('victim_pc0', ip='10.0.5.1/24', defaultRoute='via 10.0.5.254')
        legit_pc4 = self.addHost('legit_pc4', ip='10.0.5.2/24', defaultRoute='via 10.0.5.254')
        server2 = self.addHost('server2', ip='10.0.5.3/24', defaultRoute='via 10.0.5.254')
        
        self.addLink(victim_pc0, switch0)
        self.addLink(legit_pc4, switch0)
        self.addLink(server2, switch0)


def run():
    topo = OstatecznaTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None, switch=OVSBridge)
    net.start()


    info('\n*** Konfiguracja routingu statycznego...\n')
    r9 = net.get('r9')
    r7 = net.get('r7')
    
    r9.cmd('ip route add 10.0.3.0/24 via 10.0.100.2')
    r9.cmd('ip route add 10.0.4.0/24 via 10.0.100.2')
    r9.cmd('ip route add 10.0.5.0/24 via 10.0.100.2')    

    r7.cmd('ip route add 10.0.1.0/24 via 10.0.100.1')
    r7.cmd('ip route add 10.0.2.0/24 via 10.0.100.1')

    info('*** Test Atakujący -> Ofiara\n')
    net.ping([net.get('attacker'), net.get('victim_pc0')])

    info('\n*** Gotowe!\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
