from random import randrange
import pyaudio
import numpy as np
from random import random
from time import sleep
from pydub import AudioSegment
from pydub.playback import play
from pythonosc.udp_client import SimpleUDPClient
from jetbot.robot import Robot
from piano import Piano

"""main client script
controls microphone stream and organise all audio responses
and move the Jetbot"""


class Client:
    def __init__(self, ai_engine):
        self.running = True
        self.connected = False
        self.logging = False
        # self.kyma = True

        # is the robot connected
        self.robot_connected = False
        self.direction = 1
        self.speed_factor = 0.3

        # instantiate robot
        if self.robot_connected:
            self.robot_robot = Robot()

        # instanstiate piano player class
        self.piano = Piano()

        # set up mic listening func
        self.CHUNK = 2 ** 11
        self.RATE = 44100
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)

        # build send data dict
        self.send_data_dict = {'mic_level': 0,
                               'speed': 1,
                               'tempo': 0.1
                               }

        # init got dict
        self.got_dict = {}

        # # instantiate the server
        self.engine = ai_engine

    def snd_listen(self):
        print("mic listener: started!")
        while True:
            data = np.frombuffer(self.stream.read(self.CHUNK, exception_on_overflow = False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 2000:
                bars = "#" * int(50 * peak / 2 ** 16)
                print("%05d %s" % (peak, bars))
            self.send_data_dict['mic_level'] = peak / 30000

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def data_exchange(self):
        print("data exchange: started!")
        while True:
            # send self.send_data_dict
            self.engine.parse_got_dict(self.send_data_dict)

            # get self.datadict from engine
            self.got_dict = self.engine.datadict

            # sync with engine & stop freewheeling
            sleep_dur = self.got_dict['rhythm_rate']
            # print('data exchange')
            sleep(sleep_dur)

    def sound_bot(self):
        # make a serial port connection here
        print('im here sound bot - sleeping for 3')
        # sleep(3)

    # then start improvisers
        while True:
            print('im here4')
            # grab raw data from engine stream
            raw_data_from_dict = self.got_dict['master_output']
            rhythm_rate = self.got_dict['rhythm_rate']
            print('data = ', raw_data_from_dict, rhythm_rate)

            # make a sound & move bot
            self.make_sound(raw_data_from_dict, rhythm_rate)
            print('making a new one')


    def make_sound(self, incoming_raw_data, rhythm_rate):
        # # temp random num gen
        # rnd = randrange(self.audio_dir_len)
        # print(self.audio_dir[rnd])
        print('making sound')

        # make some duration decisions
        # todo this needs fixing - it should some form a variability
        #  so its not totally dependent on nets prediction
        len_delta = random() * 1000
        duration = rhythm_rate * len_delta

        print('duration = ', duration)

        # making sound
        # if duration > 10: # todo this is problamatoic
        self.piano.which_note(incoming_raw_data)
        print('play')

        # move bot
        if self.robot_connected:
            self.move_robot(incoming_raw_data, duration)
        else:
            sleep(duration/100) # todo this should be / 1000 but duration is glitchy

        print('fininshed a play')

    def move_robot(self, incoming_data, duration):
        # which movement: fwd, back, left, right
        if duration > 0.2: # todo this is problamatoic
            # define movement
            rnd_move = randrange(4)

            rnd_speed = randrange(1, 5)
            rnd_speed = rnd_speed * self.speed_factor # int(rnd_speed * self.speed_factor)

            # move an arm joint
            if rnd_move == 0:
                self.robot_robot.forward(rnd_speed)

            elif rnd_move == 1:
                self.robot_robot.backward(rnd_speed)

            elif rnd_move == 2:
                self.robot_robot.left(rnd_speed)

            elif rnd_move == 3:
                self.robot_robot.right(rnd_speed)

        # sleep for duration then send a stop command
        sleep(duration/100)
        self.robot_robot.stop()
