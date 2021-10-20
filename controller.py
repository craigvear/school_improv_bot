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

        # # instantiate kyma comms
        # if self.kyma:
        #     self.IP = "192.168.1.136" # IP address of Kyma machine
        #     self.PORT = 8000
        #
        #     self.kyma_client = SimpleUDPClient(self.IP, self.PORT)  # Create client

        # or use Alfie sax sample
        # else:
        #     self.audio_file_sax = AudioSegment.from_mp3('media/alfie.mp3')
        #     # self.audio_file_bass = AudioSegment.from_mp3('media/bass.mp3') + 4
        #
        #     # robot instrument vars
        #     # globs for sax
        #     self.pan_law_sax = -0.5
        #     self.audio_file_len_ms_sax = self.audio_file_sax.duration_seconds * 1000
        #
        #     # # globs for bass
        #     # self.pan_law_bass = 0
        #     # self.audio_file_len_ms_bass = self.audio_file_bass.duration_seconds * 1000

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
            data = np.frombuffer(self.stream.read(self.CHUNK,exception_on_overflow = False),
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

    def robot_sax(self):
        # make a serial port connection here
        print('im here SAX - sleeping for 3')
        # sleep(3)

    # then start improvisers
        while True:
            print('im here4')
            # grab raw data from engine stream
            raw_data_from_dict = self.got_dict['master_output']
            rhythm_rate = self.got_dict['rhythm_rate']
            print('data = ', raw_data_from_dict, rhythm_rate)

            # add variability to the individual instrument
            # rnd_dur_delta = random()
            # rhythm_rate *= rnd_dur_delta * 8
            # print('sax', raw_data_from_dict, rhythm_rate)

            # make a sound & move bot
            self.make_sound(raw_data_from_dict, rhythm_rate)
            print('making a new one')

    # # left this in just in case - will need to get bass audio file
    # def robot_bass(self):
    #     # make a serial port connection here
    #     # print('im here Bass - sleeping for 3')
    #     sleep(3)
    #
    # # then start improvisers
    #     while True:
    #         print('im here4')
    #         # grab raw data from engine stream
    #         raw_data_from_dict = self.got_dict['master_output']
    #
    #         # trying different part of the dict
    #         # raw_data_from_dict = self.got_dict['move_rnn']
    #
    #         rhythm_rate = self.got_dict['rhythm_rate']
    #         print('bass', raw_data_from_dict, rhythm_rate)
    #
    #         # add variability to the individual instrument
    #         rnd_dur_delta = random() * 4
    #         rhythm_rate *= rnd_dur_delta
    #         print('bass', raw_data_from_dict, rhythm_rate)
    #
    #         # make a sound & move bot
    #         self.make_sound('bass', raw_data_from_dict, rhythm_rate)
    #         print('making a new one')

    def make_sound(self, incoming_raw_data, rhythm_rate):
        # # temp random num gen
        # rnd = randrange(self.audio_dir_len)
        # print(self.audio_dir[rnd])
        print('making sound')

        # make some duration decisions
        len_delta = random() * 1000
        duration = rhythm_rate * len_delta

        # if duration > 0.1:
        #
        # if self.kyma:
        #     # scale incoming data to OSC range
        #     # kyma_data = incoming_raw_data  #int(((incoming_raw_data - 0) / (1 - 0)) * (128 - 0) + 0)
        #
        #     # parse got disct to Kyma VCS widgets (flotas 0.0-1.0)
        #     amp1 = self.got_dict['move_rnn']
        #     amp2 = self.got_dict['affect_rnn']
        #     density = self.got_dict['move_affect_conv2']
        #     grainDur = self.got_dict['affect_move_conv2']
        #     grainDurJitter =self.got_dict['master_output']
        #     loopEnd = self.got_dict['rhythm_rnn']
        #     loopStart = self.got_dict['rhythm_rate']
        #     panJitter = self.got_dict['affect_net']
        #     rate = self.got_dict['rhythm_rate']
        #     scaleFreq = self.got_dict['move_rnn']
        #     timeJitter = self.got_dict['self_awareness']
        #
        #     print(f'Kyma data send ===================   ', amp1, amp2, density, grainDur, grainDurJitter, loopEnd,
        #            loopStart, panJitter, scaleFreq, timeJitter)
        #     try:
        #         # send an OSC command to Kyma to make a sound
        #         self.kyma_client.send_message("/vcs/Amp1/1", amp1)  # Send float message
        #         self.kyma_client.send_message("/vcs/Amp2/1", amp2)  # Send float message
        #         self.kyma_client.send_message("/vcs/Density/1", density)  # Send float message
        #         self.kyma_client.send_message("/vcs/GrainDur/1", grainDur)  # Send float message
        #         self.kyma_client.send_message("/vcs/GrainDurJitter/1", grainDurJitter)  # Send float message
        #         self.kyma_client.send_message("/vcs/loopEnd/1", loopEnd)  # Send float message
        #         self.kyma_client.send_message("/vcs/LoopStart/1", loopStart)  # Send float message
        #         self.kyma_client.send_message("/vcs/PanJitter/1", panJitter)  # Send float message
        #         self.kyma_client.send_message("/vcs/Rate/1", rate)  # Send float message
        #         self.kyma_client.send_message("/vcs/ScaleFreq/1", scaleFreq)  # Send float message
        #         self.kyma_client.send_message("/vcs/TimeJitter/1", timeJitter)  # Send float message
        #     except:
        #         print('////////////         error in OSC building,  '
        #               'ValueError: Infered arg_value type is not supported')

        # move bot before making sound
        if self.robot_connected:
            self.move_robot(incoming_raw_data, duration)
        else:
            if duration > 1:
                self.piano.which_note(incoming_raw_data)
                print('play')
            sleep(duration/1000) # sleep while Kyma makes a sound (in ms) - now son


        # else:
        #     if instrument == 'sax':
        #         audio_file = self.audio_file_sax
        #         audio_file_len_ms = self.audio_file_len_ms_sax
        #         pan_law = self.pan_law_sax
        #
        #     # elif instrument == 'bass':
        #     #     audio_file = self.audio_file_bass
        #     #     audio_file_len_ms = self.audio_file_len_ms_bass
        #     #     pan_law = self.pan_law_bass
        #
        #     # rescale incoming raw data
        #     audio_play_position = int(((incoming_raw_data - 0) / (1 - 0)) * (audio_file_len_ms - 0) + 0)
        #     if duration < 0.1:
        #         duration = 0.1
        #     end_point = audio_play_position + duration
        #     print(audio_play_position, end_point, duration)
        #
        #     # make a sound from incoming data
        #     snippet = audio_file[audio_play_position: end_point]
        #     print('snippet')






        # # pan snippet
        # pan_snippet = snippet.pan(pan_law)
        # print('pan')

        # # move bot before making sound
        # if self.robot_connected:
        #     # if instrument == 'sax':
        #     self.move_robot(incoming_raw_data, duration)

        # get the robot to move with
        # play(pan_snippet)


            # sleep(duration/ 1000)
        print('fininshed a play')

    def move_robot(self, incoming_data, duration):

        # which movement: fwd, back, left, right
        if duration > 0.2:
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

        # sleep fpr duration then send a stop command
        sleep(duration/1000)
        self.robot_robot.stop()