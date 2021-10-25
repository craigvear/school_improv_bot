import argparse
import time
from ast import literal_eval

from pythonosc import udp_client

from HostnameIp import HostnameIp

if __name__ == "__main__":

    hostname_ip = HostnameIp()
    host_ip = hostname_ip.get_ip()

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="192.168.1.93",
                        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
                        help="The port the OSC server is listening on")
    args = parser.parse_args()

    client = udp_client.SimpleUDPClient(args.ip, args.port)

    with open('data_file.txt', 'r') as fp:
        for cnt, line in enumerate(fp):
            print("Line {}: {}".format(cnt, line))
            line_dict = literal_eval(line)
            try:
                client.send_message("/axisA/", line_dict['axisa'])
                client.send_message("/axisB/", line_dict['axisb'])
                client.send_message("/mlX/", line_dict['mlx'])
                client.send_message("/mlY/", line_dict['mly'])
                client.send_message("/mlz/", line_dict['mlz'])
                client.send_message("/kinX/", line_dict['kinx'])
                client.send_message("/kinZ/", line_dict['kinz'])
            except KeyError as err:
                print("Key not yet defined: {}".format(err))
            time.sleep(0.5)
