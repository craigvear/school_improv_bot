# -*- coding: utf-8 -*-
"""

"""



# import pygame
# from pygame.locals import *
# from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth
from time import sleep, time
from random import random, randrange, getrandbits, shuffle
import platform
from operator import itemgetter
from threading import Thread, Timer

PLATFORM = platform.machine()

class Piano:
    def __init__(self, harmony_signal):

        self.harmony_signal = harmony_signal
        SF2 = "media/soundfontGM.sf2"
        self.OCTAVES = 5  # number of octaves to show
        self.LOWEST = 2  # lowest octave to show
        self.FADEOUT = 0.25  # coloration fadeout time (1 tick = 0.001)

        # list the notes in the master key of C Maj;
        # including the "add whole tone" to 1, 3, 5 of each chord tones
        # giving us lydian #11 and tritone/ dom #13 5th last
        self.note_list = ["A", "B", "C", "D", "E", "F", "G", "A", "F#", "C#"]

        # set up harmonic matrix with weighting adding to 100%
        self.dmin7 = [(3, 20), (5, 40), (0, 10), (2, 30)]
        self.g9 = [(6, 15), (1, 35), (3, 5), (5, 20), (0, 25)]
        self.cM7 = [(2, 20), (4, 40), (6, 10), (1, 30)]

        # set up the lydian + whole step extention to chordal tone
        self.dmin7_lyd = [(4, 34), (6, 33), (1, 33)]
        self.g9_lyd = [(7, 34), (9, 33), (3, 33)]
        self.cM7_lyd = [(5, 34), (8, 33), (0, 33)]

        self.octave = 4
        self.channel = 1

        # start fluidsynth
        if PLATFORM == "x86_64":
            fluidsynth.init(SF2)
        else:
            fluidsynth.init(SF2, "alsa")

        # start of a played not queue to
        self.played_note = 0

        # state BPM
        bpm = 120

        # find the ms wait for triplets
        self.tick = (((60 / bpm) * 1000) / 3)

        # init the harmony dictionary for emission to GUI
        self.harmony_dict = {"BPM": bpm,
                             "chord": "none",
                             "note": "none",
                             "beat": 0}

        # start a thread to wait for commands to write
        self.incoming_note_queue = []
        self.played_note_queue = []

        # # start the thread
        # self.update_player()

        self.playingThread = None
        self.update_player()

    def update_player(self):
        # print("-------- updating queues")
        self.parse_queues()

        # gather and send details to the harmony signal emitter
        self.fill_harmony_dict()

        playingThread = Timer(self.tick/ 1000, self.update_player)
        playingThread.start()

    def parse_queues(self):
        # this func spins around controlling the 2 note queues
        # print("1")
        # print('incoming note queue', self.incoming_note_queue)
        if len(self.incoming_note_queue):
            for i, event in enumerate(self.incoming_note_queue):
                note_name, octave = itemgetter("note_name",
                                               "octave")(event)

                # play note
                self.play_note(Note(note_name, octave))

                # delete from incoming queue
                del self.incoming_note_queue[i]

                # add to played list
                self.played_note_queue.append(event)


        if len(self.played_note_queue):
            for i, event in enumerate(self.played_note_queue):
                lifespan, note_name, octave = itemgetter("endtime",
                                                        "note_name",
                                                        "octave")(event)

                # if lifespan (endtime) is less than current time
                if lifespan <= time():
                    # stop note
                    self.stop_note(Note(note_name, octave))

                    # delete from played queue
                    del self.played_note_queue[i]

    def fill_harmony_dict(self):
        # self.harmony_dict =

        self.harmony_signal.harmony_str.emit(str(self.harmony_dict))
        # print('//////////////////                   EMITTING and making sound')

    def play_note(self, note_to_play):
        """play_note determines the coordinates of a note on the keyboard image
        and sends a request to play the note to the fluidsynth server"""

        dynamic = 90 + randrange(1, 30)
        fluidsynth.play_Note(note_to_play, self.channel, dynamic)

    def stop_note(self, note_to_stop):
        fluidsynth.stop_Note(note_to_stop, self.channel)

    def which_note(self, incoming_data, rhythm_rate):
        """receives raw data from robot controller and converts into piano note"""

        # turn previous note off
        # fluidsynth.stop_Note(note=self.played_note)

        # todo - sort out 2-5-1 changes over a specified tempo
        # which chord
        # BPM = 60

        now_time = int(time())
        bar = now_time % 4
        print(f'\t\t\t\t BAR = {bar}')

        # which chord & is it root or lyd
        # normal chord notes or jazz/ lyd notes
        if getrandbits(1) == 1:
            if bar == 0:
                chord = self.dmin7
                self.harmony_dict['chord'] = "Dmin7"
            elif bar == 1:
                chord = self.g9
                self.harmony_dict['chord'] = "G9"
            else:
                chord = self.cM7
                self.harmony_dict['chord'] = "Cmaj7"

        else:
            if bar == 0:
                chord = self.dmin7_lyd
                self.harmony_dict['chord'] = "Dmin7 lydian"
            elif bar == 1:
                chord = self.g9_lyd
                self.harmony_dict['chord'] = "G9 lydian"
            else:
                chord = self.cM7_lyd
                self.harmony_dict['chord'] = "Cmaj7 lydian"

        # shufle chord seq --- too much random???
        shuffle(chord)

        # # which note
        # len_of_chord = len(chord)
        # which_note = randrange(len_of_chord)
        # this_note, this_weight = chord[which_note]
        # print(this_note, this_weight)

        # rough random for weighting
        which_weight = random() * 100

        # which octave? Drunk walk
        drunk_octave = randrange(4)

        # drunk move down octave
        if drunk_octave == 0:
            self.octave -= 1

        # drunk move up an octave
        elif drunk_octave == 1:
            self.octave += 1

        # drunk reset to octave 4
        elif drunk_octave == 3:
            self.octave = 4

        # check its in range
        if self.octave < 0:
            self.octave = 2
        elif self.octave > self.OCTAVES:
            self.octave = 4

        # get note and play
        current_sum = 0
        for note_pos, weight in chord:
            note_name = self.note_list[note_pos]
            # print(f'original note name = {self.note_list[note_pos]}; '
            #       f'adjusted note name = {note_name}, weight = {weight}')

            # which note depending on weighting
            current_sum += weight
            if current_sum > which_weight:
                print('playing', note_name)
                self.harmony_dict['note'] = note_name

                note_to_play = dict(note_name=note_name,
                                    octave=self.octave,
                                    endtime=time() + (rhythm_rate))

                # print (f'current time = {time()},  note data =   {note_to_play}')
                # add note, octave, duration (from visual processing)
                self.incoming_note_queue.append(note_to_play)
                # self.play_note(Note(note_name, self.octave))
                # self.played_note = note_name
                break


if __name__ == "__main__":
    piano = Piano()
    for x in range(10):
        piano.which_note(x, random())
        sleep(1)
