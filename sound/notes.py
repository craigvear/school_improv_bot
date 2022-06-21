from sound import harmony
import config

from random import getrandbits, shuffle, random
from operator import itemgetter

class Notes:
    def __init__(self):
        self.OCTAVES = 4  # number of octaves to show
        self.LOWEST = 5  # lowest octave to show

        self.note_alphabet = harmony.note_alphabet

        self.major_key_chord_shapes = harmony.major_key_chord_shapes

        self.lyd_chord_shapes = harmony.lyd_chord_shapes

        self.master_key = config.master_key  # which is C on the note alphabet

        # piano range vars
        self.octave = 5
        self.channel = 1

        # transposition
        self.transposition = config.transposition

    def which_note(self, harmony_dict, num_of_notes=1):
        """calcs a note from current harmony matrix.
        this function calcs the harmonic chord tones"""

        # bpm = config.bpm
        self.chord_name = harmony_dict.chord_name
        self.note = harmony_dict.note
        bar = harmony_dict.bar
        self.prog_pos = harmony_dict.prog_pos
        self.root_number = harmony_dict.root_number
        self.root_name = harmony_dict.root_name

        print("here", self.prog_pos, self.chord_name, self.note, self.root_number, self.root_name)

        # 2 which harmonic set - major of lydian
        # todo - build this to include Russell's scales
        #  & build complexity vs duration
        if getrandbits(1) == 1:
            # lydian chord shapes
            chord_shapes = self.lyd_chord_shapes
            # print("lydian shapes")
        else:
            # major chord shapes
            chord_shapes = self.major_key_chord_shapes
            # print("major shapes")


        # 3 get its shape of chordtones from chord shapes dict
        # e.g."2": [(0, 15), (3, 20), (7, 5), (10, 15), (2, 15), (5, 20), (9, 10)]
        this_chord_array = chord_shapes.get(self.prog_pos[0])
        # print('this chord shape is', this_chord_array)

        # 4 generate a note from this shape using weightings
        chord_note = self.get_note(this_chord_array, num_of_notes)

        # 5 return the note for piano to play
        # or notes for image generator
        return chord_note

    def get_note(self, this_chord_array, num_of_notes):
        """calcs a note from current harmony matrix
        harmony_dict = master harmony dict
        chord = current chord being used by improviser
        num_of_notes = how many notes to build 1 for piano bot,
        more for image making process
        """

        # current chord for process is
        # print('chord shape is', this_chord_array)

        # setup list for returning note values
        chord_note = []

        # Todo: transposition for different instrument tunings HERE

        # # add the scale to the harmony dict for GUI
        # scale_list = []
        # for this_note in this_chord_array:
        #     print(this_note[0], self.root_number)
        #     scale_note = this_note[0] + self.root_number
        #     if scale_note <= 11:
        #         scale_note_name = harmony.note_alphabet[scale_note]
        #     else:
        #         scale_note_name = harmony.note_alphabet[scale_note - 12]
        #     scale_list.append(scale_note_name)

        # self.harmony_dict['scale'] = scale_list
        # print("scale = ", scale_list)

        # loop for each note requested in *arg

        for n in range(num_of_notes):
            # shuffle chord seq
            shuffle(this_chord_array)

            # rough random for weighting
            which_weight = random() * 100
            current_sum = 0

            # find note to play using weighting
            for note_pos, weight in this_chord_array:
                # print(note_pos, weight)

                # which note depending on weighting
                current_sum += weight
                if current_sum > which_weight:

                    # todo: fix this as it only works in C major
                    # work out note name from chord and master key offset

                    # todo insert here duration data here too? e.g. if repeated count as ties?

                    note_num = self.root_number + note_pos + self.transposition
                    if note_num <= 11:
                        chord_note.append(harmony.note_alphabet[note_num])
                    else:
                        chord_note.append(harmony.note_alphabet[note_num - 12])

                    # # extract the note name for fluidsynth
                    # root_note_name = root_note_name[0]

                    # break out of loop
                    break
            # print(f'chord note  ============== {chord_note[0]}')

        return chord_note