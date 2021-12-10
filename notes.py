import harmony
from random import getrandbits, shuffle, random
from operator import itemgetter

class Notes:
    def __init__(self):
        pass

    def get_note(self, harmony_dict, chord, num_of_notes=1):
        """calcs a note from current harmony matrix
        harmony_dict = master harmony dict
        chord = current chord being used by improviser
        num_of_notes = how many notes to build 1 for piano bot,
        more for image making process
        """

        # current chord for process is
        self.chord = chord
        print('chord shape is', chord)

        # setup list for returning note values
        chord_note = []

        # extract data from harmony dict
        BPM, bar, pos, chord, note, root_of_this_chord, root_name = itemgetter("BPM",
                             "bar",
                             "pos",
                             "chord",
                             "note",
                             "root",
                             "root_name")(harmony_dict)


        print(BPM, bar, pos, chord, note, root_of_this_chord, root_name )

        # Todo: transposition for different instrument tunings HERE

        # add the scale to the harmony dict for GUI
        scale_list = []
        for this_note in self.chord:
            print(this_note[0], root_of_this_chord)
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
            shuffle(self.chord)

            # rough random for weighting
            which_weight = random() * 100
            current_sum = 0

            # find note to play using weighting
            for note_pos, weight in self.chord:
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