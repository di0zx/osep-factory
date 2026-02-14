def to_csharp_array(shellcode_bytearray):
    shellcode_len = len(shellcode_bytearray)
    return f"new byte[{shellcode_len}] {{ {''.join(hex(shellcode_bytearray[i]) + (',' if i != shellcode_len -1 else '') for i in range(0, shellcode_len))} }}"

def to_vba_array(shellcode_bytearray):
    shellcode_len = len(shellcode_bytearray)
    res = "Array("
    for i in range (0, shellcode_len):
        res += str(int(shellcode_bytearray[i]))
        if i != shellcode_len -1:
            res += ','
            if i > 0 and i % 50 == 0:
                res += ' _\n'
    res += ")"
    return res

def to_powershell_array(shellcode_bytearray):
    shellcode_len = len(shellcode_bytearray)
    return f"{''.join(hex(shellcode_bytearray[i]) + (',' if i != shellcode_len -1 else '') for i in range(0, shellcode_len))}"
    
def to_c_array(shellcode_bytearray):
    shellcode_len = len(shellcode_bytearray)
    return '"' + ''.join('\\x' + format(byte, '02x') for byte in shellcode_bytearray) + '"'