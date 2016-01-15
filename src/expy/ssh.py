# based on https://gist.githubusercontent.com/johnfink8/2190472/raw/e4f3df6dde23309d3228986d0a1cc39c0a6ed9ac/ssh.py

import paramiko
import errno
import socket


class SSHSession(object):
    def __init__(self, hostname, username, key_file):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((hostname, 22))
        self.transport = paramiko.Transport(self.sock)
        self.transport.start_client()

        pkey = paramiko.RSAKey.from_private_key(key_file)
        self.transport.auth_publickey(username, pkey)

        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

        self.chan = self.transport.open_session()
        self.chan.invoke_shell()

    def path_exists(self, path):
        try:
            self.sftp.stat(path)
        except IOError, e:
            if e.errno == errno.ENOENT:
                return False
            raise e
        else:
            return True

    def create_path(self, path):
        session = self.transport.open_session()
        session.exec_command("mkdir -p {}".format(path))
        return not session.recv_exit_status()

    def command(self, cmd):
        self.chan.sendall(cmd + '\n')

    def put(self, localfile, remotefile):
        self.sftp.put(localfile, remotefile)

    def get(self, remotefile, localfile):
        self.sftp.get(remotefile, localfile)
