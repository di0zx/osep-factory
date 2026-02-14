from common.encrypt_utils import Algorithm, EncryptUtils
from common.shellcode_formator import *
import sys

lang = sys.argv[1]
raw_shellcode = sys.argv[2]

with open(raw_shellcode, 'rb') as f:
    shellcode_bytes = f.read()
    encryptor = EncryptUtils(Algorithm.CAESAR, 7)
    encrypted_shellcode = encryptor.encrypt(shellcode_bytes)
    if lang == 'csharp':
        print(to_csharp_array(encrypted_shellcode))
    elif lang == 'vba':
        print(to_vba_array(encrypted_shellcode))
    elif lang == 'powershell':
        print(to_powershell_array(encrypted_shellcode))
    elif lang == 'c':
        print(to_c_array(encrypted_shellcode))