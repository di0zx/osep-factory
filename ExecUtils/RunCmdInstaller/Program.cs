namespace RunCmdInstaller
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
        string cmd = System.IO.File.ReadAllText(@"C:\Users\Public\cmd.txt");
        System.Diagnostics.Process.Start("cmd.exe", $"/c \"{cmd}\"");
    }
}