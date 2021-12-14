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
        brown.setup()
        self.staff_unit = 10
        self.first_note_offset = self.staff_unit / 2

    def make_image(self, harmony_dict):
        """generate a random seq of notes on a staff
        using current harmonic seq as guide"""
        # brown.setup()
        chord, note, bar, pos, root_name = itemgetter("chord_name",
                                                           "note",
                                                           "bar",
                                                           "prog_pos",
                                                           "root_name")(harmony_dict)

        # how many notes?
        number_of_notes = randrange(1, 10)
        # print (f'IMAGE MAKER: number_of_notes == {number_of_notes}')

        manuscript_width = (number_of_notes + 1) * self.staff_unit + self.first_note_offset

        # create coordinate space container
        flow = Flowable((Mm(0), Mm(0)), Mm(manuscript_width), Mm(30))

        # generate a staff in the container
        # staff = Staff((Mm(0), Mm(0)), Mm(100), flow)
        staff = Staff((Mm(0), Mm(0)), Mm(manuscript_width), flow, Mm(1))

        # populate it with music furniture
        # todo get ket and current chord from harmony_dict
        Clef(staff, Mm(0), 'treble')
        KeySignature(Mm(0), staff, 'af_major')

        # get current chord from harmony_dict
        text = Text((Mm(3), staff.unit(-2)), chord)

        note_list = self.notes.which_note(harmony_dict, number_of_notes)
        # print('note list = ', note_list)

        for n, note in enumerate(note_list):

            # use the 2nd part of note alphabet tuple
            printed_note = note[1] + "'"

            # print(f'printed note  ===== {printed_note}')
            Chordrest(Mm(self.first_note_offset + ((n + 1) * self.staff_unit)), staff, [printed_note], Beat(1, 4))

        # save as a png render
        image_path = os.path.join(os.path.dirname(__file__), 'images',
                                  f'{time()}.png')

        # todo: rendered image is offset!!!
        brown.render_image((Mm(0), Mm(0), Mm(manuscript_width), Mm(30)), image_path,
                           dpi=200,
                           bg_color=Color(0, 120, 185, 0),
                           autocrop=True)

        # brown.show()

        # reset the notation renderer
        text.remove()
        staff.remove()
        flow.remove()

        return image_path
