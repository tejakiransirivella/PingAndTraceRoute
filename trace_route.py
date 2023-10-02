import socket
import struct
import sys
import time

from icmp_header import icmp_header


class TraceRoute:
    __slots__ = "no_probes", "numeric", "summary", "dest_address", "max_hops"

    def __init__(self):
        self.no_probes = 3
        self.numeric = False
        self.summary = False
        self.dest_address = None
        self.max_hops = 30

    def get_hostname_from_addr(self, addr):
        if self.numeric:
            return addr

        try:
            return socket.gethostbyaddr(addr)[0] + " [" + addr + "]"
        except socket.error:
            return addr

    def handle_input(self):
        arg_length = len(sys.argv)
        for i in range(1, arg_length):
            if sys.argv[i] == '-h':
                i += 1
                print("usage: trace_route.py [-h] [-n] [-q Q] [-S] destination\n")
                print("positional arguments")
                print(" destination target host address\n")

                print("options:")
                print("-h\thelp message")
                print("-n\tnumerical hop address")
                print("-q\tno of probes per ttl")
                print("-S\tsummary of failed probes per hop")
                sys.exit()

            elif i == arg_length - 1:
                self.dest_address = sys.argv[i]
                i += 2
            elif sys.argv[i] == '-n':
                self.numeric = True
                i += 1
            elif sys.argv[i] == '-q':
                self.no_probes = int(sys.argv[i+1])
                i += 2
            elif sys.argv[i] == '-S':
                self.summary = True
                i += 1

    def find_trace(self):
        try:

            # create icmp header object
            icmpheader = icmp_header()
            icmpheader.set_type(8)
            icmpheader.set_identifer(1)
            icmpheader.set_seq_no(1)
            icmpheader.calculate_checksum()

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            raw_socket.settimeout(4)
            print("Tracing route to "+self.get_hostname_from_addr(self.dest_address))
            print("over a maximum of " + str(self.max_hops) + " hops:\n")

            ttl_value = 1
            ip_addr = ""
            summary = []
            while not (ttl_value > self.max_hops or ip_addr == self.dest_address):
                output = [str(ttl_value).ljust(3)]
                failed_probs = 0
                for i in range(self.no_probes):
                    ttl_bytes = struct.pack('!B', ttl_value)
                    raw_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl_bytes)

                    send_time = time.time()
                    try:
                        raw_socket.sendto(bytes.fromhex(icmpheader.to_hex()), (self.dest_address, 0))
                        data, addr = raw_socket.recvfrom(1024)
                        ip_addr = addr[0]
                        recv_time = time.time()
                        elapse_time = str(int((recv_time - send_time) * 1000)) + " ms"
                        output.append(elapse_time.ljust(5))
                    except socket.timeout:
                        output.append("*".ljust(5))
                        failed_probs += 1
                        ip_addr = "Request timed out."

                    if i == self.no_probes - 1:
                        hostname_addr = self.get_hostname_from_addr(ip_addr)
                        output.append(hostname_addr)
                summary.append([ttl_value, failed_probs])

                for item in output:
                    print(item, end="      ")
                print("")
                ttl_value += 1

            if self.summary:
                print("\nhop no" + "     failed probes")
                for record in summary:
                    print(str(record[0]).ljust(12), record[1])

            raw_socket.close()
        except socket.error as err:
            print(err)


def main():
    trace_route = TraceRoute()
    trace_route.handle_input()
    trace_route.find_trace()


if __name__ == "__main__":
    main()
