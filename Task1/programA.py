toy_memory = {}


def memory_write(address, value):
    toy_memory[address] = value & 0xFF


def memory_read(address):
    return toy_memory.get(address, 0)


def convert(n):
    as_hex = f"0x{n:04X}"
    as_bin = format(n, "016b")
    as_signed = n - 65536 if n >= 32768 else n
    return as_hex, as_bin, as_signed


def pack16(num):
    bottom = num & 0xFF
    top = (num >> 8) & 0xFF
    return bottom, top


def unpack16(bottom, top):
    return bottom | (top << 8)


def ascii_dump(text, start=0x1000):
    result = []
    for offset, ch in enumerate(text):
        result.append(f"0x{start + offset:04X} : 0x{ord(ch):02X}") 
        
    result.append(f"0x{start + len(text):04X} : 0x00")
    return result


def array_address(base, index, size):
    return base + (index * size)


def show_stack(a, b):
    return [
        "bp     : RETURN",
        f"bp+2   : a = {a}",
        f"bp+4   : b = {b}",
    ]


DIVIDER = "-" * 35


def main():
    running = True

    while running:
        print(f"\n{DIVIDER}")
        print(" CMP5361 - Memory & Number Tool")
        print(DIVIDER)
        print(" [1]  Number converter")
        print(" [2]  Little-endian packer")
        print(" [3]  ASCII memory viewer")
        print(" [4]  Array element lookup")
        print(" [5]  Stack frame viewer")
        print(" [0]  Quit")
        print(DIVIDER)

        pick = input(">> ").strip()

        if pick == "1":
            num = int(input("Enter decimal (0 to 65535): "))
            h, b, s = convert(num)
            print(f"HEX = {h}")
            print(f"BIN(16) = {b}")
            print(f"SIGNED16 = {s}")

        elif pick == "2":
            num = int(input("Enter a 16-bit number: "))
            raw = input("Target address (hex like 0x2000 or decimal): ").strip()
            addr = int(raw, 16) if raw.startswith("0x") or raw.startswith("0X") else int(raw)

            bot, top = pack16(num)
            print(f"LOW BYTE = {bot}")
            print(f"HIGH BYTE = {top}")
            print(f"UNPACKED = {unpack16(bot, top)}")

            memory_write(addr, bot)
            memory_write(addr + 1, top)

            print(f"MEM[0x{addr:04X}] = 0x{bot:02X}")
            print(f"MEM[0x{addr + 1:04X}] = 0x{top:02X}")
            print(f"READ MEM[0x{addr:04X}] = 0x{memory_read(addr):02X}")
            print(f"READ MEM[0x{addr + 1:04X}] = 0x{memory_read(addr + 1):02X}")

        elif pick == "3":
            word = input("Type a string (10 chars max): ")[:10]
            for row in ascii_dump(word):
                print(row)
            print(f"LENGTH (until 0x00) = {len(word)}")

        elif pick == "4":
            base = int(input("Base address: "))
            idx  = int(input("Element index: "))
            sz   = int(input("Bytes per element (1 or 2): "))
            op   = input("Operation - read or write: ").strip().lower()

            target = array_address(base, idx, sz)
            print(f"ADDRESS = {base} + {idx}*{sz} = 0x{target:04X}")

            if op == "write":
                val = int(input("Value to store: "))
                if sz == 1:
                    memory_write(target, val)
                    print(f"WRITE size=1 value={val} to ADDRESS 0x{target:04X}")
                else:
                    b0, b1 = pack16(val)
                    memory_write(target, b0)
                    memory_write(target + 1, b1)
                    print(f"WRITE size=2 value={val} to ADDRESS 0x{target:04X}")
            else:
                if sz == 1:
                    print(f"READ size=1 from ADDRESS 0x{target:04X} = {memory_read(target)}")
                else:
                    out = unpack16(memory_read(target), memory_read(target + 1))
                    print(f"READ size=2 from ADDRESS 0x{target:04X} = {out}")

        elif pick == "5":
            p1 = int(input("First param (a): "))
            p2 = int(input("Second param (b): "))
            for row in show_stack(p1, p2):
                print(row)
            print(f"AX = {p1}")
            print(f"BX = {p2}")
            print(f"AX (AX+BX) = {p1 + p2}")

        elif pick == "0":
            print("Closing tool.")
            running = False

        else:
            print("Not a valid choice, try again.")


if __name__ == "__main__":
    main()