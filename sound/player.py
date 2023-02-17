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
import logging


# import project modules
from sound import harmony_data
from sound.notes import Notes
import config
from sound.harmony_data import HarmonyBorg

PLATFORM = platform.machine()


class Chord:
    """Creates and object for each chord in the progression.
    Args:

        """

    def __init__(self, chord_data):
        # generate harmonic params
        self.tonic_root = chord_data[0]
        _tonic_root_position = self.calc_note_number(self.tonic_root)
        self.lydian_root = self.calc_lydian_root(chord_data, _tonic_root_position)

        # generate scales and chords with note names
        self.scale_dict, self.chord_dict = self.generate_principle_scales(self.lydian_root)

    def calc_note_number(self, root_name):
        """
        Using harmony_data.note_alphabet calculates the position of the root
        :param root_name:
        :return:
        """
        position = [i for i, note in enumerate(harmony_data.note_alphabet) if note == root_name]
        return position[0]

    def calc_lydian_root(self, chord_type, tonic_position):
        """
        Calculates the Lydian root given the chord type
        (primary modal genre e.g. min 7th), and the tonic root.
        Returns:
            lydian tonic note name and position on note_list
        """

        tonic_root = chord_type[0]
        primary_modal_genre = chord_type[1]

        def find_lydian_position(tonic_position, lydian_offset):
            """Calculates the lydian root using the root and lydian offset from the PMG model"""
            lydian_position = tonic_position + lydian_offset
            # note_num = self.root_number + note_pos + self.transposition
            if lydian_position <= 11:
                return harmony_data.note_alphabet[lydian_position]
                # chord_note.append(harmony_data.note_alphabet[note_num])
            else:
                return harmony_data.note_alphabet[lydian_position - 12]

        if primary_modal_genre == "I":
            lydian_root_offset = 0
        elif primary_modal_genre == "II":
            lydian_root_offset = 10
        elif primary_modal_genre == "III":
            lydian_root_offset = 8
        elif primary_modal_genre == "+IV":
            lydian_root_offset = 6
        elif primary_modal_genre == "V":
            lydian_root_offset = 5
        elif primary_modal_genre == "VI":
            lydian_root_offset = 3
        elif primary_modal_genre == "VII":
            lydian_root_offset = 1
        elif primary_modal_genre == "+V":
            lydian_root_offset = 4

        else:
            lydian_root_offset = 0

        return find_lydian_position(tonic_position, lydian_root_offset)

    def generate_principle_scales(self, lydian_root):
        """Generates a list of all the primary scales associated with the lydian
        root of this chord
        """
        scales = {}
        chords = {}
        lyd_root_position = self.calc_note_number(lydian_root)
        ninth_chord_shape = [0, 2, 4, 6, 8]

        for i, scale_code in enumerate(config.scale_patterns):
            lydian_primary_scale = [lydian_root]
            this_note = lyd_root_position
            for interval in scale_code:

                next_note = this_note + interval

                if next_note <= 11:
                    next_note_name = harmony_data.note_alphabet[next_note]
                    # chord_note.append(harmony_data.note_alphabet[note_num])
                else:
                    next_note_name = harmony_data.note_alphabet[next_note - 12]

                lydian_primary_scale.append(next_note_name)
                this_note = next_note

            logging.debug(f"lydian_primary_scale = {i, lydian_primary_scale}")

            # check scale contains tonic (and is therefore prevailing in this chordmode)
            for n, note in enumerate(lydian_primary_scale):
                if note == self.tonic_root:
                    scales[f"scale{i}"] = lydian_primary_scale
                    tonic_root_position = n

                    # adding 9th chord for each valid scale
                    chord = []
                    for offset in ninth_chord_shape:
                        next_note_pos = tonic_root_position + offset

                        # calc loop around for scale
                        if next_note_pos >= (len(lydian_primary_scale) -1):
                            next_note_pos -= len(lydian_primary_scale)

                        chord.append(lydian_primary_scale[next_note_pos])
                    chords[f"chord{i}"] = chord
                    logging.debug(f"chord = {i, chord}")
                    # break

        return scales, chords


