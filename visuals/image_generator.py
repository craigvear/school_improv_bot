# import python modules
import os
from random import randrange
from time import time
from operator import itemgetter

# import project modules
from sound.notes import Notes
from neoscore.common import *


class ImageGen:
    def __init__(self):
        self.notes = Notes()
        neoscore.setup()
        self.staff_unit = 10
        self.first_note_offset = self.staff_unit / 2

    def make_image(self, harmony_dict):
        """generate a random seq of notes on a staff
        using current harmonic seq as guide"""
        chord, note, bar, pos, root_name, key = itemgetter("chord_name",
                                                           "note",
                                                           "bar",
                                                           "prog_pos",
                                                           "root_name",
                                                                "key")(harmony_dict)

        chord = harmony_dict.chord_name
        note = harmony_dict.note
        bar = harmony_dict.bar
        pos = harmony_dict.prog_pos
        root_name = harmony_dict.root_name
        key = harmony_dict.key

        # how many notes?
        number_of_notes = randrange(1, 10)
        # print (f'IMAGE MAKER: number_of_notes == {number_of_notes}')

        manuscript_width = (number_of_notes + 1) * self.staff_unit + self.first_note_offset

        # create coordinate space container
        flow = Flowable(ORIGIN, None, Mm(manuscript_width), Mm(30))

        # generate a staff in the container
        # staff = Staff((Mm(0), Mm(0)), Mm(100), flow)
        staff = Staff(ORIGIN, flow, Mm(manuscript_width))

        # populate it with music furniture
        # todo get ket and current chord from harmony_dict
        Clef(ZERO, staff, 'treble')
        KeySignature(Mm(0), staff, f'{key[1]}_major')

        # get current chord from harmony_dict
        text = Text((Mm(3), staff.unit(-2)), staff, chord)

        note_list = self.notes.which_note(harmony_dict, number_of_notes)
        # print('note list = ', note_list)

        for n, note in enumerate(note_list):

            # use the 2nd part of note alphabet tuple
            printed_note = note[1] + "'"

            # print(f'printed note  ===== {printed_note}')
            Chordrest(Mm(self.first_note_offset + ((n + 1) * self.staff_unit)),
                      staff, [printed_note],
                      (1, 4))

        # save as a png render
        image_path = os.path.join(os.path.dirname(__file__), '../images',
                                  f'{time()}.png')

        # todo: rendered image is offset!!!
        neoscore.render_image(None,
                              image_path,
                              200)

        # neoscore.show()

        # reset the notation renderer
        text.remove()
        staff.remove()
        flow.remove()

        return image_path
