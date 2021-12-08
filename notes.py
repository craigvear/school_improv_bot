import harmony
from random import getrandbits, shuffle, random
from operator import itemgetter

class Notes:
    def __init__(self):
        pass

    def get_note(self, harmony_dict, chord, num_of_notes=1):
        """calcs a note from current harmony matrix"""

        # setup list for returning note values
        chord_note = []

        # extract data from harmony dict
        root_of_this_chord, pos = itemgetter("root",
                                             "pos")(harmony_dict)

        # # which harmonic set - major of lydian
        # # todo - build this to include Russell's scales
        # #  & build complexity vs duration
        # if getrandbits(1) == 1:
        #     # lydian chord shapes
        #     chord_shapes = harmony.lyd_chord_shapes
        #     print("lydian shapes")
        # else:
        #     # major chord shapes
        #     chord_shapes = harmony.major_key_chord_shapes
        #     print("major shapes")
        #
        # # get the current bar position to align to harmonic progression
        # bar_position = self.harmony_dict.get('bar')
        #
        # # current position in progression = the chord type
        # pos = self.progression[bar_position - 1]
        #
        # # calc position of root (1st position) for each chord in progression
        # root_of_this_chord = pos[1] + self.master_key
        #
        # # go get its name from alphabet
        # if root_of_this_chord <= 11:
        #     chord_root = harmony.note_alphabet[root_of_this_chord]
        # else:
        #     chord_root = harmony.note_alphabet[root_of_this_chord - 12]
        # # print('chord is ', chord_root, pos[2])
        # self.harmony_dict['chord'] = chord_root + pos[2]

        # get its shape of chordtones from chord shapes dict


        self.chord = chord
        # print('chord shape is', chord)

        # add the scale to the harmony dict for GUI
        scale_list = []
        for this_note in chord:
            scale_note = this_note[0] + root_of_this_chord
            if scale_note <= 11:
                scale_note_name = harmony.note_alphabet[scale_note]
            else:
                scale_note_name = harmony.note_alphabet[scale_note - 12]
            scale_list.append(scale_note_name)

        # self.harmony_dict['scale'] = scale_list
        # print("scale = ", scale_list)

        # loop for each note requested in *arg

        for n in range(num_of_notes):
            # shuffle chord seq
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
                        chord_note.append(harmony.note_alphabet[note_name])
                    else:
                        chord_note.append(harmony.note_alphabet[note_name - 12])

                    # break out of loop
                    break
            print(f'chord note  ============== {chord_note[0]}')

        return chord_note