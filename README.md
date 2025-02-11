# 自动备份设备配置脚本 / network_config_auto_backup

## 概述 / Overview

  一个 Python 脚本，通过读取 Excel 文件 (Info.xls) 中的设备凭证，使用 SSH 连接每个设备，并执行 commands 文件夹下的文本命令文件。执行结果将被保存，以便日后查看或备份。 
 
 A Python script that automates network device management by reading device credentials from an Excel file (Info.xls), connecting to each device via SSH, and executing commands from text files in the commands folder. 

## 文件结构 / File Structure
    .
    ├── main.py
    ├── Info.xls                   # 包含设备凭证（IP，用户名，密码）的 Excel 文件 / Excel file containing device credentials (IP, username, password)
    ├── commands/                  # 包含设备命令的文本文件目录 / Directory containing text files with commands for devices
    │   ├── command1.txt
    │   └── command2.txt
    └── confg_bak/                    # 存放设备配置备份的目录 / Directory for storing device configuration backups
        ├── device1.log
        └── device2.log

## How It Works / 工作原理
1.输入：脚本从 Info.xls 文件读取设备信息（IP，用户名，密码等）.
  Input:The script will read device information (IP, username, password, etc) from the Info.xls file.

2.命令执行：脚本将访问 commands/ 文件夹，并读取xls中应对 .txt 文件，执行设备配置命令。
  Command Execution: The script will access the commands/ folder, read the corresponding .txt files as specified in the Info.xls, and execute the device configuration commands.

3.设备连接：脚本将使用提供的凭证通过 SSH 连接每个设备。
  Device Connection: The script will connect to each network device via SSH using the provided credentials.

4.命令执行：脚本将在每台设备上执行命令。
  Command Execution: The commands will be executed on each device.

5.输出：每个命令的输出将保存到 config_bak/ 文件夹，供日后参考。
  Output: The output from each command will be saved in the output/ folder for future reference.

## 注意事项 / Notes 

1.请确保设备可以从运行脚本的机器访问。 
  Ensure the devices are reachable from the machine running the script.

2.脚本通过 SSH 访问设备。
  The script use SSH access to network devices.


