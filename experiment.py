#!/usr/bin/python

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd, ITSLink
from mn_wifi.wmediumdConnector import interference


def topology():

	#Create a network
	net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

	info("*** Creating nodes\n")
	kwargs = {'ssid': 'vanet-ssid', 'mode': 'g', 'passwd': '123456789a',
              'encrypt': 'wpa2', 'failMode': 'standalone', 'datapath': 'user'}
    	ap1 = net.addAccessPoint('ap1', mac='00:00:00:11:00:01', channel='1',
                            position='2600,3500,0', **kwargs)
	sta1 = net.addStation('sta1', mac='00:00:00:00:00:01', position='200,400,0')
	sta2 = net.addStation('sta2', mac='00:00:00:00:00:02', position='400,400,0')
	car1 = net.addCar('car1', wlans=2, mac='00:00:00:00:00:03', encrypt=['wpa2', ''], position='150,200,0')
	car1 = net.addCar('car2', wlans=2, mac='00:00:00:00:00:04', encrypt=['wpa2', ''], position='250,200,0')
	car1 = net.addCar('car3', wlans=2, mac='00:00:00:00:00:05', encrypt=['wpa2', ''], position='350,200,0')
	car1 = net.addCar('car4', wlans=2, mac='00:00:00:00:00:06', encrypt=['wpa2', ''], position='450,200,0')
#	c1 = net.addController('c1')

	#bs1 = net.addBaseStation('BS1', ssid='new-ssid1', mode='g', channel='1')
	#bs2 = net.addBaseStation('BS2', ssid='new-ssid2', mode='g', channel='6')
	#bs3 = net.addBaseStation('BS3', ssid='new-ssid3', mode='g', channel='11')

	info("*** Configuring Propagation Model\n")
	net.setPropagationModel(model="logDistance", exp=3.5)

    	info("*** Configuring nodes\n")
    	net.configureNodes()
    	for car in net.cars:
        	net.addLink(car, intf=car.wintfs[1].name,
                    	cls=ITSLink, band=20, channel=181)


	info("*** Starting ITS Links\n")
    	net.addLink(sta1, intf='sta1-wlan0', cls=ITSLink,
        	        band=20, channel=181, proto='batman_adv')
    	net.addLink(sta2, intf='sta2-wlan0', cls=ITSLink,
        	        band=20, channel=181, proto='batman_adv')

	#for x in range(0,20):
	#	net.addMesh(car[x], ssid='mesh')

#	net.addLink(bs1, bs2)
#	net.addLink(bs1, bs3)

	net.plotGraph(max_x=600, max_y=600)

	info("*** Starting network\n")
	net.build()
#	c1.start()
	ap1.start([])

	for id, car in enumerate(net.cars):
        	car.setIP('192.168.0.{}/24'.format(id+1),
                	  intf='{}'.format(car.wintfs[0].name))
        	car.setIP('192.168.1.{}/24'.format(id+1),
                	  intf='{}'.format(car.wintfs[1].name))
#	sta1.start([c1])
#	sta2.start([c1])
#	sta3.start([c1])

	info("*** Running CLI\n")
	CLI(net)

	info("*** Stopping network\n")
	net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
