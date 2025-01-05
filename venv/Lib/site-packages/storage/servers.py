import os
import re
from ssh import SSHSession

class LinuxServer(SSHSession):
    """
    Establish SSH Connection to Linux Server which can be used
    to run commands against it
    """
    def get_hostname(self):
        """
        Returns Server Hostname
        """
        output, error = self.command('hostname')
        hostname = " ".join(output).strip()
        return hostname

    def has_hbas(self):
        """
        Return True if Server has HBA's, otherwise NO
        """
        output, error = self.command('/sbin/lspci | grep -i fibre')
        if output:
            return True
        else:
            return False

    def get_hba_manufacturer(self):
        """
        Returns HBA Manufacturer
        """
        manufacturer = None
        if self.has_hbas():
            output, error = self.command('/sbin/lspci | grep -i fibre')
            if re.search("Brocade", " ".join(output), re.IGNORECASE) and not re.search("QLogic|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "Brocade"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|Emulex", " ".join(output), re.IGNORECASE):
                manufacturer = "QLogic"
            elif re.search("QLogic", " ".join(output), re.IGNORECASE) and not re.search("Brocade|QLogic", " ".join(output), re.IGNORECASE):
                manufacturer = "Emulex"
            else:
                manufacturer = "Unknown"
        return manufacturer

class RedhatServer(LinuxServer):

    def get_os_version(self):
        """
        Returns OS Version
        """
        output, error = self.command('cat /etc/redhat-release')
        return " ".join(output).strip()

    def get_packages(self, package):
        """
        Return Installed Packages
        package can be actual package or pattern
        """
        packages = []
        output, error = self.command('rpm -qa %s' % package)

        if output and not re.search('is not installed', " ".join(output)):
            for entry in output:
                packages.append(entry.strip())
        return packages

    def get_wwpns(self):
        """
        Returns a list with WWPN's
        """
        wwpns = []
        if self.get_hba_manufacturer():
            output, error = self.command('cat /sys/class/fc_host/host*/port_name')
            if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                for item in output:
                    item = item.strip()
                    if re.match("0x", item) and len(item) == 18:
                        wwpns.append(":".join(re.findall('..', item.strip('0x'))))
                    else:
                        pass
        return wwpns

    def check_hba_driver(self):
        """
        Returns True if bcu or scli is installed for respective HBA,
        if not False.

        Currently all it checks is if bcu and scli commands are
        available or not. Does not really check if HBA driver is installed successfully.
        """
        output, error = ([], [])

        manufacturer = self.get_hba_manufacturer()
        fc_hosts = self.command('cat /sys/class/fc_host/host*/port_name')[0]
        search = re.search('No such file or directory', " ".join(fc_hosts), re.IGNORECASE)

        if manufacturer == "Brocade" and not search:
            output, error = self.command('bcu -v')
        elif manufacturer == "QLogic" and not search:
            output, error = self.command('scli -v')
        if output:
            return True
        else:
            return False


    def get_bcu_version(self):
        output, error = self.command('bcu -v')
        if output:
            version = re.search('Version:(.+?)', " ".join(output) , re.I)
            if version:
                return version.group(1)
            else:
                return "Not Available"
        else:
            return "bcu may not be installed"

    def get_scli_version(self):
        pass


class ESXServer(LinuxServer):
    def get_os_version(self):
        """
        Returns OS Version
        """
        command = "head -1 /proc/vmware/version | awk '{split($0,array,\",\")} END{print array[1]}'"
        output, error = self.command(command)
        return " ".join(output).strip()

    def get_wwpns(self):
        """
        Returns a list with WWPN's
        """
        wwpns = []
        manufacturer = self.get_hba_manufacturer()
        if manufacturer:
            if manufacturer == "Brocade":
                output, error = self.command('cat /proc/scsi/bfa/* | grep WWPN')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match("WWPN: ", item) and len(item) == 29:
                            wwpns.append(item.strip("WWPN: "))
            elif manufacturer == "QLogic":
                output, error = self.command('cat /proc/scsi/qla2xxx/* | grep adapter-port')
                if output and not re.search('No such file or directory', " ".join(output), re.IGNORECASE):
                    for item in output:
                        item = item.strip()
                        if re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item):
                            wwpn = re.match('scsi-qla.+-adapter-port=[A-Fa-f0-9]{16}:', item).group().split('=')[
                                   1].strip(':')
                            wwpns.append(":".join(re.findall('..', wwpn)))

        return wwpns