import pandas as pd
import shutil
import os
import paramiko
import datetime
import time
import traceback
from concurrent.futures import ThreadPoolExecutor


class GetInfo:
    # 读取excel文件，获取交换机信息

    def __init__(self):
        self.excel = 'info.xls'

    def get_hosts(self):
        data = pd.read_excel(self.excel)
        # 读取excel文件
        return data["hostname"], data["ip"], data["username"], data["password"], data["commands"]

    @staticmethod
    def get_commands(file_name, folder_path="commands"):
        file_path = os.path.join(folder_path, f"{file_name}.txt")
        try:
            with open(file_path, encoding='utf-8') as fn:
                ls = fn.readlines()
            return ls
        except FileNotFoundError:
            print(f" {file_path} not found")
            return []


class CreateFiles:
    # 创建文件夹
    # 创建文本文件

    def __init__(self):
        self.now = datetime.datetime.now().strftime('%Y%m%d')
        self.file_path = 'data'

    def mkdir(self):
        # 创建目录，如果目录存在先删除再创建
        try:
            os.makedirs(self.file_path)
        except FileExistsError:
            shutil.rmtree(self.file_path)
            os.makedirs(self.file_path)

    def create_log(self, dis_cu, hn):
        # 创建文本文件保存配置
        file = open(f"{self.file_path}/{hn}.log", 'wb')
        for config in dis_cu:
            try:
                file.write(config)
            except TypeError:
                file.write(config.encode('utf-8'))
        file.close()
    @staticmethod
    def create_error_log(hn):
        with open(f"error.log", 'a') as errorInfo:
            errorInfo.write(f'\n[{time.strftime("%Y-%m-%d %X")}]{hn}:\n')
            traceback.print_exc(file=errorInfo)


def decide_stdout(stdout):
    # 判断交换机登陆后是否有[y/n]修改密码提示
    o = stdout.strip().lower().decode()
    if 'y/n' in o:
        return 'y'
    else:
        return 'n'


def backup_config(device_name, ip, username, password, comm):
    # 保存交换机配置
    mk = CreateFiles()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 自动保存公钥
    try:
        dis_cu = [f"{time.strftime('%Y%m%d %X')}\r\n"]
        print(f"{device_name}backup start！")
        # ssh.connect(hostname=ip, username=username, password=password, timeout=30)
        ssh.connect(hostname=ip, username=username, password=password)
        ssh_shell = ssh.invoke_shell()
        # get shell
        time.sleep(1)
        stdout = ssh_shell.recv(1024)
        # dis_cu.append(stdout)
        # 判断是否存在修改密码提示
        out = decide_stdout(stdout)
        time.sleep(1)
        if out == 'y':
            ssh_shell.send(b'n\n')
        # 从txt获取命令
        commands = GetInfo.get_commands(comm)
        # print(commands)
        for command in commands:
            ssh_shell.send(command.encode(encoding='utf-8'))
            ssh_shell.send(b'\n')
        time.sleep(10)
        num = 0
        while True:
            num += 1
            stdout = ssh_shell.recv(1024000)
            dis_cu.append(stdout)
            ssh_shell.send(b'\n')
            time.sleep(10)
            if dis_cu[num - 1] == dis_cu[num]:
                break
            # 判断输出是否结束
        ssh.close()
        # 关闭ssh会话
        mk.create_log(dis_cu, device_name)
        # print(f"{device_name}backup succeed。")


    except Exception:
        print(f"{device_name} failed。")
        mk.create_error_log(device_name)


def multithreading(devices):
    with ThreadPoolExecutor(max_workers=150) as executor:
        for hn, ip, un, pw, co in zip(*devices):  # 使用 * 解包 hosts 元组
            executor.submit(backup_config, hn, ip, un, pw, co)


if __name__ == '__main__':
    print('start')
    mk_dir = CreateFiles()
    mk_dir.mkdir()
    hosts = GetInfo().get_hosts()
    multithreading(hosts)