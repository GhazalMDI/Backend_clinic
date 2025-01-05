from time import sleep
import paramiko


class SSHException(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class SSHConnectionException(SSHException):
    pass


class SSHCommandException(SSHException):
    pass


class SSHSession(object):
    """
    Generic SSHSession which can be used to run commands
    """
    def __init__(self, hostname, username, password, timeout=60):
        """
        Establish SSH Connection using given hostname, username and
        password which can be used to run commands.
        """
        self.hostname = hostname

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.ssh.connect(hostname=hostname, username=username, password=password, timeout=60, look_for_keys=False)
        except paramiko.BadHostKeyException:
            raise SSHConnectionException('SSH Server host key could not be verified')
        except paramiko.AuthenticationException:
            raise SSHConnectionException('SSH Authentication failed')
        except paramiko.SSHException:
            raise SSHConnectionException('Paramiko SSH Connection Problem')
        except Exception, e:
            raise SSHConnectionException('SSH Connection Error:%s ' % e)

    def __repr__(self):
        """
        Return a representation string
        """
        return "<%s (%s)>" % (self.__class__.__name__, self.hostname)

    def __del__(self):
        """Try to close connection if possible"""
        try:
            sleep(2)
            self.ssh.close()
        except Exception:
            pass

    def command(self, command):
        """
        Runs given command and returns output, error.

        This is the method you are after if none of the above fulfill your needs either to add more functionality or
        customize. You can run any command using SSH session established and parse the output the way you like.

        Example:
        def myfunc(ssh_session):
            output, error = ssh_session.command('date')
            return "".join(output).strip()
        """
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.readlines()
            error = stdout.readlines()
            return output, error
        except Exception, e:
            raise SSHCommandException('Unable to run given command %s. Error %s' % (command,e) )