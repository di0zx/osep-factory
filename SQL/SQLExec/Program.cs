using System;
using System.Data.SqlClient;
using System.Collections.Generic;

namespace SQLExec
{
    class Program
    {
        static void Main(string[] args)
        {
            if (args.Length != 4)
            {
                Console.WriteLine($"Usage: {System.AppDomain.CurrentDomain.FriendlyName} server database (--file query_file | --query query)");
                Environment.Exit(0);
            }
            String sqlServer = args[0];
            String database = args[1];
            String mode = args[2];
            List<string> queries = new List<string>();
            if (mode == "--file")
            {
                foreach (string line in System.IO.File.ReadAllLines(args[3]))
                {
                    queries.Add(line);
                }
            }
            else if (mode == "--query")
            {
                foreach (string token in args[3].Replace("\\n","\n").Split('\n'))
                {
                    queries.Add(token);
                }
            }
            else
            {
                Console.WriteLine($"Usage: {System.AppDomain.CurrentDomain.FriendlyName} server database (--file query_file | --query query)");
                Environment.Exit(0);
            }

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
}
