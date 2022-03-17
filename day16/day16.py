from ast import parse


def parse_input(input_file: str) -> str:
    """Parse puzzle input.

    Args:
        input_file (str): Puzzle input txt file.

    Returns:
        str: hexadecimal representation.
    """
    o = open(input_file)
    return o.read()


def hex_to_bin(hex_rep: str) -> str:
    """Convert hexadecimal to binary.

    Args:
        hex_rep (str): Hexadecimal representation.

    Returns:
        str: Binary representation.
    """
    return bin(int(hex_rep, 16))[2:].zfill(len(hex_rep) * 4)


class Bits:
    """Buoyancy Interchange Transmission System.

    Args:
        hex_rep (str): Hexadecimal representation.
    """

    def __init__(self, hex_rep: str) -> None:
        self.bin_rep = hex_to_bin(hex_rep)
        self.pc = 0
        self.version_sum = 0
        self.numbers = []

    def get(self, n: int) -> str:
        """Get the next n chunk and move the program counter by n.

        Args:
            n (int): Size of chunk to get.

        Returns:
            str: Chunk.
        """
        chunk = self.bin_rep[self.pc : self.pc + n]
        self.pc += n
        return chunk


def decode(bits: str):
    """Decode bits.

    Args:
        bits (str): Bits to decode.
    """

    def product(numbers):
        result = 1
        for i in numbers:
            result *= i
        return result

    def greater_than(numbers):
        if numbers[0] > numbers[1]:
            return 1
        else:
            return 0

    def less_than(numbers):
        if numbers[0] < numbers[1]:
            return 1
        else:
            return 0

    def equal_to(numbers):
        if numbers[0] == numbers[1]:
            return 1
        else:
            return 0

    operations = {
        0: sum,
        1: product,
        2: min,
        3: max,
        5: greater_than,
        6: less_than,
        7: equal_to,
    }
    version = int(bits.get(3), 2)
    bits.version_sum += version
    type_id = int(bits.get(3), 2)

    if type_id == 4:
        number = ""
        while True:
            cont = int(bits.get(1))
            group = bits.get(4)
            number += group
            if not cont:
                return int(number, 2)

    else:
        results = []
        length_id = bits.get(1)
        if length_id == "0":
            subpack_len = int(bits.get(15), 2)
            subpack_end = bits.pc + subpack_len
            while bits.pc < subpack_end:
                results.append(decode(bits))

        if length_id == "1":
            subpack_num = int(bits.get(11), 2)
            for _ in range(subpack_num):
                results.append(decode(bits))
        return operations[type_id](results)


# Tests


def test_parse_input():
    output = parse_input("day16/input.txt")
    assert type(output) is str


def test_hex_to_bin():
    assert hex_to_bin("D2FE28") == "110100101111111000101000"
    assert (
        hex_to_bin("38006F45291200")
        == "00111000000000000110111101000101001010010001001000000000"
    )
    assert (
        hex_to_bin("EE00D40C823060")
        == "11101110000000001101010000001100100000100011000001100000"
    )


def test_decode_literal():
    packet = Bits("D2FE28")
    assert decode(packet) == 2021


def test_decode_operator_length():
    packet = Bits("38006F45291200")
    assert decode(packet) == 1


def test_decode_operators_number():
    packet = Bits("EE00D40C823060")
    assert decode(packet) == 3


def test_part_1():
    packet_1 = Bits("8A004A801A8002F478")
    packet_2 = Bits("620080001611562C8802118E34")
    packet_3 = Bits("C0015000016115A2E0802F182340")
    packet_4 = Bits("A0016C880162017C3686B18A3D4780")
    decode(packet_1)
    decode(packet_2)
    decode(packet_3)
    decode(packet_4)
    assert packet_1.version_sum == 16
    assert packet_2.version_sum == 12
    assert packet_3.version_sum == 23
    assert packet_4.version_sum == 31


def test_part_2():
    packet_1 = Bits("C200B40A82")
    packet_2 = Bits("04005AC33890")
    packet_3 = Bits("880086C3E88112")
    packet_4 = Bits("CE00C43D881120")
    packet_5 = Bits("D8005AC2A8F0")
    packet_6 = Bits("F600BC2D8F")
    packet_7 = Bits("9C005AC2F8F0")
    packet_8 = Bits("9C0141080250320F1802104A08")
    assert decode(packet_1) == 3
    assert decode(packet_2) == 54
    assert decode(packet_3) == 7
    assert decode(packet_4) == 9
    assert decode(packet_5) == 1
    assert decode(packet_6) == 0
    assert decode(packet_7) == 0
    assert decode(packet_8) == 1


if __name__ == "__main__":
    output = parse_input("day16/input.txt")
    transmission = Bits(output)
    answer_2 = decode(transmission)
    answer_1 = transmission.version_sum

    print("Day 16 Solutions:")
    print(f"Part 1: {answer_1}")
    print(f"Part 2: {answer_2}")
