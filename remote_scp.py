#coding=utf-8
import paramiko, os


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


if __name__ == 'main':
    print('hello')
    remote_scp('remoteRead','192.168.0.203', '/home/xcache/wanglei/temp_xredirect/config.ini', 'D://remote_config.ini', 'root', 'jt123@')
