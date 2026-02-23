# CMP5361 – Computer Mathematics and Declarative Programming

Academic Year 2025–26

## Assessment Overview

This module assessment consists of:

* **Group Project (60%)**

  * Task 1 (40%) – Deadline: 16 March
  * Task 2 (20%) – Deadline: 30 March

* **Final Exam (40%)**

  * Exam Date: 24 April
  * Extenuating Circumstances / Student Support Deadline: 11 May

Group size: 6 students (one submission per group).

---

# Task 1 (40%) – Hex, Memory, and Stack Calculator

## Purpose

Task 1 assesses your understanding through a small, fixed-scope Python program. You will implement a menu-driven tool that demonstrates core computing and low-level programming concepts.

The task supports the module’s declarative and functional programming goals. You are expected to:

* Structure your solution as small, reusable input-to-output functions.
* Avoid mixing calculations with input and printing.
* Keep the menu interface imperative, but ensure core logic is predictable and has minimal side effects.
* Make the code easy to reason about and test automatically.

All groups must build the same program with the same required options and outputs.

---

# Concepts Demonstrated

Your program must demonstrate:

* Decimal, hexadecimal, and binary representations (including fixed-width 16-bit binary)
* Little-endian representation of 16-bit numbers
* Signed vs unsigned 16-bit interpretation (two’s complement)
* ASCII storage as bytes and a simple memory dump
* Array addressing using offsets (base + index × element size)
* Pointer-style memory access in a toy memory model
* A simplified stack-frame model (bp, bp+2, bp+4)
* A register-style view (e.g., AX/BX)
* Automated testing
* A clear written report with screenshots
* A short demo video

---

# Software Requirements

* Python version: 3.11 or higher
* External packages: Not required (use Python Standard Library only)

Testing framework (choose one):

* Option A: `unittest` (built-in)
* Option B: `pytest` (install separately if used)

Reference links:

