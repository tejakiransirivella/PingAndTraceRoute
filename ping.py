import socket
import sys
import time

from icmp_header import icmp_header


class Ping:
    __slots__ = ("count", "wait", "packet_size", "timeout", "dest_address")
    TTL_LOC = 8

    def __init__(self):
        self.count = sys.maxsize
        self.wait = 1
        self.packet_size = 56
        self.timeout = sys.maxsize
        self.dest_address = None

    def handle_input(self):
        arg_length = len(sys.argv)
        for i in range(1, arg_length):
            if sys.argv[i] == '-h':
                i += 1
            elif i == arg_length - 1:
                self.dest_address = sys.argv[i]
                i += 2
            elif sys.argv[i] == '-c':
                self.count = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == '-i':
                self.wait = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == '-s':
                self.packet_size = int(sys.argv[i + 1])
                i += 2
            elif sys.argv[i] == '-t':
                self.timeout = int(sys.argv[i + 1])
                i += 2

    def send_ping(self):
        try:
            icmpheader = icmp_header()
            icmpheader.set_type(8)
            icmpheader.set_identifer(1)
            icmpheader.set_seq_no(1)
            icmpheader.calculate_checksum()

            payload = icmpheader.to_hex()
            for i in range(self.packet_size):
                payload += "00"
            payload = bytes.fromhex(payload)

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

            print("Pinging", self.dest_address, "with", self.packet_size, "bytes of data:")

            start_time_for_timeout = time.time()
            for i in range(self.count):
                start_time = time.time()
                raw_socket.sendto(payload, (self.dest_address, 0))
                data, addr = raw_socket.recvfrom(1024)
                end_time = time.time()

                elapse_time = str(int((end_time - start_time) * 1000)) + "ms"
                data = data.hex()
                ttl = int(data[self.TTL_LOC * 2:self.TTL_LOC * 2 + 2], 16)

                print("Reply from " + self.dest_address + ": bytes=" + str(self.packet_size) +
                      " time=" + elapse_time + " TTL=" + str(ttl))
                if int(end_time - start_time_for_timeout) > self.timeout:
                    break
                time.sleep(self.wait)
            raw_socket.close()
        except socket.error as err:
            print(err)


def main():
    ping = Ping()
    ping.handle_input()
    ping.send_ping()


if __name__ == "__main__":
    main()
