# network_config_auto_backup

## Overview

  A Python script that automates network device management by reading device credentials from an Excel file (Info.xls), connecting to each device via SSH, and executing commands from text files in the commands folder.
  
## File Structure
    .
    ├── main.py
    ├── Info.xls                   # Excel file containing device credentials (IP, username, password)
    ├── commands/                  # Directory containing text files with commands for devices
    │   ├── command1.txt
    │   └── command2.txt
    └── confg_bak/                    # Directory for storing device configuration backups
        ├── device1.log
        └── device2.log

## How It Works
1.Input:The script will read device information (IP, username, password, etc) from the Info.xls file.

2.Command Execution: The script will access the commands/ folder, read the corresponding .txt files as specified in the Info.xls, and execute the device configuration commands.

3.Device Connection: The script will connect to each network device via SSH using the provided credentials.

4.Command Execution: The commands will be executed on each device.

5.Output: The output from each command will be saved in the output/ folder for future reference.

## Notes 

  1.Ensure the devices are reachable from the machine running the script.

  2.The script use SSH access to network devices.


