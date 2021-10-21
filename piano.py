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
from time import sleep, time
from random import random, randrange, getrandbits, shuffle


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
        self.played_note = 0

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
        now_time = int(time())
        bar = now_time % 4

        # rnd_chord = randrange(3)
        if bar == 0:
            chord = self.dmin7
        elif bar == 1:
            chord = self.g9
        else:
            chord = self.cM7

        # shufle chord seq --- too much random???
        shuffle(chord)
        print(chord)

        # # which note
        # len_of_chord = len(chord)
        # which_note = randrange(len_of_chord)
        # this_note, this_weight = chord[which_note]
        # print(this_note, this_weight)

        # rough random for weighting
        which_weight = random() * 100

        # chord note or next note?
        add_whole_note = randrange(2)

        # which octave? Drunk walk
        drunk_octave = randrange(4)
        print('                         ', drunk_octave)
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
            note_name = self.note_list[note_pos + add_whole_note]
            print(f'original note name = {self.note_list[note_pos]}; '
                  f'adjusted note name = {note_name}, weight = {weight}')

            # which note depending on weighting
            current_sum += weight
            if current_sum > which_weight:
                print('playing', note_name)
                self.play_note(Note(note_name, self.octave))
                self.played_note = note_name
                break


if __name__ == "__main__":
    piano = Piano()
    for x in range(10):
        piano.which_note(x)
        sleep(1)
