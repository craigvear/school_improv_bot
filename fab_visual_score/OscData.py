import argparse
import threading
import platform

from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher

from HostnameIp import HostnameIp

PLATFORM = platform.machine()

if "arm" in PLATFORM:
    from easygopigo3 import EasyGoPiGo3

# axisA = -255 and 255
# axisB = -255 and 255
# all the others between 0 and 1 (float)

SAVE_TO_FILE = False
MAXIMUM_SPEED = 1000

MIN_FROM_MAX = -500
MAX_FROM_MAX = 650


class OscData():
    def __init__(self, osc_signal_obj):
        self.osc_signal = osc_signal_obj

        hostname_ip = HostnameIp()
        host_ip = hostname_ip.get_ip()

        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default="192.168.1.93", help="The ip to listen on")
        parser.add_argument("--port", type=int, default=8000, help="The port to listen on")
        args = parser.parse_args()

        if "arm" in PLATFORM:
            self.gpg = EasyGoPiGo3()
            self.gpg.set_speed(MAXIMUM_SPEED)

        self.final_data = {}
        self.data_file = open("data_file.txt", "a+")

        self.dispatcher = Dispatcher()
        self.dispatcher.map("/axisA/", self.axisa, "axisa")
        self.dispatcher.map("/axisB/", self.axisb, "axisb")
        self.dispatcher.map("/mlX/", self.mlx, "mlx")
        self.dispatcher.map("/mlY/", self.mly, "mly")
        self.dispatcher.map("/mlZ/", self.mlz, "mlz")
        self.dispatcher.map("/kinX/", self.kinx, "kinx")
        self.dispatcher.map("/kinY/", self.kiny, "kiny")
        self.dispatcher.map("/kinZ/", self.kinz, "kinz")
        self.dispatcher.map("/filter/", self.filter, "filter")
        if "arm" in PLATFORM:
            self.dispatcher.map("/left/", self.left, "left")
            self.dispatcher.map("/right/", self.right, "right")

        server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), self.dispatcher)
        print("Serving on {}".format(server.server_address))

        _serve = server.serve_forever
        server_thread = threading.Thread(target=_serve)
        server_thread.daemon = True
        server_thread.start()

    def filter(self, unused_addr, args, msg):
        self.osc_signal.osc_str.emit(str(msg))

    def motor_power(self, value):
        return (((int(value) - MIN_FROM_MAX) * (100 - -100)) / (MAX_FROM_MAX - MIN_FROM_MAX)) + -100

    def left(self, unused_addr, args, msg):
        self.gpg.set_motor_power(self.gpg.MOTOR_LEFT, self.motor_power(msg))

    def right(self, unused_addr, args, msg):
        self.gpg.set_motor_power(self.gpg.MOTOR_RIGHT, self.motor_power(msg))

    def axisa(self, unused_addr, args, msg):
        self.final_data['axisa'] = msg

    def axisb(self, unused_addr, args, msg):
        self.final_data['axisb'] = msg

        if "arm" in PLATFORM:
            self.gpg.set_motor_power(self.gpg.MOTOR_RIGHT, self.motor_power(msg))

    def mlx(self, unused_addr, args, msg):
        self.final_data['mlx'] = msg

    def mly(self, unused_addr, args, msg):
        self.final_data['mly'] = msg

    def mlz(self, unused_addr, args, msg):
        self.final_data['mlz'] = msg

    def kinx(self, unused_addr, args, msg):
        self.final_data['kinx'] = msg

    def kiny(self, unused_addr, args, msg):
        self.final_data['kiny'] = msg

    def kinz(self, unused_addr, args, msg):
        self.final_data['kinz'] = msg
        if SAVE_TO_FILE:
            self.data_file.write(str(self.final_data) + "\n")
        self.osc_signal.osc_str.emit(str(self.final_data))
