from programA import convert, pack16, unpack16
from programA import ascii_dump, array_address, show_stack
from programA import memory_write, memory_read


def test_pack_unpack_zero():

    low, high = pack16(0)

    assert low == 0
    assert high == 0

    value = unpack16(low, high)
    assert value == 0


def test_pack_unpack_one():

    low, high = pack16(1)

    assert low == 1
    assert high == 0

    assert unpack16(low, high) == 1


def test_pack_unpack_255():

    low, high = pack16(255)

    assert low == 255
    assert high == 0

    number = unpack16(low, high)

    assert number == 255


def test_pack_unpack_256():

    low, high = pack16(256)

    assert low == 0
    assert high == 1

    result = unpack16(low, high)

    assert result == 256


def test_pack_unpack_65535():

    low, high = pack16(65535)

    assert low == 255
    assert high == 255

    final = unpack16(low, high)

    assert final == 65535


def test_ascii_dump_simple():

    rows = ascii_dump("HELLO", start=0x1000)

    # first character should be H
    assert rows[0] == "0x1000 : 0x48"

    # last should be null terminator
    assert rows[-1] == "0x1005 : 0x00"


def test_array_address():

    addr = array_address(1000, 3, 2)

    assert addr == 1006


def test_stack_frame():

    lines = show_stack(10, 20)

    assert "RETURN" in lines[0]
    assert "a = 10" in lines[1]
    assert "b = 20" in lines[2]


def test_binary_length():

    nums = [0, 1, 255, 256, 65535]

    for n in nums:

        _, bits, _ = convert(n)

        assert len(bits) == 16


def test_signed_and_memory():

    _, _, s = convert(65535)
    assert s == -1

    _, _, s2 = convert(32768)
    assert s2 == -32768

    low, high = pack16(1000)

    memory_write(0x2000, low)
    memory_write(0x2001, high)

    read_value = unpack16(
        memory_read(0x2000),
        memory_read(0x2001)
    )

    assert read_value == 1000