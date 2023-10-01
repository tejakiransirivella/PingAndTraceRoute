class icmp_header:
    __slots__ = ("type", "code", "checksum", "identifier", "seq_no")
    TYPE_BITS = 8
    CODE_BITS = 8
    CHECKSUM_BITS = 16
    IDENTIFIER_BITS = 16
    SEQ_NO_BITS = 16

    def __init__(self):
        self.type = 0
        self.code = 0
        self.checksum = 0
        self.identifier = 0
        self.seq_no = 0

    def set_type(self, type):
        self.type = type

    def set_code(self, code):
        self.code = code

    def set_identifer(self, identifier):
        self.identifier = identifier

    def set_seq_no(self, seq_no):
        self.seq_no = seq_no

    def calculate_checksum(self):
        properties_hex = self.to_hex()
        offset = 0
        checksum = 0
        while offset < len(properties_hex):
            checksum += int(properties_hex[offset:offset + 4], 16)
            offset += 4
        self.checksum = checksum ^ 65535

    def to_hex(self):
        properties = [[self.type, self.TYPE_BITS], [self.code, self.CODE_BITS],
                      [self.checksum, self.CHECKSUM_BITS], [self.identifier, self.IDENTIFIER_BITS],
                      [self.seq_no, self.SEQ_NO_BITS]]
        properties_hex = ""
        for property in properties:
            property_hex = hex(property[0])[2:]
            property_hex = property_hex.zfill(property[1] // 4)
            properties_hex += property_hex
        return properties_hex


def test():
    header = icmp_header()
    header.set_type(8)
    header.set_identifer(1)
    header.set_seq_no(1)
    header.calculate_checksum()
    print(header.checksum)
