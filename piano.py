# -*- coding: utf-8 -*-
"""
*** Description ***
    A pygame MIDI piano.
    This piano is completely controlled by the keyboard, no MIDI hardware is
    required. You only have to set the SF2 variable to a valid soundfont file.
*** Keys ****
    Base octave:
        z,x,c,v,b,n,m    C,D,E,F,G,A,B
        s,d,g,h,j    C#,D#,F#,G#,A#
    Octave higher:
        w,e,r,t,y,u,i   C,D,E,F,G,A,B
        3,4,6,7,8    C#,D#,F#,G#,A#
    Control octaves (default = 4):
        -        octave down
        =        octave up
    Control channels (default = 8):
        backspace    channel down
        \        channel up
"""



# import pygame
# from pygame.locals import *
# from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth
from time import sleep
from random import random, randrange, getrandbits


class Piano:
    def __init__(self):
        SF2 = "media/soundfontGM.sf2"
        self.OCTAVES = 5  # number of octaves to show
        self.LOWEST = 2  # lowest octave to show
        self.FADEOUT = 0.25  # coloration fadeout time (1 tick = 0.001)

        self.note_list = ["A", "B", "C", "D", "E", "F", "G", "A"]

        # set up harmonic matrix with weighting adding to 100%
        self.dmin7 = [(3, 20), (5, 40), (0, 10), (2, 30)]
        self.g9 = [(6, 15), (1, 35), (3, 5), (5, 20), (0, 25)]
        self.cM7 = [(2, 20), (4, 40), (6, 10), (1, 30)]

        self.octave = 4
        self.channel = 8

        # start fluidsynth
        fluidsynth.init(SF2)
        # self.played_note = "C"

        # start someform of clock for chord sequence
        self.tick = 0.0


    def play_note(self, note):
        """play_note determines the coordinates of a note on the keyboard image
        and sends a request to play the note to the fluidsynth server"""

        fluidsynth.play_Note(note, self.channel, 100)

    def which_note(self, incoming_data):
        """receives raw data from robot controller and converts into piano note"""

        # turn previous note off
        # fluidsynth.stop_Note(note=self.played_note)

        # which chord
        # if self.tick:
        rnd_chord = randrange(3)
        # if rnd_chord == 0:
        #     chord = self.dmin7
        # elif rnd_chord == 1:
        #     chord = self.g9
        # else:
        chord = self.cM7
        print (chord)

        # # which note
        # len_of_chord = len(chord)
        # which_note = randrange(len_of_chord)
        # this_note, this_weight = chord[which_note]
        # print(this_note, this_weight)

        # rough random for weighting
        which_weight = random() * 100
        print(which_weight)

        # chord note or next note?
        add_whole_note = getrandbits(1)
        print(add_whole_note)

        current_sum = 0
        for note_pos, weight in chord:
            note_name = self.note_list[note_pos + add_whole_note]
            print(note_name, weight)
            current_sum += weight
            if current_sum > which_weight:
                print('playing', note_name)
                self.play_note(Note(note_name, self.octave))
                # self.played_note = note_name
                break




        #
        # # work out weighting
        # # if
        #
        #
        # # quick rescale as a fix
        # # note_data = incoming_data
        #
        #
        #
        #
        # if add_whole_note:
        #
        #     note_data = randrange(13)
        #     note_data += 1
        #
        #     if note_data == 1:
        #         self.play_note(Note("C", self.octave))
        #     elif note_data == 2:
        #         self.play_note(Note("C#", self.octave))
        #     elif note_data == 3:
        #         self.play_note(Note("D", self.octave))
        #     elif note_data == 4:
        #         self.play_note(Note("D#", self.octave))
        #     elif note_data == 5:
        #         self.play_note(Note("E", self.octave))
        #     elif note_data == 6:
        #         self.play_note(Note("F", self.octave))
        #     elif note_data == 7:
        #         self.play_note(Note("F#", self.octave))
        #     elif note_data == 8:
        #         self.play_note(Note("G", self.octave))
        #     elif note_data == 9:
        #         self.play_note(Note("G#", self.octave))
        #     elif note_data == 10:
        #         self.play_note(Note("A", self.octave))
        #     elif note_data == 11:
        #         self.play_note(Note("A#", self.octave))
        #     elif note_data == 12:
        #         self.play_note(Note("B", self.octave))
        #     elif note_data == 13:
        #         self.play_note(Note("C", self.octave + 1))

if __name__ == "__main__":
    piano = Piano()
    for x in range(10):
        piano.which_note(x)
        sleep(1)
