import socket

from icmp_header import icmp_header


class ping:

    DEST_ADDRESS = '8.8.8.8'

    def send_ping(self):
        try:
            icmpheader = icmp_header()
            icmpheader.set_type(8)
            icmpheader.set_identifer(1)
            icmpheader.set_seq_no(1)
            icmpheader.calculate_checksum()

            raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            raw_socket.sendto(bytes.fromhex(icmpheader.to_hex()), (self.DEST_ADDRESS, 0))
            data, addr = raw_socket.recvfrom(1024)
            print(f"Received response from {data.hex(' ')}{addr}")
            raw_socket.close()
        except socket.error as err:
            print(err)


def test():
    ping1 = ping()
    ping1.send_ping()


test()
