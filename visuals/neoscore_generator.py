# import python modules
import os
from random import randrange, getrandbits
from time import time
from operator import itemgetter

# import project modules
from sound.notes import Notes
from neoscore.common import *
import sound.harmony_data as harmony
import config


class ImageGen:
    """Creates a neoscore image for a given chord"""
    def __init__(self):
        self.notes = Notes()
        neoscore.setup()
        self.staff_unit = 10
        # self.first_note_offset = self.staff_unit / 2

        # make key for neoscore notes: master key +- transposition
        self.key = config.master_key + config.transposition
        self.temperature = config.temperature


    def make_image(self, harmony_dict):
        """generate a random seq of notes on a staff
        using current harmonic seq as guide"""

        # how many notes?
        number_of_notes = int(randrange(1, 10) * self.temperature)
        # print (f'IMAGE MAKER: number_of_notes == {number_of_notes}')

        manuscript_width = (number_of_notes + 1) * self.staff_unit # + self.first_note_offset

        # create coordinate space container
        flow = Flowable(ORIGIN, None, Mm(manuscript_width), Mm(30))

        # generate a staff in the container
        # staff = Staff((Mm(0), Mm(0)), Mm(100), flow)
        staff = Staff(ORIGIN, flow, Mm(manuscript_width))

        # populate it with music furniture
        Clef(ZERO, staff, 'treble')
        key_name = harmony.note_alphabet[self.key][0]
        KeySignature(Mm(0), staff, f'{key_name}_major')

        # get current chord from harmony_dict
        # text = Text((Mm(3), staff.unit(-2)), staff, chord)

        note_list = self.notes.which_note(harmony_dict, number_of_notes)
        # print('note list = ', note_list)

        for n, note in enumerate(note_list):
            # use the 2nd part of note alphabet tuple
            printed_note = note[1] # + "'"

            # print(f'printed note  ===== {printed_note}')
            # todo- add complexity here depending on GEARS
            rnd_duration = randrange(4)
            if rnd_duration == 0:
                # crotchets
                note_dur = 4
            elif rnd_duration == 1:
                # quavers
                note_dur = 8
            elif rnd_duration == 2:
                # minums
                note_dur = 2
            else:
                # semi-quavers
                note_dur = 16

            # add temperature factor
            note_dur = int(note_dur * self.temperature)

            Chordrest(Mm((n + 1) * self.staff_unit),
                      staff, [printed_note],
                      (1, note_dur))

        # save as a png render
        image_path = os.path.join(os.path.dirname(__file__), '../images',
                                  f'{time()}.png')

        # todo: rendered image is offset!!!
        neoscore.render_image(None,
                              image_path,
                              200)

        # neoscore.show()

        # reset the notation renderer
        # text.remove()
        staff.remove()
        flow.remove()

        return image_path
