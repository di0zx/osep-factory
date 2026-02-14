from enum import Enum

CSHARP_CAESAR_TEMPLATE = """
byte[] buf = new byte[enc.Length];
for(int i = 0; i < enc.Length; i++)
{
buf[i] = (byte)(((uint)enc[i] - key) & 0xFF);
}
return buf;
"""

class Algorithm(Enum):
    CAESAR=0
    XOR=1

class Language(Enum):
    CSHARP=0
    POWERSHELL=1
    VBA=2

class EncryptUtils:

    def __init__(self, alg, key):
        self._alg = alg
        self._key = key


    def _encrypt_caesar(self, raw_shellcode):
        encrypted_shellcode = bytearray(len(raw_shellcode))
        for i in range(0, len(raw_shellcode)):
            encrypted_shellcode[i] = (raw_shellcode[i] + self._key) & 0xFF
        return encrypted_shellcode

    def _encrypt_xor(self, raw_shellcode):
        encrypted_shellcode = bytearray(len(raw_shellcode))
        for i in range(0, len(raw_shellcode)):
            encrypted_shellcode[i] = raw_shellcode[i] ^ self._key
        return encrypted_shellcode

    def _get_decrypt_method_caesar(self, language):
        if language == Language.CSHARP:
            return CSHARP_CAESAR_TEMPLATE
            

    def encrypt(self, raw_shellcode):
        if self._alg == Algorithm.CAESAR:
            return self._encrypt_caesar(raw_shellcode)
        elif self._alg == Algorithm.XOR:
            return self._encrypt_xor(raw_shellcode)


    def get_decrypt_method(self, language):
        if self._alg == Algorithm.CAESAR:
            return self._get_decrypt_method_caesar(language)
