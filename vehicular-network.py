from mininet.net import Mininet
from mininet.node import Controller
from mininet.wifi.node import AccessPoint, Station
from mininet.cli import CLI
from mininet.log import setLogLevel
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, ITSLink

def vehicularNetwork():
    net = Mininet(controller=Controller)

    print("*** Creating nodes")
    # Adding vehicles
    v1 = net.addCar('v1', wlans=1)
    v2 = net.addCar('v2', wlans=1)
    v3 = net.addCar('v3', wlans=1)
    v4 = net.addCar('v4', wlans=1)

    # Adding stations
    sta1 = net.addStation('sta1', position='10,20,0')
    sta2 = net.addStation('sta2', position='30,40,0')

    # Adding access points
    ap1 = net.addAccessPoint('ap1', ssid='V2I', mode='g', channel='1', position='20,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='meshNetwork', mode='g', channel='6', position='40,50,0')

    print("*** Creating links")
    # Creating links between vehicles and access points
    net.addLink(v1, ap1)
    net.addLink(v2, ap1)
    net.addLink(v3, ap1)
    net.addLink(v4, ap1)

    # Creating links between stations and access points
    net.addLink(sta1, ap2)
    net.addLink(sta2, ap2)

    # Enabling V2I communication using 802.11p protocol
    ap1.setMeshIface('ap1-wlan1', ssid='V2I', mode='80211p')

    print("*** Starting network")
    net.build()
    net.start()

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == "__main__":
    setLogLevel('info')
    vehicularNetwork()
