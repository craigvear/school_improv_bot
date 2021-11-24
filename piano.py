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
        self.LOWEST = 3  # lowest octave to show


        ##############################################################
        # old matrix here
        ##############################################################

        # list the notes in the master key of C Maj;
        # including the "add whole tone" to 1, 3, 5 of each chord tones
        # giving us lydian #11 and tritone/ dom #13 5th last
        # self.note_list = ["A", "B", "C", "D", "E", "F", "G", "A", "F#", "C#"]

        # set up harmonic matrix with weighting adding to 100%
        # offset by starting tonic of master key

        # # minor 7th = ii in the 2-5-1
        # self.min7 = [(0, 20), (3, 40), (7, 10), (10, 30)]  # 1, 3, 5, 7 of minor scale
        # self.min7_sharp11_13 = [(0, 15), (3, 20), (7, 5), (10, 15), (2, 15), (5, 20), (9, 10)]  # 1, 3, 5, 7, 9, #11, 13 of minor scale
        #
        # # major dom 9th - V in the 2-5-1
        # self.dom9 = [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)] # flat 7
        # self.dom9_sharp11_13 = [(0, 15), (4, 20), (7, 5), (10, 15), (2, 15), (5, 20), (9, 10)]
        #
        # # major dom 9th - V in the 2-5-1
        # self.maj7 = [(0, 20), (4, 40), (7, 10), (11, 30)]
        # self.maj7_sharp11_13 = [(0, 15), (4, 20), (7, 5), (11, 15), (2, 15), (5, 20), (9, 10)]
        #
        # # set up harmonic matrix with weighting adding to 100%
        # self.dmin7 = [(3, 20), (5, 40), (0, 10), (2, 30)]
        # self.g9 = [(6, 15), (1, 35), (3, 5), (5, 20), (0, 25)]
        # self.cM7 = [(2, 20), (4, 40), (6, 10), (1, 30)]
        #
        # # set up the lydian + whole step extention to chordal tone
        # self.dmin7_lyd = [(4, 34), (6, 33), (1, 33)]
        # self.g9_lyd = [(7, 34), (9, 33), (3, 33)]
        # self.cM7_lyd = [(5, 34), (8, 33), (0, 33)]

        ##############################################################
        # new matrix here
        ##############################################################

        # alt method using full 12 note alphabet: 0 - 11
        self.note_alphabet = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]

        # chord types are 1: tonic Maj7; 2: minor 7th; 4: sub dom maj7; 5: dom 7th etc
        self.major_key_chord_shapes = {"1": [(0, 20), (4, 40), (7, 10), (11, 30)],
                             "3": [(0, 20), (3, 40), (7, 10), (10, 30)],
                             "2": [(0, 20), (3, 40), (7, 10), (10, 30)],
                             "5": [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)],
                             "6": [(0, 20), (3, 40), (7, 10), (10, 30)]
                                       }

        # same as above but with lyd + whole tone extensions to core triad chord tones
        # e.g. 9th, #11, 13
        self.lyd_chord_shapes = {"1": [(0, 15), (4, 20), (7, 5), (11, 15),
                                       (2, 15), (6, 20), (9, 10)],
                                 "2": [(0, 15), (3, 20), (7, 5), (10, 15),
                                       (2, 15), (5, 20), (9, 10)],
                                 "3": [(0, 15), (3, 20), (7, 5), (10, 15),
                                       (2, 15), (5, 20), (9, 10)],
                                 "5": [(0, 15), (4, 20), (7, 5), (10, 15),
                                       (2, 15), (5, 20), (9, 10)],
                                 "6": [(0, 15), (3, 20), (7, 5), (10, 15),
                                       (2, 15), (5, 20), (9, 10)]
                                 }

        # list the name and note alphabet position for each progression
        progression2511 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")]
        progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
        progression3625 = [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]

        # which progression
        self.progression = progression3625

        self.master_key = 3  # which is C on the note alphabet

        # piano range vars
        self.octave = 4
        self.channel = 1

        # chronos vars
        self.bass_octave = 1
        self._last_bar = None

        # start fluidsynth
        if PLATFORM == "x86_64":
            fluidsynth.init(SF2)
        else:
            fluidsynth.init(SF2, "alsa")

        # start of a played not queue to
        self.played_note = 0

        # % factor if a note event is played or not
        self.note_played_or_not = 0.5

        # state BPM
        bpm = 120
        self.time_sig = 4

        # state how many sub divides to a beat. 4=16ths, 12 = semi trips
        self.subdivision = 12

        # which turnaround
        turnaround_bar_length = 4
        self.turnaround = turnaround_bar_length

        # consts for the counting process
        self.bar = 1
        self.beat = 1
        self.tick = 0

        # convert bar and beat to ms
        bpm_to_ms = ((60 / bpm) * 1000)

        # find the ms wait for subdivide
        self.sleep_dur = (bpm_to_ms / self.subdivision) / 1000

        # init the harmony dictionary for emission to GUI
        self.harmony_dict = {"BPM": bpm,
                             "chord": "none",
                             "note": "none",
                             "bar": "none"}

        # start a thread to wait for commands to write
        self.incoming_note_queue = []
        self.played_note_queue = []

        # Play a root bass note at beginning of each bar?
        self.bass_line = True

        self.playingThread = None
        self.update_player()

    def update_player(self):
        # print("-------- updating queues")
        self.parse_queues()

        # gather and send details to the harmony signal emitter
        self.fill_harmony_dict()

        # calc bar and beat & play root in LH
        self.chronos()

        # Update the piano playback system 12 times a beat (covers semi's and trips)
        playingThread = Timer(self.sleep_dur, self.update_player)
        playingThread.start()

    def chronos(self):
        """coordinate the master tempo and behaviours
        using BPM and root notes in bass LH"""
        # get bar
        current_bar = self.calc_bar()
        current_bar = current_bar % self.turnaround

        # calc root of current sequence & play
        # on bar change
        if current_bar != self._last_bar:
            if current_bar == 0:
                root_note_name = "D"
            elif current_bar == 1:
                root_note_name = "G"
            else:
                root_note_name = "C"

            # play the root
            # self.play_note(Note(root_note_name, self.bass_octave))
            bass = dict(note_name=root_note_name,
                        octave=self.bass_octave,
                        endtime=time() + 1,
                        dynamic=40)

            # print (f'current time = {time()},  note data =   {note_to_play}')
            # add note, octave, duration (from visual processing)
            if self.bass_line:
                self.incoming_note_queue.append(bass)

        self._last_bar = current_bar

    def calc_bar(self):
        self.tick += 1
        # print(f'doin stuff - BAR BEAT TICK {self.bar}, {self.beat}, {self.tick}')

        if self.tick >= self.subdivision:
            self.beat += 1
            self.tick = 0

        if self.beat > self.time_sig:
            self.bar += 1
            self.beat = 1

        self.harmony_dict['bar'] = self.bar
        return self.bar

    def parse_queues(self):
        # this func spins around controlling the 2 note queues
        # print("1")
        # print('incoming note queue', self.incoming_note_queue)
        if len(self.incoming_note_queue):
            for i, event in enumerate(self.incoming_note_queue):
                note_name, octave, dynamic = itemgetter("note_name",
                                                        "octave",
                                                        "dynamic")(event)

                # play note
                self.play_note(Note(note_name, octave), dynamic)

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

        self.harmony_signal.harmony_str.emit(self.harmony_dict)
        # print('//////////////////                   EMITTING and making sound')

    def play_note(self, note_to_play, dynamic):
        """play_note determines the coordinates of a note on the keyboard image
        and sends a request to play the note to the fluidsynth server"""

        # dynamic = 90 + randrange(1, 30)
        fluidsynth.play_Note(note=note_to_play, channel=self.channel, velocity=dynamic)
        print(f'\t\t\t\t\tplaying {note_to_play}, channel {self.channel}, velocity {dynamic}')

    def stop_note(self, note_to_stop):
        fluidsynth.stop_Note(note_to_stop, self.channel)

    def which_octave(self):
        """determines the octave to be played by the piano
         and includes a drunk walk"""
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

    def which_note(self, incoming_data, rhythm_rate):
        """receives raw data from robot controller
        and converts into piano note"""

        # decide to make sound or not based on project %
        if random() <= self.note_played_or_not:
            print('play')

            # which harmonic set - major of lydian
            # todo - build this to include Russell's scales
            #  & build complexity vs duration
            if getrandbits(1) == 1:
                # lydian chord shapes
                chord_shapes = self.lyd_chord_shapes
                print("lydian shapes")
            else:
                # major chord shapes
                chord_shapes = self.major_key_chord_shapes
                print("major shapes")

            # get the current bar position to align to harmonic progression
            bar_position = self.harmony_dict.get('bar') - 1
            print(bar_position)

            # # what is length of progression? is it 4 bars or under?
            # progression_length = len(self.progression)
            # print(progression_length)
            #
            # # if its less than 4 bars, repeat last bar
            # if bar_position > progression_length:
            #     bar_position = progression_length

            # current position in progression = the chord type
            pos = self.progression[bar_position]
            print(pos)

            # calc position of root (1st position) for each chord in progression
            root_of_this_chord = pos[1] + self.master_key

            # go get its name from alphabet
            if root_of_this_chord <= 11:
                chord_root = self.note_alphabet[root_of_this_chord]
            else:
                chord_root = self.note_alphabet[root_of_this_chord - 12]
            # print('chord is ', chord_root, pos[2])
            self.harmony_dict['chord'] = chord_root + pos[2]

            # get its shape of chordtones from chord shapes dict
            chord = chord_shapes.get(pos[0])
            # print('chord shape is', chord)

            # add the scale to the harmony dict for GUI
            scale_list = []
            for this_note in chord:
                scale_note = this_note[0] + root_of_this_chord
                if scale_note <= 11:
                    scale_note_name = self.note_alphabet[scale_note]
                else:
                    scale_note_name = self.note_alphabet[scale_note - 12]
                scale_list.append(scale_note_name)

            # self.harmony_dict['scale'] = scale_list
            # print("scale = ", scale_list)

            # shufle chord seq
            shuffle(chord)

            # rough random for weighting
            which_weight = random() * 100
            current_sum = 0

            # find note to play using weighting
            for note_pos, weight in chord:
                # print(note_pos, weight)

                # which note depending on weighting
                current_sum += weight
                if current_sum > which_weight:

                    # work out note name from chord and master key offset
                    note_name = root_of_this_chord + note_pos
                    if note_name <= 11:
                        chord_note = self.note_alphabet[note_name]
                    else:
                        chord_note = self.note_alphabet[note_name - 12]

                    # print(which_weight, chord_note)

                    # create note to play event
                    # random generate a dynamic
                    dynamic = 90 + randrange(1, 30)

                    # package into dict for queue
                    note_to_play = dict(note_name=chord_note,
                                        octave=self.octave,
                                        endtime=time() + rhythm_rate,
                                        dynamic=dynamic)

                    self.incoming_note_queue.append(note_to_play)

                    # add final dictionary details
                    print('playing', chord_note)
                    self.harmony_dict['note'] = chord_note

                    break












            # # which chord & is it root or lyd
            # # normal chord notes or jazz/ lyd notes
            # if getrandbits(1) == 1:
            #     if bar_position == 0:
            #         chord = self.dmin7
            #         self.harmony_dict['chord'] = "Dmin7"
            #     elif bar_position == 1:
            #         chord = self.g9
            #         self.harmony_dict['chord'] = "G9"
            #     else:
            #         chord = self.cM7
            #         self.harmony_dict['chord'] = "Cmaj7"
            #
            # else:
            #     if bar_position == 0:
            #         chord = self.dmin7_lyd
            #         self.harmony_dict['chord'] = "Dmin7 lydian"
            #     elif bar_position == 1:
            #         chord = self.g9_lyd
            #         self.harmony_dict['chord'] = "G9 lydian"
            #     else:
            #         chord = self.cM7_lyd
            #         self.harmony_dict['chord'] = "Cmaj7 lydian"

            #
            # # which chord & is it root or lyd
            # # normal chord notes or jazz/ lyd notes
            # if getrandbits(1) == 1:
            #     # major chord shapes
            #     chord_shapes = self.lyd_chord_shapes
            # else:
            #     chord_shapes = self.major_key_chord_shapes
            #
            # progression_length = len(self.progression)
            # print(progression_length)
            #
            # if bar_position > progression_length:
            #     bar_position = progression_length
            #
            # pos = self.progression[bar_position]
            #
            # # calc position of root (1st position) for each chord in progression
            # root_of_this_chord = pos[1] + self.masterkey
            # # go get its name from alphabet
            # if root_of_this_chord <= 11:
            #     chord_root = self.note_alphabet[root_of_this_chord]
            # else:
            #     chord_root = self.note_alphabet[root_of_this_chord - 12]
            # print('chord is ', chord_root)
            #
            # # get its shape of chordtones from chord shapes dict
            # chordtones = chord_shapes.get(pos[0])
            # print('chord shape is', chordtones)
            #
            # # for each of chord tones this shape calc the actual note
            # for chordtone in chordtones:
            #     # add the master key & print the chordtone as iterated from note alphabet
            #     chord_note_position = root_of_this_chord + chordtone[0]
            #     if chord_note_position <= 11:
            #         chord_note = self.note_alphabet[chord_note_position]
            #     else:
            #         chord_note = self.note_alphabet[chord_note_position - 12]
            #     print(
            #         f'\t {pos[0]} chord {chord_root}{pos[2]} in master key {self.note_alphabet[master_key]}  = {chord_note}, with weighting {chordtone[1]}%')
            #
            # # shufle chord seq --- too much random???
            # shuffle(chord)
            #
            # # # which note
            # # len_of_chord = len(chord)
            # # which_note = randrange(len_of_chord)
            # # this_note, this_weight = chord[which_note]
            # # print(this_note, this_weight)
            #
            # # rough random for weighting
            # which_weight = random() * 100
            #
            # # which octave? Drunk walk
            # drunk_octave = randrange(4)
            #
            # # drunk move down octave
            # if drunk_octave == 0:
            #     self.octave -= 1
            #
            # # drunk move up an octave
            # elif drunk_octave == 1:
            #     self.octave += 1
            #
            # # drunk reset to octave 4
            # elif drunk_octave == 3:
            #     self.octave = 4
            #
            # # check its in range
            # if self.octave < self.LOWEST:
            #     self.octave = 3
            # elif self.octave > self.OCTAVES:
            #     self.octave = 4
            #
            # # get note and play
            # current_sum = 0
            # for note_pos, weight in chord:
            #     note_name = self.note_list[note_pos]
            #     # print(f'original note name = {self.note_list[note_pos]}; '
            #     #       f'adjusted note name = {note_name}, weight = {weight}')
            #
            #     # which note depending on weighting
            #     current_sum += weight
            #     if current_sum > which_weight:
            #         print('playing', note_name)
            #         self.harmony_dict['note'] = note_name
            #
            #         # random generate a dynamic
            #         dynamic = 90 + randrange(1, 30)
            #
            #         # package into dict for queue
            #         note_to_play = dict(note_name=note_name,
            #                             octave=self.octave,
            #                             endtime=time() + rhythm_rate,
            #                             dynamic=dynamic)
            #
            #         # print (f'current time = {time()},  note data =   {note_to_play}')
            #         # add note, octave, duration (from visual processing)
            #         self.incoming_note_queue.append(note_to_play)
            #         # self.play_note(Note(note_name, self.octave))
            #         # self.played_note = note_name
            #         break


if __name__ == "__main__":
    piano = Piano()
    for x in range(10):
        piano.which_note(x, random())
        sleep(1)
