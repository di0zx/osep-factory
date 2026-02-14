# osep-factory

A payload generation framework that automates the creation of pre and post-exploitation utilities. It uses Metasploit (`msfvenom`) to generate raw shellcodes and then wraps them into various delivery formats with encryption to evade antivirus detection.

## How it works

The main entry point is `generate_tools.sh`. When executed, it:

1. Generates raw Meterpreter reverse-TCP shellcodes via `msfvenom` for multiple architectures (Windows x64, Windows x86, Linux x64) in both staged and unstaged variants.
2. Encrypts the shellcodes using a Caesar cipher (configurable key) and injects them into language-specific templates.
3. Compiles the resulting C# projects and copies all artifacts into a `tools/` output directory.

## Generated artifacts

| Artifact | Description |
|---|---|
| **ASPX webshell** (`web/met.aspx`) | Encrypted shellcode embedded in an ASPX page with runtime Caesar decryption |
| **VBA macros** (`macros/runner.vba`) | Office macro that decrypts and executes shellcode in-process |
| **VBA PowerShell macro** (`macros/runner_powershell.vba`) | Office macro that downloads and executes a PowerShell runner |
| **C# Runner** (`Runner.exe`) | Shellcode runner using `VirtualAllocExNuma` for sandbox evasion |
| **C# DynamicRunner** (`DynamicRunner.exe`) | Shellcode runner using dynamic API resolution |
| **C# ProcessInjector** (`ProcessInjector.exe`) | Injects shellcode into a remote process via `OpenProcess`/`VirtualAllocEx`/`WriteProcessMemory` |
| **C# ProcessHollowing** (`ProcessHollowing.exe`) | Spawns a suspended process and replaces its memory with shellcode |
| **C# RemoteServiceRunner** (`RemoteServiceRunner.exe`) | Executes shellcode through a Windows service |
| **DotNet2Jscript** (`DotNet2Jscript.zip`) | Converts the C# shellcode runner into a JScript/VBScript/VBA payload via .NET serialization |
| **ELF runner** (`elf_runner`) | Native Linux x64 binary with embedded encrypted shellcode |
| **PowerShell runners** (`powershell/runner.ps1`) | PowerShell scripts with AMSI bypass that decrypt and execute shellcode |
| **SQL tools** (`SQL/SQLExec.exe`) | SQL Server query executor with Windows integrated authentication |

## Configuration

Key variables at the top of `generate_tools.sh`:

```
KEY=7                              # Caesar cipher shift key
METERPRETER_WIN64_PORT=8080        # Meterpreter listener ports
METERPRETER_LIN64_PORT=8081
METERPRETER_WIN32_PORT=8082
HTTP_SERVER_PORT=8000              # HTTP server for staging PowerShell scripts
IFACE=enp3s0                       # Network interface for IP auto-detection
```

## Bundled PowerShell scripts

The `powershell/` directory includes several well-known offensive PowerShell tools:

- **PowerView.ps1** / **PowerView.patched.ps1** - Active Directory enumeration (with AMSI-patched variant)
- **PowerUp.ps1** - Windows privilege escalation checks
- **PowerUpSQL.ps1** - SQL Server security assessment
- **LAPSToolkit.ps1** / **LAPSRecon.ps1** - LAPS password retrieval
- **roast.ps1** - Kerberoasting / AS-REP roasting
- **HostRecon.ps1** - Local host reconnaissance
- **port-scan-tcp.ps1** - TCP port scanner
- **amsi.ps1** - AMSI bypass

## Project structure

```
osep-factory/
├── generate_tools.sh           # Main build script
├── scripts/                    # Python payload generators
│   ├── common/
│   │   ├── encrypt_utils.py    # Caesar & XOR encryption
│   │   └── shellcode_formator.py
│   ├── aspx_maker.py
│   ├── vba_maker.py
│   ├── csharp_runner_maker.py
│   ├── process_injector_maker.py
│   ├── process_hollowing_maker.py
│   ├── elf_runner_maker.py
│   └── ...
├── ShellcodeRunners/           # C# solution with runner projects
├── DotNetToJScript/            # .NET-to-script conversion tool
├── ExecUtils/                  # Command execution & CLM bypass tools
├── SQL/                        # SQL Server interaction tools
└── powershell/                 # Offensive PowerShell scripts
```

## Prerequisites

- Metasploit Framework (`msfvenom`)
- Mono (`xbuild`) for compiling C# solutions
- Python 3
- GCC cross-compiler (`x86_64-linux-gnu-gcc`) for the ELF runner

## Usage

```bash
./generate_tools.sh
```

All output is written to the `tools/` directory.