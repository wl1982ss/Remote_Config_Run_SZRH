from invoke import task
from fabric import Connection
import paramiko, os
import codecs


system_config = dict()
config_ini_conf = dict()    # config.ini 的配置参数
cachetable_conf = dict()    #cachetable.pattern 的 配置参数
forbidip_conf = dict()      #forbidip.pattern 的 配置参数


@task
def hello(c):
    conn = Connection(host='192.168.0.203', user='root', connect_kwargs={"password": "jt123@"})
    conn.run("ls /home")


# 远程拷贝，上传文件
def remote_scp(type, host_ip, remote_path, local_path, username, password):
    ssh_port = 22
    try:
        print(host_ip)
        conn = paramiko.Transport((host_ip, ssh_port))
        print(conn)
        conn.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(conn)
        print(sftp)
        if type == 'remoteRead':
            print("remoteRead:")
            if not local_path:
                fileName = os.path.split(remote_path)
                local_path = os.path.join('/tmp', fileName[1])
            print(local_path)
            sftp.get(remote_path, local_path)

        if type == 'remoteWrite':
            sftp.put(local_path, remote_path)

        conn.close()
        return True

    except Exception:
        return False


# 修改 config.ini 文件的配置
def modify_config_ini():
    # 远程获取 config.ini 文件
    flag = remote_scp('remoteRead', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/config.ini', os.getcwd() +'/remote_config.ini', 'root', 'jt123@')

    # 读取 remote_config.ini 文件内容
    config_ini_file = open(os.getcwd() + "/remote_config.ini", 'rb')
    line = config_ini_file.readline().decode()

    new_config_ini_file = codecs.open(os.getcwd() + "/new_remote_config.ini", 'w', 'utf-8')

    while line:
        tmp_pos1 = line.find("#")
        tmp_pos2 = line.find("=")

        if tmp_pos1 == 0:  # 以#号开头的行，跳过
            new_config_ini_file.write(line)
            line = config_ini_file.readline().decode()
            continue

        if tmp_pos2 == -1:  # 不含 = 号的行，跳过
            new_config_ini_file.write(line)
            line = config_ini_file.readline().decode()
            continue

        strlist = line.split(' = ')
        if strlist[0].strip() in config_ini_conf.keys():
            new_config_ini_file.write(strlist[0].strip() + ' = ' + config_ini_conf[strlist[0]].strip() + '\n')
        else:
            new_config_ini_file.write(line)

        line = config_ini_file.readline().decode()

    config_ini_file.close()
    new_config_ini_file.close()

    # 将新生成的 config.ini 文件 传回 远程服务器
    flag = remote_scp('remoteWrite', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/config.ini', os.getcwd() + '/new_remote_config.ini', 'root', 'jt123@')


# 修改 cachetable.patterns 文件的配置
def modify_cachetable():
    # 远程获取 cachetable.patterns 文件
    flag = remote_scp('remoteRead', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/cachetable.patterns', os.getcwd() +'/remote_cachetable.patterns', 'root', 'jt123@')

    # 读取 remote_cachetable.patterns 文件内容
    cachetable_file = open(os.getcwd() + "/remote_cachetable.patterns", 'rb')
    line = cachetable_file.readline().decode()

    new_cachetable_file = codecs.open(os.getcwd() + "/new_remote_cachetable.patterns", 'w', 'utf-8')

    while line:
        tmp_pos1 = line.find("#")
        tmp_pos2 = line.find("=")

        if tmp_pos1 == 0:  # 以#号开头的行，跳过
            new_cachetable_file.write(line)
            line = cachetable_file.readline().decode()
            continue

        if tmp_pos2 == -1:  # 不含 = 号的行，跳过
            new_cachetable_file.write(line)
            line = cachetable_file.readline().decode()
            continue

        strlist = line.split(' = ')
        print(strlist[0])
        if strlist[0].strip() in cachetable_conf.keys():
            new_cachetable_file.write(strlist[0].strip() + ' = ' + cachetable_conf[strlist[0]].strip() + '\n')
        else:
            new_cachetable_file.write(line)

        line = cachetable_file.readline().decode()

    cachetable_file.close()
    new_cachetable_file.close()

    print("cache table value is : \n")
    for key, value in cachetable_conf.items():
        print(key + " is:")
        print(value)

    # 将新生成的 cachetable.patterns 文件 传回 远程服务器
    flag = remote_scp('remoteWrite', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/new_cachetable.patterns', os.getcwd() + '/new_remote_cachetable.patterns', 'root', 'jt123@')


# 修改 forbidip.patterns 文件的配置
def modify_forbidip():
    # 远程获取 forbidip.patterns 文件
    flag = remote_scp('remoteRead', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/forbidip.patterns', os.getcwd() +'/remote_forbidip.patterns', 'root', 'jt123@')

    # 读取 remote_forbidip.patterns 文件内容
    forbidip_file = open(os.getcwd() + "/remote_forbidip.patterns", 'rb')
    line = forbidip_file.readline().decode()

    new_forbidip_file = codecs.open(os.getcwd() + "/new_remote_forbidip.patterns", 'w', 'utf-8')

    while line:
        tmp_pos1 = line.find("#")
        tmp_pos2 = line.find("=")

        if tmp_pos1 == 0:  # 以#号开头的行，跳过
            new_forbidip_file.write(line)
            line = forbidip_file.readline().decode()
            continue

        if tmp_pos2 == -1:  # 不含 = 号的行，跳过
            new_forbidip_file.write(line)
            line = forbidip_file.readline().decode()
            continue

        strlist = line.split(' = ')
        print(strlist[0])
        if strlist[0].strip() in forbidip_conf.keys():
            new_forbidip_file.write(strlist[0].strip() + ' = ' + forbidip_conf[strlist[0]].strip() + '\n')
        else:
            new_forbidip_file.write(line)

        line = forbidip_file.readline().decode()

    forbidip_file.close()
    new_forbidip_file.close()

    print("forbid ip value is : \n")
    for key, value in forbidip_conf.items():
        print(key + " is:")
        print(value)

    # 将新生成的 forbidip.patterns 文件 传回 远程服务器
    flag = remote_scp('remoteWrite', '192.168.0.203', '/home/xcache/wanglei/temp_xredirect/new_forbidip.patterns', os.getcwd() + '/new_remote_forbidip.patterns', 'root', 'jt123@')


@task
def modify(c):

    # 读取安装配置文件
    f = open("D:\wanglei\Project\Python_Project\Remote_Config_Run_SZRH\systemProperty.txt")
    line = f.readline()

    while line:

        tmp_pos1 = line.find('#')
        tmp_pos2 = line.find('=')

        if tmp_pos1 == 0:       # 以#号开头的行，跳过
            line = f.readline()
            continue

        if tmp_pos2 == -1:      # 不含 = 号的行，跳过
            line = f.readline()
            continue

        strlist_1 = line.split('.')

        if strlist_1[0] == 'config_ini':
            strlist_2 = strlist_1[1].split('=')
            config_ini_conf[strlist_2[0].strip()] = strlist_2[1].strip()
        elif strlist_1[0] == 'cachetable':
            strlist_2 = strlist_1[1].split('=')
            cachetable_conf[strlist_2[0].strip()] = strlist_2[1].strip()
        elif strlist_1[0] == 'forbidip':
            strlist_2 = strlist_1[1].split('=')
            forbidip_conf[strlist_2[0].strip()] = strlist_2[1].strip()
        else:
            strlist_2 = line.split('=')
            system_config[strlist_2[0].strip()] = strlist_2[1].strip()

        line = f.readline()

    f.close()

    # 修改xredirect 的 config.ini 文件
    modify_config_ini()

    # 修改xredirect 的 cachetable.pattern 文件
    modify_cachetable()

    # 修改xredirect 的 forbidip.pattern 文件
    modify_forbidip()


@task
def test(c):
    conn = Connection(host='192.168.0.203', user='root', connect_kwargs={"password": "jt123@"})
    conn.run("ls /home")
