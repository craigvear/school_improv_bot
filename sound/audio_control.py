"""main sound script
controls microphone stream"""


# get python libraries
import pyaudio
import numpy as np
import math
# from sound.audio_data import LiveAudioData
from threading import Thread
from random import random
import logging

#  import local methods
from nantucket.hivemind import DataBorg


class AudioEngine:
    """controls audio listening"""
    def __init__(self): #, ai_engine):
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
        # self.send_data_dict = {'mic_level': 0,
        #                        'speed': 1,
        #                        'tempo': 0.1,
        #                        'freq': 0,
        #                        'midinote': ("z", 0)
        #                        }

        # self.send_data_dict = LiveAudioData()

        # plug into the hive mind data borg
        self.hivemind = DataBorg()

        self.notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        # own the AI data server
        # self.engine = ai_engine

        # t3 = Thread(target=self.snd_listen)
        # t3.start()

    def snd_listen(self):
        logging.info("mic listener: started!")
        while self.running:
            data = np.frombuffer(self.stream.read(self.CHUNK,
                                                  exception_on_overflow = False),
                                 dtype=np.int16)
            peak = np.average(np.abs(data)) * 2
            if peak > 1000:
                bars = "#" * int(50 * peak / 2 ** 16)

                # Calculates the frequency from with the peak ws
                data = data * np.hanning(len(data))
                fft = abs(np.fft.fft(data).real)
                fft = fft[:int(len(fft) / 2)]
                freq = np.fft.fftfreq(self.CHUNK, 1.0 / self.RATE)
                freq = freq[:int(len(freq) / 2)]
                freqPeak = freq[np.where(fft == np.max(fft))[0][0]] + 1

                # get midinote from freqPeak
                midinote = self.freq_to_note(freqPeak)

                # Shows the peak frequency and the bars for the amplitude
                logging.debug(f"peak frequency: {freqPeak} Hz, mididnote {midinote}:\t {bars}")

                self.hivemind.mic_in = peak # / 30000
                self.hivemind.freq = freqPeak
                self.hivemind.midinote = midinote
                # self.engine.parse_got_dict(self.send_data_dict)

                # normalise it for range 0.0 - 1.0
                normalised_peak = ((peak - 0) / (20000 - 0)) * (1 - 0) + 0
                if normalised_peak > 1.0:
                    normalised_peak = 1.0

                # put normalised amplitude into Nebula's dictionary for use
                self.hivemind.mic_in = normalised_peak

                # if loud sound then 63% affect gesture manager
                if normalised_peak > 0.8:
                    if random() > 0.36:
                        self.hivemind.interrupt_bang = False
                        self.hivemind.randomiser()
                        logging.info("-----------------------------INTERRUPT----------------------------")

    def freq_to_note(self, freq):
        # formula taken from https://en.wikipedia.org/wiki/Piano_key_frequencies
        note_number = 12 * math.log2(freq / 440) + 49
        note_number = round(note_number)

        note = (note_number - 1) % len(self.notes)
        note = self.notes[note]

        octave = (note_number + 8) // len(self.notes)

        return note, octave

    def terminate(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


