import socket


class HostnameIp:
    def __init__(self):
        try:
            self.host_name = socket.gethostname()
            self.host_ip = socket.gethostbyname(self.host_name)
            print("Hostname: ", self.host_name)
            print("IP: ", self.host_ip)
        except Exception as e:
            print("Unable to get Hostname & IP. Error {}".format(e))

    def get_ip(self):
        return self.host_ip
