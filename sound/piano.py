# -*- coding: utf-8 -*-
"""
This class controls all the piano backing sound control and choices.
It calculates the current bar and beat and coordinates the bass line
It also controls all the piano note choices and rhythmical playback
"""
# import python modules
from mingus.containers import *
from mingus.midi import fluidsynth
from time import sleep, time
from random import random, randrange
import platform
from operator import itemgetter
from threading import Timer

# import project modules
from sound import harmony
from sound.notes import Notes
import config
from sound.harmony import Harmony

PLATFORM = platform.machine()

class Piano:
    def __init__(self, harmony_signal):

        self.harmony_signal = harmony_signal
        SF2 = "media/soundfontGM.sf2"
        self.OCTAVES = 5  # number of octaves to show
        self.LOWEST = 3  # lowest octave to show

        self.note_alphabet = harmony.note_alphabet

        self.major_key_chord_shapes = harmony.major_key_chord_shapes

        # same as above but with lyd + whole tone extensions to core triad chord tones
        # e.g. 9th, #11, 13
        self.lyd_chord_shapes = harmony.lyd_chord_shapes

        # which progression
        harmonic_prog = config.harmonic_prog

        # get progression from harmony dataclass
        self.progression = harmony.progression[harmonic_prog]

        self.master_key = config.master_key  # which is C on the note alphabet
        master_key_name = self.note_alphabet[3]

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

        # get temperature
        self.temperature = config.temperature

        # % factor if a note event is played or not
        self.note_played_or_not = 1 * self.temperature

        # state time sig
        self.time_sig = config.time_sig

        # state how many sub divides to a beat. 4=16ths, 12 = semi trips
        self.subdivision = config.subdivision

        # which turnaround
        self.turnaround_bar_length = len(self.progression)

        # consts for the counting process
        self.bar = 1
        self.beat = 1
        self.tick = 0

        # convert bar and beat to ms
        bpm_to_ms = config.bpm_to_ms

        # find the ms wait for subdivide
        self.sleep_dur = (bpm_to_ms / self.subdivision) / 1000

        self.harmony_dict = Harmony

        # init the note machine
        self.notes = Notes()

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

        # send details to the harmony signal emitter
        # self.fill_harmony_dict()

        # calc bar and beat & play root in LH
        self.chronos()

        # Update the piano playback system 12 times a beat (covers semi's and trips)
        playingThread = Timer(self.sleep_dur, self.update_player)
        playingThread.start()

    def chronos(self):
        """coordinate the master tempo and behaviours
        using BPM and root notes in bass LH"""
        # get bar e.g. 2
        current_bar = self.calc_bar()

        # current position in progression e.g. ("2", 2, "min7")
        # = "2" 2nd chord in 251, 2 on A major progression (before master key transposition) , chord type
        current_progression_pos = self.progression[current_bar - 1]

        # calc position of root (1st position) for this chord in the progression
        # and add master key transposition e.g. 2 + 6 = 8
        root_number_of_this_chord = current_progression_pos[1] + self.master_key

        # go get its name from alphabet e.g. 'F'
        if root_number_of_this_chord <= 11:
            root_note_name = self.note_alphabet[root_number_of_this_chord][0]
        else:
            root_note_name = self.note_alphabet[root_number_of_this_chord - 12][0]

        # # extract the note name for fluidsynth
        # root_note_name = root_note_name[0]

        # fill the harmony dict with current data every cycle and emit
        self.harmony_dict.chord_name = root_note_name + current_progression_pos[2]
        self.harmony_dict.prog_pos = current_progression_pos
        self.harmony_dict.root_number = root_number_of_this_chord
        self.harmony_dict.root_name = root_note_name
        self.send_harmony_dict()

        # on bar change play a bass note
        if current_bar != self._last_bar:
            # package the note to a dict
            bass = dict(note_name=root_note_name,
                        octave=self.bass_octave,
                        endtime=time() + 1,
                        dynamic=40)

            # and send to queue if active
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

        if self.bar > self.turnaround_bar_length:
            self.bar = 1

        self.harmony_dict.bar = self.bar

        # todo calc chord in progression here too

        # print('bar =', self.bar)
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

    def send_harmony_dict(self):

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

        # keep in the limits
        if self.octave < self.LOWEST:
            self.octave = self.LOWEST

        elif self.octave > (self.LOWEST + self.OCTAVES):
            self.octave = self.LOWEST

    def note_to_play(self, incoming_data, rhythm_rate):
        """receives raw data from soundbot controller
        and converts into piano note"""
        # decide to make sound or not based on project %
        # todo - increase frequency using temperature setting
        if random() <= self.note_played_or_not:
            # create note to add event to queue
            print('play')

            # todo - 2 or 3 notes every now and then?
            # what is the current chord in the harmonic prog?
            chord_note = self.notes.which_note(self.harmony_dict)

            # extract the note value (it returns a
            # list as image generator also calls this
            # returns tuple (fluidsynth_note_name, brown_note_name)
            chord_note = chord_note[0][0]

            # which octave?
            self.which_octave()

            # random generate a dynamic
            dynamic = 90 + randrange(1, 30)

            # todo - increase/ decrease duration using temperature
            # variable duration
            duration = rhythm_rate * (randrange(10, 30) / 10)

            # package into dict for queue
            note_to_play = dict(note_name=chord_note,
                                octave=self.octave,
                                endtime=time() + duration,
                                dynamic=dynamic)

            self.incoming_note_queue.append(note_to_play)

            # add final dictionary details
            # print('playing', chord_note)
            self.harmony_dict.note = chord_note
