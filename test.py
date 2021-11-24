from random import getrandbits, shuffle, random, randrange

# alt method using full 12 note alphabet: 0 - 11
note_alphabet = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]

# set up harmonic matrix with weighting adding to 100%
# offset by starting tonic of master key

# minor 7th = ii in the 2-5-1
min7 = [(0, 20), (3, 40), (7, 10), (10, 30)]  # 1, 3, 5, 7 of minor scale
min7_sharp11_13 = [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)]  # 1, 3, 5, 7, 9, #11, 13 of minor scale

# major dom 9th - V in the 2-5-1
dom9 = [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)]  # flat 7
dom9_sharp11_13 = [(0, 15), (4, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)]

# major dom 9th - V in the 2-5-1
maj7 = [(0, 20), (4, 40), (7, 10), (11, 30)]
maj7_sharp11_13 = [(0, 15), (4, 20), (7, 5), (11, 15),
                   (2, 15), (5, 20), (9, 10)]

# chord types are 1: tonic Maj7; 2: minor 7th; 4: sub dom maj7; 5: dom 7th etc
major_key_chord_shapes = {"1": [(0, 20), (4, 40), (7, 10), (11, 30)],
                "3": [(0, 20), (3, 40), (7, 10), (10, 30)],
                "2": [(0, 20), (3, 40), (7, 10), (10, 30)],
                "5": [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)],
                "6": [(0, 20), (3, 40), (7, 10), (10, 30)]
                }
# same as above but with lyd + whole tone extensions to core triad chord tones
# e.g. 9th, #11, 13
lyd_chord_shapes = {"1": [(0, 15), (4, 20), (7, 5), (11, 15),
                   (2, 15), (6, 20), (9, 10)],
                "2": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                "3": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                    "5": [(0, 15), (4, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                  "6": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)]
                }

master_key = 3 # Cmajor

octave = 4

harmony_dict = {}

# list the name and note alphabet position for each progression
# (scale_position e.g. "5" chord in 2-5-1,
# alphabet_deviation_from_root e.g. 7 semitones from root,
# chord_name e.g. "Dom7"

progression251 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7")]
progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
progression3625 = [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]

progression = progression1625

print(len(progression))

print(f"1625 in key of {note_alphabet[master_key]}")


def which_octave():
    # which octave? Drunk walk
    drunk_octave = randrange(4)

    # drunk move down octave
    if drunk_octave == 0:
        octave -= 1

    # drunk move up an octave
    elif drunk_octave == 1:
        octave += 1

    # drunk reset to octave 4
    elif drunk_octave == 3:
        octave = 4

    return octave


