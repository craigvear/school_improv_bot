import harmony
from random import getrandbits, shuffle, random
from operator import itemgetter

class Notes:
    def __init__(self):
        self.OCTAVES = 5  # number of octaves to show
        self.LOWEST = 3  # lowest octave to show

        ##############################################################
        # new matrix here
        ##############################################################

        # alt method using full 12 note alphabet: 0 - 11
        # self.note_alphabet = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]
        self.note_alphabet = harmony.note_alphabet

        # chord types are 1: tonic Maj7; 2: minor 7th; 4: sub dom maj7; 5: dom 7th etc
        # self.major_key_chord_shapes = {"1": [(0, 20), (4, 40), (7, 10), (11, 30)],
        #                      "3": [(0, 20), (3, 40), (7, 10), (10, 30)],
        #                      "2": [(0, 20), (3, 40), (7, 10), (10, 30)],
        #                      "5": [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)],
        #                      "6": [(0, 20), (3, 40), (7, 10), (10, 30)]
        #                                }
        self.major_key_chord_shapes = harmony.major_key_chord_shapes

        # same as above but with lyd + whole tone extensions to core triad chord tones
        # e.g. 9th, #11, 13
        # self.lyd_chord_shapes = {"1": [(0, 15), (4, 20), (7, 5), (11, 15),
        #                                (2, 15), (6, 20), (9, 10)],
        #                          "2": [(0, 15), (3, 20), (7, 5), (10, 15),
        #                                (2, 15), (5, 20), (9, 10)],
        #                          "3": [(0, 15), (3, 20), (7, 5), (10, 15),
        #                                (2, 15), (5, 20), (9, 10)],
        #                          "5": [(0, 15), (4, 20), (7, 5), (10, 15),
        #                                (2, 15), (5, 20), (9, 10)],
        #                          "6": [(0, 15), (3, 20), (7, 5), (10, 15),
        #                                (2, 15), (5, 20), (9, 10)]
        #                          }
        self.lyd_chord_shapes = harmony.lyd_chord_shapes

        # list the name and note alphabet position for each progression
        # progression2511 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")]
        # progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
        # progression3625 = [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]

        # # which progression
        # self.progression = harmony.progression["1625"]

        self.master_key = 3  # which is C on the note alphabet

        # piano range vars
        self.octave = 4
        self.channel = 1

        # transposition
        self.transposition = 0

    def which_note(self, harmony_dict, num_of_notes=1):
        """calcs a note from current harmony matrix.
        this function calcs the harmonic chord tones"""
        #
        # # setup list for returning note values
        # chord_note = []

        # 1. what is current harmonic data
        # extract data from harmony dict
        self.prog_pos, self.chord_name, self.note, self.root_number, self.root_name = itemgetter("prog_pos",
                                                                             "chord_name",
                                                                             "note",
                                                                             "root_number",
                                                                             "root_name")(harmony_dict)

        print(self.prog_pos, self.chord_name, self.note, self.root_number, self.root_name)

        # 2 which harmonic set - major of lydian
        # todo - build this to include Russell's scales
        #  & build complexity vs duration
        if getrandbits(1) == 1:
            # lydian chord shapes
            chord_shapes = self.lyd_chord_shapes
            print("lydian shapes")
        else:
            # major chord shapes
            chord_shapes = self.major_key_chord_shapes
            print("major shapes")


        # 3 get its shape of chordtones from chord shapes dict
        # e.g."2": [(0, 15), (3, 20), (7, 5), (10, 15), (2, 15), (5, 20), (9, 10)]
        this_chord_array = chord_shapes.get(self.prog_pos[0])
        print('this chord shape is', this_chord_array)

        # 4 generate a note from this shape using weightings
        chord_note = self.get_note(this_chord_array, num_of_notes)

        # 5 return the note for piano to play
        # or notes for image generator
        return chord_note

    #
    # def which_chord(self):
    #     # setup list for returning note values
    #     chord_note = []
    #
    #     # extract data from harmony dict
    #     root_of_this_chord, pos = itemgetter("root",
    #                                             "pos")(self.harmony_dict)
    #
    #     # # which harmonic set - major of lydian
    #     # # todo - build this to include Russell's scales
    #     # #  & build complexity vs duration
    #     # if getrandbits(1) == 1:
    #     #     # lydian chord shapes
    #     #     chord_shapes = self.lyd_chord_shapes
    #     #     print("lydian shapes")
    #     # else:
    #     #     # major chord shapes
    #     #     chord_shapes = self.major_key_chord_shapes
    #     #     print("major shapes")
    #
    #     # # get the current bar position to align to harmonic progression
    #     # bar_position = self.harmony_dict.get('bar')
    #
    #     # # current position in progression = the chord type
    #     # pos = self.progression[bar_position - 1]
    #
    #     # # calc position of root (1st position) for each chord in progression
    #     # root_of_this_chord = pos[1] + self.master_key
    #     #
    #     # # go get its name from alphabet
    #     # if root_of_this_chord <= 11:
    #     #     chord_root = self.note_alphabet[root_of_this_chord]
    #     # else:
    #     #     chord_root = self.note_alphabet[root_of_this_chord - 12]
    #     # # print('chord is ', chord_root, pos[2])
    #     # self.harmony_dict['chord'] = chord_root + pos[2]
    #
    #     # get its shape of chordtones from chord shapes dict
    #     chord = chord_shapes.get(pos[0])
    #     # print('chord shape is', chord)
    #
    #     return self.notes.get_note(self.harmony_dict, chord, num_of_notes)

    def get_note(self, this_chord_array, num_of_notes):
        """calcs a note from current harmony matrix
        harmony_dict = master harmony dict
        chord = current chord being used by improviser
        num_of_notes = how many notes to build 1 for piano bot,
        more for image making process
        """

        # current chord for process is
        print('chord shape is', this_chord_array)

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

                    # work out note name from chord and master key offset
                    note_num = self.root_number + note_pos + self.transposition
                    if note_num <= 11:
                        chord_note.append(harmony.note_alphabet[note_num])
                    else:
                        chord_note.append(harmony.note_alphabet[note_num - 12])

                    # # extract the note name for fluidsynth
                    # root_note_name = root_note_name[0]

                    # break out of loop
                    break
            print(f'chord note  ============== {chord_note[0]}')

        return chord_note