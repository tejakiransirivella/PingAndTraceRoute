import socket
import struct
import time

from icmp_header import icmp_header
from ip_header import ip_header


class TraceRoute:
    DEST_ADDRESS = '8.8.8.8'

    __slots__ = "no_probes"

    def __init__(self):
        self.no_probes = 3

    def get_hostname_from_addr(self, addr):
        try:
            return socket.gethostbyaddr(addr)[0] + " ["+addr+"]"
        except socket.error as err:
            return addr

    def find_trace(self):
        try:

            # create icmp header object
            icmpheader = icmp_header()
            icmpheader.set_type(8)
            icmpheader.set_identifer(1)
            icmpheader.set_seq_no(1)
            icmpheader.calculate_checksum()

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

            ttl_value = 1
            ip_addr = ""
            while ip_addr != self.DEST_ADDRESS:
                output = [ttl_value]
                for i in range(self.no_probes):
                    ttl_bytes = struct.pack('!B', ttl_value)
                    raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_bytes)
                    send_time = time.time()
                    raw_socket.sendto(bytes.fromhex(icmpheader.to_hex()), (self.DEST_ADDRESS, 0))
                    data, addr = raw_socket.recvfrom(1024)
                    recv_time = time.time()
                    elapse_time = str(int((recv_time-send_time)*1000)) + " ms"
                    output.append(elapse_time)
                    if i == self.no_probes-1:
                        ip_addr = addr[0]
                        hostname_addr = self.get_hostname_from_addr(ip_addr)
                        output.append(hostname_addr)
                for item in output:
                    print(item, end="      ")
                print("")
                ttl_value += 1
            raw_socket.close()
        except socket.error as err:
            print(err)


def test():
    trace_route = TraceRoute()
    trace_route.find_trace()


test()
