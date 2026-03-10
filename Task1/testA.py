import unittest
from programA import (
    convert,
    pack16,
    unpack16,
    ascii_dump,
    array_address,
    show_stack,
    memory_write,
    memory_read,
)


class ProgramTests(unittest.TestCase):

    def test_1_pack_unpack_boundary_0(self):
        bot, top = pack16(0)
        self.assertEqual(bot, 0)
        self.assertEqual(top, 0)
        self.assertEqual(unpack16(bot, top), 0)

    def test_2_pack_unpack_boundary_1(self):
        bot, top = pack16(1)
        self.assertEqual(bot, 1)
        self.assertEqual(top, 0)
        self.assertEqual(unpack16(bot, top), 1)

    def test_3_pack_unpack_boundary_255(self):
        bot, top = pack16(255)
        self.assertEqual(bot, 255)
        self.assertEqual(top, 0)
        self.assertEqual(unpack16(bot, top), 255)

    def test_4_pack_unpack_boundary_256(self):
        bot, top = pack16(256)
        self.assertEqual(bot, 0)
        self.assertEqual(top, 1)
        self.assertEqual(unpack16(bot, top), 256)

    def test_5_pack_unpack_boundary_65535(self):
        bot, top = pack16(65535)
        self.assertEqual(bot, 255)
        self.assertEqual(top, 255)
        self.assertEqual(unpack16(bot, top), 65535)

    def test_6_ascii_dump_hello(self):
        rows = ascii_dump("HELLO", start=0x1000)
        self.assertEqual(rows[0], "0x1000 : 0x48")
        self.assertEqual(rows[-1], "0x1005 : 0x00")

    def test_7_array_address_base_1000_index_3_size_2(self):
        self.assertEqual(array_address(1000, 3, 2), 1006)

    def test_8_stack_frame_offsets_and_values(self):
        rows = show_stack(10, 20)
        self.assertIn("RETURN", rows[0])
        self.assertIn("a = 10", rows[1])
        self.assertIn("b = 20", rows[2])

    def test_9_bin16_always_16_characters(self):
        for num in [0, 1, 255, 256, 65535]:
            _, bits, _ = convert(num)
            self.assertEqual(len(bits), 16)

    def test_10_signed16_and_memory_write_read(self):
        _, _, signed = convert(65535)
        self.assertEqual(signed, -1)
        _, _, signed = convert(32768)
        self.assertEqual(signed, -32768)
        bot, top = pack16(1000)
        memory_write(0x2000, bot)
        memory_write(0x2001, top)
        self.assertEqual(unpack16(memory_read(0x2000), memory_read(0x2001)), 1000)


if __name__ == "__main__":
    unittest.main(verbosity=2)