class Player:
    def __init__(self): #, harmony_signal):

        # self.harmony_signal = harmony_signal
        SF2 = "sound/soundfontGM.sf2"
        self.OCTAVES = 5  # number of octaves to show
        self.LOWEST = 3  # lowest octave to show

        self.note_alphabet = harmony_data.note_alphabet

        self.major_key_chord_shapes = harmony_data.major_key_chord_shapes

        # same as above but with lyd + whole tone extensions to core triad chord tones
        # e.g. 9th, #11, 13
        self.lyd_chord_shapes = harmony_data.lyd_chord_shapes

        # which progression
        harmonic_prog = {}

        for chord in config.harmonic_prog:
            chord_object = Chord(chord)
            try:
                harmonic_prog[f"{chord[0] + chord[1]}"] = chord_object
            except:
                logging.info(f"{chord[0] + chord[1]} already existing in harmony dictionary")


        # get progression from harmony dataclass
        self.progression = harmony_data.progression[harmonic_prog]
        # print("PROGRESSION", self.progression)

        self.master_key = config.master_key  # which is C on the note alphabet
        master_key_name = self.note_alphabet[3]

        # piano range vars
        self.octave = 4

        # chronos vars
        self.bass_octave = 1
        self._last_bar = None

        # start fluidsynth
        if PLATFORM == "x86_64":
            fluidsynth.init(SF2)
        else:
            fluidsynth.init(SF2, "alsa")

        # instrument 0 = piano, 1 = bass
        fluidsynth.set_instrument(0, 1)
        fluidsynth.set_instrument(1, 32)
        self.channel_piano = 0
        self.channel_bass = 1

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

        self.harmony_dict = HarmonyBorg()

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
        self.process_queues()

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
        # print("current pos", current_progression_pos)

        # calc position of root (1st position) for this chord in the progression
        # and add master key transposition e.g. 2 + 6 = 8
        root_number_of_this_chord = current_progression_pos[0] + self.master_key
        # print("root", root_number_of_this_chord)

        # go get its name from alphabet e.g. 'F'
        if root_number_of_this_chord <= 11:
            root_note_name = self.note_alphabet[root_number_of_this_chord][0]
        else:
            root_note_name = self.note_alphabet[root_number_of_this_chord - 12][0]

        # # extract the note name for fluidsynth
        # root_note_name = root_note_name[0]

        # fill the harmony dict with current data every cycle and emit
        self.harmony_dict.chord_name = root_note_name + current_progression_pos[1]
        self.harmony_dict.chord_shape = current_progression_pos[1]
        # print('dict current_progression_pos[1]', current_progression_pos[1])
        self.harmony_dict.chord_shape_list = harmony_data.chord_shapes.get(current_progression_pos[1])
        # print('dict self.chord_shape_list', self.harmony_dict.chord_shape_list)
        self.harmony_dict.prog_pos = current_progression_pos
        self.harmony_dict.root_number = root_number_of_this_chord
        self.harmony_dict.root_name = root_note_name
        # self.send_harmony_dict()

        # on bar change play a bass note
        if current_bar != self._last_bar:
            # package the note to a dict
            # todo - move this to def play_bass & get bass substitute from progression

            bass = dict(note_name=root_note_name,
                        octave=self.bass_octave,
                        channel=self.channel_bass,
                        endtime=time() + 1,
                        dynamic=100)

            print('bass = ', bass)

            # and send to queue if active
            if self.bass_line:
                self.incoming_note_queue.append(bass)

        self._last_bar = current_bar

    def play_bass(self):
        pass

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

        # print('bar =', self.bar)
        return self.bar

    def process_queues(self):
        # this func spins around controlling the 2 note queues
        # print("1")
        # print('incoming note queue', self.incoming_note_queue)
        if len(self.incoming_note_queue):

            # piano
            for i, event in enumerate(self.incoming_note_queue):
                note_name, octave, channel, dynamic = itemgetter("note_name",
                                                        "octave",
                                                                 "channel",
                                                        "dynamic")(event)

                # play note
                self.play_piano(note_name, octave, channel, dynamic)

                # delete from incoming queue
                del self.incoming_note_queue[i]

                # add to played list
                self.played_note_queue.append(event)

            # bass



            # drums


        if len(self.played_note_queue):
            for i, event in enumerate(self.played_note_queue):
                lifespan, note_name, channel, octave = itemgetter("endtime",
                                                                  "note_name",
                                                                  "channel",
                                                                  "octave")(event)

                # if lifespan (endtime) is less than current time
                if lifespan <= time():
                    # stop note
                    self.stop_note(note_name, octave, channel)

                    # delete from played queue
                    del self.played_note_queue[i]

    # def send_harmony_dict(self):
    #
    #     self.harmony_signal.harmony_str.emit(self.harmony_dict)
    #     # print('//////////////////                   EMITTING and making sound')

    def play_piano(self, note_to_play, octave, channel, dynamic):
        """play_note determines the coordinates of a note on the keyboard image
        and sends a request to play the note to the fluidsynth server"""

        # dynamic = 90 + randrange(1, 30)
        fluidsynth.play_Note(Note(name=note_to_play,
                                  octave=octave,
                                  channel=channel,
                                  velocity=dynamic)
                             )
        print(f'\t\t\t\t\tplaying {note_to_play}, channel {channel}, velocity {dynamic}')

    def stop_note(self, note_to_stop, octave, channel):
        fluidsynth.stop_Note(Note(name=note_to_stop,
                                  octave=octave,
                                  channel=channel)
                             )

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

    def note_to_play(self, emission_dict):
        """receives raw data from Nantucket controller
        and converts into piano note.

        incoming data = Nebula output from affect engine
        rhythm rate = nebula internal clock
        """

        incoming_data = emission_dict.get("emission_data")
        rhythm_rate = emission_dict.get("rhythm_rate")

        # decide to make sound or not based on project temperature
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
            dynamic = 70 + randrange(1, 50)

            # todo - increase/ decrease duration using temperature
            # variable duration = nebula current rhythm rate * random factor / temperature
            duration = (rhythm_rate * (randrange(10, 50) / 20)) / self.temperature

            # package into dict for queue
            note_to_play = dict(note_name=chord_note,
                                octave=self.octave,
                                channel=self.channel_piano,
                                endtime=time() + duration,
                                dynamic=dynamic)

            print('piano = ', note_to_play)

            self.incoming_note_queue.append(note_to_play)

            # add final dictionary details
            # print('playing', chord_note)
            self.harmony_dict.note = chord_note

        else:
            print('skipped over this emission')


if __name__ == "__main__":
    test = Chord(("A", "II", 4))
    print(f"tonic_root = {test.tonic_root}")
    print(f"lydian_root = {test.lydian_root}")
    print(f"test2.scale_dict.items = {test.scale_dict.items()}")
    for scale in test.scale_dict.items():
        print(f"scale = {scale}")
    print(f"test2.chord_dict.items = {test.chord_dict.items()}")
    for chord in test.chord_dict.items():
        print(f"chord = {chord}")

    # test2 = Chord(("B", "V", 4))
    # print(f"tonic_root = {test2.tonic_root}")
    # print(f"lydian_root = {test2.lydian_root}")
    # print(f"test2.scale_dict.items = {test2.scale_dict.items()}")
    # for scale in test2.scale_dict.items():
    #     print(f"scale = {scale}")
    # print(f"test2.chord_dict.items = {test2.chord_dict.items()}")
    # for chord in test2.chord_dict.items():
    #     print(f"chord = {chord}")
