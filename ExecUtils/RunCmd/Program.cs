namespace RunCmd
{
    class Program
    {
        static void Main(string[] args)
        {
            string cmd = args[0];
            System.Diagnostics.Process.Start("cmd.exe", $"/c \"{cmd}\"");
        }
    }
}
