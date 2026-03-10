memory = {}
# this is the toy memory that was required

def memory_write(addr, byte):
    memory[addr] = byte & 0xFF


def memory_read(addr):
    return memory.get(addr, 0)


def convert(n):
    hex_str = f"0x{n:04X}"
    bin_str = format(n, '016b')
    signed = n if n < 32768 else n - 65536
    return hex_str, bin_str, signed


def pack_u16_le(n):
    low = n & 0xFF
    high = (n >> 8) & 0xFF
    return low, high


def unpack_u16_le(low, high):
    return low + (high << 8)


def ascii_dump_lines(s, base=0x1000):
    lines = []
    for i, ch in enumerate(s):
        addr = base + i
        lines.append(f"0x{addr:04X} : 0x{ord(ch):02X}")
    null_addr = base + len(s)
    lines.append(f"0x{null_addr:04X} : 0x00")
    return lines


def element_address(base, index, size):
    return base + index * size


def stack_frame_lines(a, b):
    lines = []
    lines.append("bp     : RETURN")
    lines.append(f"bp+2   : a = {a}")
    lines.append(f"bp+4   : b = {b}")
    return lines


def main():
    while True:
        print("\n1) Convert (decimal -> hex and 16-bit binary)")
        print("2) Little-endian pack/unpack (16-bit)")
        print("3) ASCII memory dump")
        print("4) Array addressing")
        print("5) Stack frame (bp offsets)")
        print("0) Exit")

        match input("Choose an option: ").strip():

            case "1":
                n = int(input("Enter a decimal number (0 to 65535): "))
                hex_str, bin_str, signed = convert(n)
                print(f"HEX = {hex_str}")
                print(f"BIN(16) = {bin_str}")
                print(f"SIGNED16 = {signed}")

            case "2":
                n = int(input("Enter a number (0 to 65535): "))
                addr_input = input("Enter memory address (e.g. 0x2000 or 8192): ").strip()
                addr = int(addr_input, 16) if addr_input.lower().startswith("0x") else int(addr_input)
                low, high = pack_u16_le(n)
                print(f"LOW BYTE = {low}")
                print(f"HIGH BYTE = {high}")
                print(f"UNPACKED = {unpack_u16_le(low, high)}")
                memory_write(addr, low)
                memory_write(addr + 1, high)
                print(f"MEM[0x{addr:04X}] = 0x{low:02X}")
                print(f"MEM[0x{addr + 1:04X}] = 0x{high:02X}")
                print(f"READ MEM[0x{addr:04X}] = 0x{memory_read(addr):02X}")
                print(f"READ MEM[0x{addr + 1:04X}] = 0x{memory_read(addr + 1):02X}")

            case "3":
                s = input("enter a string (max 10 characters): ")[:10]
                for line in ascii_dump_lines(s):
                    print(line)
                print(f"LENGTH (until 0x00) = {len(s)}")

            case "4":
                base = int(input("enter base address (decimal): "))
                index = int(input("enter index: "))
                size = int(input("enter element size (1 or 2): "))
                mode = input("enter mode (read or write): ").strip().lower()
                addr = element_address(base, index, size)
                print(f"ADDRESS = {base} + {index}*{size} = 0x{addr:04X}")
                match mode:
                    case "write":
                        value = int(input("enter value to write: "))
                        match size:
                            case 1:
                                memory_write(addr, value)
                                print(f"WRITE size=1 value={value} to ADDRESS 0x{addr:04X}")
                            case 2:
                                low, high = pack_u16_le(value)
                                memory_write(addr, low)
                                memory_write(addr + 1, high)
                                print(f"WRITE size=2 value={value} to ADDRESS 0x{addr:04X}")
                    case "read":
                        match size:
                            case 1:
                                print(f"READ size=1 from ADDRESS 0x{addr:04X} = {memory_read(addr)}")
                            case 2:
                                val = unpack_u16_le(memory_read(addr), memory_read(addr + 1))
                                print(f"READ size=2 from ADDRESS 0x{addr:04X} = {val}")

            case "5":
                a = int(input("enter first value (a): "))
                b = int(input("enter second value (b): "))
                for line in stack_frame_lines(a, b):
                    print(line)
                print(f"AX = {a}")
                print(f"BX = {b}")
                print(f"AX (AX+BX) = {a + b}")

            case "0":
                print("goodbye and see you later!")
                break

            case _:
                print("invalid option, please try again.")


if __name__ == "__main__":
    main()