for n in range(10):

    # which harmonic set - major of lydian
    if getrandbits(1) == 1:
        # lydian chord shapes
        chord_shapes = lyd_chord_shapes
        print("lydian shapes")
    else:
        # major chord shapes
        chord_shapes = major_key_chord_shapes
        print("major shapes")

    # what is bar position?
    bar_position = n % 4

    # what is length of progression? is it 4 bars or under?
    progression_length = len(progression)

    # if its less than 4 bars, repeat last bar
    if bar_position > progression_length:
        bar_position = progression_length

    # current position in progression = the chord type
    pos = progression[bar_position]

    # calc position of root (1st position) for each chord in progression
    root_of_this_chord = pos[1] + master_key

    print(n, bar_position, pos, root_of_this_chord)

    # go get its name from alphabet
    if root_of_this_chord <= 11:
        chord_root = note_alphabet[root_of_this_chord]
    else:
        chord_root = note_alphabet[root_of_this_chord-12]
    print ('chord is ', chord_root, pos[2])
    harmony_dict['chord'] = [chord_root, pos[2]]

    # get its shape of chordtones from chord shapes dict
    chord = chord_shapes.get(pos[0])
    print ('chord shape is', chord)

    # add the scale to the harmony dict for GUI
    scale_list = []
    for note in chord:
        scale_note = note[0] + root_of_this_chord
        if scale_note <= 11:
            scale_note_name = note_alphabet[scale_note]
        else:
            scale_note_name = note_alphabet[scale_note - 12]
        scale_list.append(scale_note_name)

    harmony_dict['scale'] = scale_list
    print("scale = ", scale_list)

    # shufle chord seq --- too much random???
    shuffle(chord)

    print(chord)

    # rough random for weighting
    which_weight = random() * 100
    current_sum = 0

    # find note to play using weighting
    for note_pos, weight in chord:
        print(note_pos, weight)

        # which note depending on weighting
        current_sum += weight
        if current_sum > which_weight:

            # work out note name from chord and master key offset
            note_name = root_of_this_chord + note_pos
            if note_name <= 11:
                chord_note = note_alphabet[note_name]
            else:
                chord_note = note_alphabet[note_name - 12]

            print(which_weight, chord_note)

            # create note to play event
            # random generate a dynamic
            dynamic = 90 + randrange(1, 30)

            package into dict for queue
            note_to_play = dict(note_name=chord_note,
                                octave=octave,
                                endtime=time() + rhythm_rate,
                                dynamic=dynamic)

            incoming_note_queue.append(note_to_play)


            # create dictionary details

            print('playing', chord_note)
            harmony_dict['note'] = chord_note


            break


    # print("###################################")



    #
    # octave = which_octave()
    #
    # # # check its in range
    # # if octave < LOWEST:
    # #     octave = 3
    # # elif octave > OCTAVES:
    # #     octave = 4
    #
    # # weighting stuff here
    # # get note and play
    # # rough random for weighting
    # which_weight = random() * 100
    # current_sum = 0
    # for note_pos, weight in chord:
    #     # note_name = self.note_list[note_pos]
    #     # print(f'original note name = {self.note_list[note_pos]}; '
    #     #       f'adjusted note name = {note_name}, weight = {weight}')
    #
    #     note_name = root_of_this_chord + chord[0]
    #     if note_name <= 11:
    #         chord_note = note_alphabet[note_name]
    #     else:
    #         chord_note = note_alphabet[note_name - 12]
    #
    #     # which note depending on weighting
    #     current_sum += weight
    #     if current_sum > which_weight:
    #         print('playing', note_name)
    #         self.harmony_dict['note'] = note_name
    #
    #         # random generate a dynamic
    #         dynamic = 90 + randrange(1, 30)
    #
    #         # package into dict for queue
    #         note_to_play = dict(note_name=note_name,
    #                             octave=self.octave,
    #                             endtime=time() + rhythm_rate,
    #                             dynamic=dynamic)
    #
    #         # print (f'current time = {time()},  note data =   {note_to_play}')
    #         # add note, octave, duration (from visual processing)
    #         self.incoming_note_queue.append(note_to_play)
    #         # self.play_note(Note(note_name, self.octave))
    #         # self.played_note = note_name
    #         break
    #
    #
    # # for each of chord tones this shape calc the actual note
    # for chordtone in chordtones:
    #     # add the master key & print the chordtone as iterated from note alphabet
    #     # chord_note_position = root_of_this_chord + chordtone[0]
    #     # if chord_note_position <= 11:
    #     #     chord_note = note_alphabet[chord_note_position]
    #     # else:
    #     #     chord_note = note_alphabet[chord_note_position-12]
    #     print(f'\t {pos[0]} chord {chord_root}{pos[2]} in master key {note_alphabet[master_key]}  = {chord_note}, with weighting {chordtone[1]}%')
    #



#
# for pos in progression:
#     # calc position of root (1st position) for each chord in progression
#     root_of_this_chord = pos[1] + master_key
#
#     # go get its name from alphabet
#     if root_of_this_chord <= 11:
#         chord_root = note_alphabet[root_of_this_chord]
#     else:
#         chord_root = note_alphabet[root_of_this_chord-12]
#     print ('chord is ', chord_root)
#
#     # get its shape of chordtones from chord shapes dict
#     chordtones = lyd_chord_shapes.get(pos[0])
#     print ('chord shape is', chordtones)
#
#     # for each of chord tones this shape calc the actual note
#     for chordtone in chordtones:
#         # add the master key & print the chordtone as iterated from note alphabet
#         chord_note_position = root_of_this_chord + chordtone[0]
#         if chord_note_position <= 11:
#             chord_note = note_alphabet[chord_note_position]
#         else:
#             chord_note = note_alphabet[chord_note_position-12]
#         print(f'\t {pos[0]} chord {chord_root}{pos[2]} in master key {note_alphabet[master_key]}  = {chord_note}, with weighting {chordtone[1]}%')
#