* unittest: [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)
* Python Standard Library: [https://docs.python.org/3/library/index.html](https://docs.python.org/3/library/index.html)
* pytest: [https://docs.pytest.org/](https://docs.pytest.org/)

---

# Required Files

Your submission must include:

* `programA.py` – the main program
* `testA.py` – unit tests (unittest or pytest)
* `Task1_Report.pdf` – written report with screenshots and explanations
* `README.md` – instructions for running program and tests
* `Task1_DemoVideo.mp4`
  OR
  `Task1_DemoVideo_Link.txt` containing a shareable link

---

# Program Menu (Must Match Exactly)

When running `programA.py`, the program must display:

```
1) Convert (decimal → hex and 16-bit binary)
2) Little-endian pack/unpack (16-bit)
3) ASCII memory dump
4) Array addressing
5) Stack frame (bp offsets)
0) Exit
```

The program must:

* Accept user input (0–5)
* Execute the selected option
* Return to the menu
* Exit only when the user chooses 0

---

# Program Specifications

## Option 1 – Convert (decimal → hex and binary)

Input:

* Integer n (0 ≤ n ≤ 65535)

Output must include:

```
HEX = <hex value>
BIN(16) = <16-bit binary string>
SIGNED16 = <signed interpretation>
```

Rules:

* Binary must always be 16 characters (pad with leading zeros).
* SIGNED16 interpretation:

  * If n < 32768 → SIGNED16 = n
  * If n ≥ 32768 → SIGNED16 = n − 65536

Example:

* n = 65535
  BIN(16) = 1111111111111111
  SIGNED16 = -1

---

## Option 2 – Little-endian Pack/Unpack (16-bit) + Memory Write/Read

Input:

* Integer n (0 ≤ n ≤ 65535)
* Memory address addr (decimal or hex, e.g. 0x2000)

Output must include:

```
LOW BYTE = <0..255>
HIGH BYTE = <0..255>
UNPACKED = <number>
```

Rules:

* LOW BYTE = least significant 8 bits
* HIGH BYTE = next 8 bits
* UNPACKED must equal original n
* Write LOW BYTE to memory at addr
* Write HIGH BYTE to memory at addr+1
* Read both bytes back and print them

Example format:

```
MEM[0x2000] = 0xE8
MEM[0x2001] = 0x03
READ MEM[0x2000] = 0xE8
READ MEM[0x2001] = 0x03
```

---

## Option 3 – ASCII Memory Dump + Null Terminator

Input:

* String s (maximum 10 characters)

Rules:

* Base address: 0x1000
* Each character stored at next address (+1)
* Store null terminator (0x00) after last character
* Include null terminator in dump
* After dump, print:

```
LENGTH (until 0x00) = <number>
```

Output format:

```
0x1000 : 0xHH
```

---

## Option 4 – Array Addressing + Dereference

Input:

* base (address)
* index
* size (1 or 2 bytes)
* mode (read or write)
* value (if mode = write)

Output must include:

```
ADDRESS = base + index*size = <computed address>
```

If mode = write:

* Store value in memory
* If size = 1 → store 1 byte
* If size = 2 → store 2 bytes in little-endian
* Print confirmation

If mode = read:

* Read 1 or 2 bytes
* Print value

Example format:

```
WRITE size=2 value=1000 to ADDRESS 0x3004
READ size=2 from ADDRESS 0x3004 = 1000
```

---

## Option 5 – Stack Frame (Simplified) + Register View

Input:

* Two integers a and b

Assume:

* Return address at bp
* First parameter at bp+2
* Second parameter at bp+4

Output:

```
bp : RETURN
bp+2 : a = <value>
bp+4 : b = <value>
```

Then display:

```
AX = <a>
BX = <b>
AX (AX+BX) = <a+b>
```

No real memory simulation required.

---

# Unit Testing Requirements

Minimum:

* At least 10 meaningful tests
* Boundary tests for pack/unpack:

  * 0, 1, 255, 256, 65535
* At least one ASCII dump test
* At least one array addressing test
* At least one stack frame test
* At least one test ensuring BIN(16) is always 16 bits
* At least one SIGNED16 test (e.g. 65535 → -1)
* At least one memory write/read-back test

---

# Structuring Code for Testing

To make testing straightforward:

* Put main calculations in small functions.
* Keep input/output inside the menu only.
* Import functions into `testA.py` for testing.

Recommended helper functions:

* `convert(n)`
* `pack_u16_le(n)`
* `unpack_u16_le(low, high)`
* `ascii_dump_lines(s, base=0x1000)`
* `element_address(base, index, size)`
* `stack_frame_lines(a, b)`
* `memory_write(addr, byte)`
* `memory_read(addr)`

If using pytest, include installation instructions in README.

---

# Written Report Requirements

Your report must include:

## Overview

Short description of what the program does and what each option demonstrates.

## Screenshots (Minimum 10)

Must include:

1. Main menu
2. Output for Options 1–5
3. Test output showing passing tests
4. Memory write and read-back example

## Explanation of Each Option

For each option:

* What input is required?
* What output is printed?
* What computing idea is demonstrated?

## Testing Evidence

* Exact command used to run tests
* Screenshot showing tests passing

---

# Group Contribution and Individual Roles

Your report must include a section titled:

**Group Contribution and Individual Roles**

Include:

* A table listing each group member
* Their responsibilities
* What they delivered

Also include a short paragraph describing:

* How the group collaborated
* Division of tasks
* Integration process

Any student identified as not engaging or not collaborating may receive 0 for the assessment.

---

# Submission Format

Submit one zip file per group containing:

* programA.py
* testA.py
* Task1_Report.pdf
* Task1_DemoVideo.mp4
  OR
  Task1_DemoVideo_Link.txt
* README.md

README.md must include:

* Python version used
* How to run the program:

  ```
  python programA.py
  ```
* How to run tests:

For unittest:

```
python -m unittest
```

or

```
python -m unittest -v
```

For pytest:

```
python -m pip install pytest
pytest
```

or

```
pytest -q
```

If submitting a link instead of a video file, confirm staff access.

---

# Marking Criteria (40 Marks Total)

## A) Program Correctness – 25 Marks

* Menu works correctly
* Option 1 correct format and SIGNED16
* Option 2 correct pack/unpack and memory behavior
* Option 3 correct ASCII dump and null terminator
* Option 4 correct address calculation and read/write behavior
* Option 5 correct stack-frame display and register view

## B) Unit Tests – 5 Marks

* At least 10 meaningful tests
* Required boundary cases included
* SIGNED16 test included
* Memory write/read-back test included
* Tests run and pass
* Logic separated into testable functions

## C) Written Report – 10 Marks

* Clear overview
* Correct explanations
* Required screenshots included
* Testing evidence clearly shown

---

# Task 2

Task 2 details will be released within the next two weeks.

---

# Final Exam (40%)

Details provided separately by module staff.
