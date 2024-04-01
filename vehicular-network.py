from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.cli import CLI
from mininet.log import setLogLevel

def vehicularNetwork():
    net = Mininet(controller=Controller, accessPoint=OVSKernelAP, switch=OVSKernelSwitch)

    print("*** Creating nodes")
    # Adding vehicles
    v1 = net.addCar('v1', wlans=1)
    v2 = net.addCar('v2', wlans=1)
    v3 = net.addCar('v3', wlans=1)
    v4 = net.addCar('v4', wlans=1)

    # Adding stations
    sta1 = net.addStation('sta1', position='10,20,0')
    sta2 = net.addStation('sta2', position='30,40,0')

    print("*** Creating links")
    # Creating links between vehicles and stations
    net.addMesh(v1, intf='v1-wlan0', ssid='meshNetwork')
    net.addMesh(v2, intf='v2-wlan0', ssid='meshNetwork')
    net.addMesh(v3, intf='v3-wlan0', ssid='meshNetwork')
    net.addMesh(v4, intf='v4-wlan0', ssid='meshNetwork')

    # Enabling V2I communication using 802.11p protocol
    net.addL2Mesh('v1', intf='v1-wlan0', ssid='V2I', mode='80211p')
    net.addL2Mesh('v2', intf='v2-wlan0', ssid='V2I', mode='80211p')
    net.addL2Mesh('v3', intf='v3-wlan0', ssid='V2I', mode='80211p')
    net.addL2Mesh('v4', intf='v4-wlan0', ssid='V2I', mode='80211p')

    # Creating link between stations
    net.addLink(sta1, sta2)

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
