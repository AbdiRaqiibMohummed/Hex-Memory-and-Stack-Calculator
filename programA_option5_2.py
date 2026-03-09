"""
CMP5361 Task 1 - Hex, Memory, and Stack Calculator (programA.py)

Implements menu Options 1–5 to match the assessment brief output formats.

Notes:
- Uses a toy memory model: a dictionary mapping addresses (int) -> byte values (0..255).
- Core logic is kept in small functions to make unit testing straightforward.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


# -----------------------------
# Toy memory model (byte-addressable)
# -----------------------------
ToyMemory = Dict[int, int]


def memory_write(mem: ToyMemory, addr: int, byte: int) -> None:
    """Write a single byte (0..255) to toy memory at addr."""
    if not (0 <= byte <= 0xFF):
        raise ValueError("byte must be in 0..255")
    if addr < 0:
        raise ValueError("addr must be non-negative")
    mem[addr] = byte


def memory_read(mem: ToyMemory, addr: int) -> int:
    """Read a single byte from toy memory at addr. Unwritten addresses read as 0x00."""
    if addr < 0:
        raise ValueError("addr must be non-negative")
    return mem.get(addr, 0)


def parse_int_allow_hex(prompt: str) -> int:
    """
    Parse an integer from user input.
    Accepts decimal like '123' or hex like '0x2000'.
    """
    raw = input(prompt).strip()
    # int(x, 0) accepts 0x.., 0b.., 0o.. and plain decimal
    return int(raw, 0)


def fmt_addr(addr: int) -> str:
    """Format addresses like 0x2000 (uppercase hex digits)."""
    # use at least 4 hex digits for readability (matches examples like 0x2000, 0x1000, 0x3004)
    return f"0x{addr:04X}"


def fmt_byte(byte: int) -> str:
    """Format a byte like 0xE8 (uppercase)."""
    return f"0x{byte:02X}"


# -----------------------------
# Option 1 - Convert (decimal -> hex, BIN(16), SIGNED16)
# -----------------------------
def bin16(n: int) -> str:
    if not (0 <= n <= 0xFFFF):
        raise ValueError("n must be in 0..65535")
    return format(n, "016b")  # always 16 chars


def signed16(n: int) -> int:
    if not (0 <= n <= 0xFFFF):
        raise ValueError("n must be in 0..65535")
    return n if n < 0x8000 else n - 0x10000


def hex_u16(n: int) -> str:
    if not (0 <= n <= 0xFFFF):
        raise ValueError("n must be in 0..65535")
    return f"0x{n:04X}"


def option1_run() -> None:
    n = parse_int_allow_hex("Enter n (0..65535): ")
    # Per brief we assume input in range, but still guard:
    if not (0 <= n <= 0xFFFF):
        print("Invalid n. Must be 0..65535.")
        return
    print(f"HEX = {hex_u16(n)}")
    print(f"BIN(16) = {bin16(n)}")
    print(f"SIGNED16 = {signed16(n)}")


# -----------------------------
# Option 2 - Little-endian pack/unpack (16-bit) + memory write/read
# -----------------------------
def pack_u16_le(n: int) -> Tuple[int, int]:
    if not (0 <= n <= 0xFFFF):
        raise ValueError("n must be in 0..65535")
    low = n & 0xFF
    high = (n >> 8) & 0xFF
    return low, high


def unpack_u16_le(low: int, high: int) -> int:
    if not (0 <= low <= 0xFF and 0 <= high <= 0xFF):
        raise ValueError("low/high must be bytes 0..255")
    return low | (high << 8)


def option2_run(mem: ToyMemory) -> None:
    n = parse_int_allow_hex("Enter n (0..65535): ")
    if not (0 <= n <= 0xFFFF):
        print("Invalid n. Must be 0..65535.")
        return

    addr = parse_int_allow_hex("Enter addr (decimal or hex, e.g. 0x2000): ")
    if addr < 0:
        print("Invalid addr. Must be non-negative.")
        return

    low, high = pack_u16_le(n)
    print(f"LOW BYTE = {low}")
    print(f"HIGH BYTE = {high}")

    # write little-endian bytes
    memory_write(mem, addr, low)
    memory_write(mem, addr + 1, high)

    # evidence lines (style from brief)
    print(f"MEM[{fmt_addr(addr)}] = {fmt_byte(low)}")
    print(f"MEM[{fmt_addr(addr + 1)}] = {fmt_byte(high)}")

    r0 = memory_read(mem, addr)
    r1 = memory_read(mem, addr + 1)
    print(f"READ MEM[{fmt_addr(addr)}] = {fmt_byte(r0)}")
    print(f"READ MEM[{fmt_addr(addr + 1)}] = {fmt_byte(r1)}")

    unpacked = unpack_u16_le(r0, r1)
    print(f"UNPACKED = {unpacked}")


# -----------------------------
# Option 3 - ASCII memory dump + null terminator + length scan
# -----------------------------
def ascii_dump_lines(s: str, base: int = 0x1000, mem: Optional[ToyMemory] = None) -> Tuple[List[str], int]:
    """
    Return (dump_lines, length_until_null).
    Writes to mem if provided, otherwise uses an internal temporary memory dict.
    """
    if len(s) > 10:
        raise ValueError("s must be at most 10 characters")

    local_mem: ToyMemory = mem if mem is not None else {}
    # store characters
    for i, ch in enumerate(s):
        memory_write(local_mem, base + i, ord(ch) & 0xFF)
    # store null terminator
    memory_write(local_mem, base + len(s), 0x00)

    # build dump lines including null terminator
    dump_lines: List[str] = []
    for i in range(len(s) + 1):
        addr = base + i
        dump_lines.append(f"{fmt_addr(addr)} : {fmt_byte(memory_read(local_mem, addr))}")

    # length scan until 0x00
    length = 0
    while memory_read(local_mem, base + length) != 0x00:
        length += 1

    return dump_lines, length


def option3_run(mem: ToyMemory) -> None:
    s = input("Enter s (max 10 chars): ")
    if len(s) > 10:
        print("Invalid s. Maximum 10 characters.")
        return

    base = 0x1000
    lines, length = ascii_dump_lines(s, base=base, mem=mem)
    for line in lines:
        print(line)
    print(f"LENGTH (until 0x00) = {length}")


# -----------------------------
# Option 4 - Array addressing + dereference (read/write one element)
# -----------------------------
def element_address(base: int, index: int, size: int) -> int:
    if size not in (1, 2):
        raise ValueError("size must be 1 or 2")
    if base < 0 or index < 0:
        raise ValueError("base and index must be non-negative")
    return base + index * size


def write_element(mem: ToyMemory, addr: int, size: int, value: int) -> None:
    if size == 1:
        if not (0 <= value <= 0xFF):
            raise ValueError("value must be 0..255 for size=1")
        memory_write(mem, addr, value)
    elif size == 2:
        if not (0 <= value <= 0xFFFF):
            raise ValueError("value must be 0..65535 for size=2")
        low, high = pack_u16_le(value)
        memory_write(mem, addr, low)
        memory_write(mem, addr + 1, high)
    else:
        raise ValueError("size must be 1 or 2")


def read_element(mem: ToyMemory, addr: int, size: int) -> int:
    if size == 1:
        return memory_read(mem, addr)
    if size == 2:
        low = memory_read(mem, addr)
        high = memory_read(mem, addr + 1)
        return unpack_u16_le(low, high)
    raise ValueError("size must be 1 or 2")


def option4_run(mem: ToyMemory) -> None:
    base = parse_int_allow_hex("Enter base (address): ")
    index = parse_int_allow_hex("Enter index (i): ")
    size = parse_int_allow_hex("Enter size (1 or 2): ")

    try:
        addr = element_address(base, index, size)
    except ValueError as e:
        print(f"Invalid input: {e}")
        return

    # Required output line
    print(f"ADDRESS = base + index*size = {fmt_addr(addr)}")

    mode = input("Enter mode (read/write): ").strip().lower()
    if mode not in ("read", "write"):
        print("Invalid mode. Must be 'read' or 'write'.")
        return

    if mode == "write":
        value = parse_int_allow_hex("Enter value (only for write): ")
        try:
            write_element(mem, addr, size, value)
        except ValueError as e:
            print(f"Invalid value: {e}")
            return
        # Required style message
        print(f"WRITE size={size} value={value} to ADDRESS {fmt_addr(addr)}")
    else:
        value = read_element(mem, addr, size)
        print(f"READ size={size} from ADDRESS {fmt_addr(addr)} = {value}")


# -----------------------------
# Option 5 - Stack frame (simplified bp offsets) + register-style view
# -----------------------------
def stack_frame_lines(a: int, b: int) -> List[str]:
    """
    Return the required output lines for Option 5.
    Assumptions from the brief:
    - return address is at bp
    - first parameter is at bp+2
    - second parameter is at bp+4
    """
    return [
        "bp : RETURN",
        f"bp+2 : a = {a}",
        f"bp+4 : b = {b}",
        f"AX = {a}",
        f"BX = {b}",
        f"AX (AX+BX) = {a + b}",
    ]


def option5_run() -> None:
    a = parse_int_allow_hex("Enter a: ")
    b = parse_int_allow_hex("Enter b: ")
    for line in stack_frame_lines(a, b):
        print(line)


# -----------------------------
# Menu
# -----------------------------
MENU = """\
---- Hex | memory | stack calculator ----

1) Convert (decimal → hex and 16-bit binary)
2) Little-endian pack/unpack (16-bit)
3) ASCII memory dump
4) Array addressing
5) Stack frame (bp offsets)
0) Exit
"""


def main() -> None:
    mem: ToyMemory = {}  # shared memory across options (2–4)
    while True:
        print(MENU)
        try:
            choice = int(input("Select an Option from 0-5: ").strip())
        except ValueError:
            print("Invalid input. Please enter a number 0-5.")
            continue

        if choice == 0:
            print("exiting system")
            break
        elif choice == 1:
            option1_run()
        elif choice == 2:
            option2_run(mem)
        elif choice == 3:
            option3_run(mem)
        elif choice == 4:
            option4_run(mem)
        elif choice == 5:
            option5_run()
        else:
            print("Invalid option. Please enter a number 0-5.")


if __name__ == "__main__":
    main()
