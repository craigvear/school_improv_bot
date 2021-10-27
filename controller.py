"""main client script
controls microphone stream"""


# get python libraries
import pyaudio
import numpy as np


class Client:
    """controls listening plate and robot comms"""
    def __init__(self, ai_engine):
        self.running = True
        self.connected = False
        self.logging = False

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

        # own the AI data server
        self.engine = ai_engine
        #
        # # init got dict
        # self.got_dict = self.engine.datadict

    def snd_listen(self):
        print("mic listener: started!")
        while True:
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow = False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 2000:
                bars = "#" * int(50 * peak / 2 ** 16)
                print("%05d %s" % (peak, bars))
            self.send_data_dict['mic_level'] = peak # / 30000
            self.engine.parse_got_dict(self.send_data_dict)

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
