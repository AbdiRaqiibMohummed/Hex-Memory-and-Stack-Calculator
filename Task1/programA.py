# output

# 1) Convert (decimal à hex and 16-bit binary)
# 2) Little-endian pack/unpack (16-bit)
# 3) ASCII memory dump
# 4) Array addressing
# 5) Stack frame (bp offsets)
# 0) Exit
# The user enters an option (0–5). The programme performs that option, then returns to the menu
# until the user chooses 0.


# Option 1: Convert (decimal → hex and binary)
# Input: integer n (assume 0 ≤ n ≤ 65535)
# Output must include these two lines:
# • HEX = <hex value>
# • BIN(16) = <16-bit binary string>
# • SIGNED16 = <signed interpretation>
# Rules:
# • BIN(16) must always be 16 characters long (pad with leading zeros).
# • SIGNED16 interprets the same 16-bit pattern as two’s complement:
# • if n < 32768 → SIGNED16 = n
# • if n ≥ 32768 → SIGNED16 = n − 65536
# • Example: n = 65535 → BIN(16)=1111111111111111 and SIGNED16 = -1


def convert():
    n = int(input("\nEnter a number to convert: "))
    convert_to_hex = hex(n)
    
    output = f"""
    Hex = {convert_to_hex}
    """
    print(output)
    
def little_endian_pack_16_bit():
    print("pack")

def little_endian_unpack_16_bit():
    print("unpack")

def ascii_memory_dump():
    print("ascii dump")

def array_addressing():
    print("array addressing")
    
def stack_frame():
    print("stack framing")

    


def main():
    menu = """
  ---- Hex | memory | stack calculator ----
    
  1) Convert (decimal → hex and 16-bit binary)
  2) Little-endian pack/unpack (16-bit)
  3) ASCII memory dump
  4) Array addressing
  5) Stack frame (bp offsets)
  0) Exit
    """
    while True:
        print(menu)
        choice = int(input("Select an Option from 0-5: "))
        
        match choice:
            case 0: 
                # this wil exit the system successfully
                print("exiting system")
                break
            
            case 1:
                convert() 
                # goint to run the function here
                break
            
        
        
if __name__ == "__main__":
    main()