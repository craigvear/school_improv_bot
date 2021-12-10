# import python modules
import os
from random import randrange
from time import time
from operator import itemgetter

# import project modules
from notes import Notes
from brown.common import *


class ImageGen:
    def __init__(self):
        self.notes = Notes()
        # brown.setup()
        self.staff_unit = 8

    def make_image(self, harmony_dict):
        """generate a random seq of notes on a staff
        using current harmonic seq as guide"""
        brown.setup()
        bpm, chord, note, bar, pos, root_name = itemgetter("BPM",
                                                           "chord_name",
                                                           "note",
                                                           "bar",
                                                           "prog_pos",
                                                           "root_name")(harmony_dict)

        # how many notes?
        number_of_notes = randrange(1, 5)
        print (f'IMAGE MAKER: number_of_notes == {number_of_notes}')

        # create coordinate space container
        flow = Flowable((Mm(0), Mm(0)), Mm(20), Mm(30))

        # generate a staff in the container
        # staff = Staff((Mm(0), Mm(0)), Mm(20), flowable)
        staff = Staff((Mm(0), Mm(0)), Mm((number_of_notes + 1) * self.staff_unit), flow, Mm(1))

        # populate it with music furniture
        # todo get ket and current chord from harmony_dict

        Clef(staff, Mm(0), 'treble')
        KeySignature(Mm(0), staff, 'af_major')

        # todo get current chord from harmony_dict
        chord_name = 'BbMaj9'

        Text((Mm(3), staff.unit(-2)), chord_name)

        note_list = self.notes.which_note(harmony_dict, number_of_notes)

        for n, note in enumerate(note_list):

            printed_note = note.lower()+"'"
            Chordrest(Mm((n+1) * self.staff_unit), staff, [printed_note], Beat(2, 4))


            #
            #
            # # musictext = MusicText(staff, Mm(1), 'G')
            # # note1 = Notehead(Mm(10), "g'", (1, 2), staff)
            # # line = Stem(100, 30, staff)
            # note = Chordrest(Mm(10), staff, ["c'"], Beat(2, 4))
            # note2 = Chordrest(Mm(20), staff, ["a'", "bs"], Beat(2, 4))
            #
            #
            # note3 = Chordrest(Mm(30), staff, ["a'", "bs"], Beat(2, 4))
            # note4 = Chordrest(Mm(40), staff, ["a'", "bs"], Beat(2, 4))
            #
            # note5 = Chordrest(Mm(50), staff, ["a'", "bs"], Beat(2, 4))

        # slur = Slur((Mm(0), Mm(0), note1),
        #             (Mm(0), Mm(0), (number_of_notes + 1) * 10))

        image_path = os.path.join(os.path.dirname(__file__), 'images',
                                  f'{time()}.png')
        brown.render_image((Mm(0), Mm(0), Inch(2), Inch(2)), image_path,
                           bg_color=Color(0, 120, 185, 0),
                           autocrop=True)

        # todo clear all notes to reset


        #
        # brown.show()