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

# chord types are
chord_shapes = {"1": [(0, 20), (4, 40), (7, 10), (11, 30)],
                "2": [(0, 20), (3, 40), (7, 10), (10, 30)],
                "5": [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)]
                }

lyd_chord_shapes = {"1": [(0, 15), (4, 20), (7, 5), (11, 15),
                   (2, 15), (6, 20), (9, 10)],
                "2": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                "5": [(0, 15), (4, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)]
                }

master_key = 6 # Cmajor

# list the name and note alphabet position for each progression
progression251 = [("2", 2), ("5", 7), ("1", 0)] # ii-V-1

print(f"2-5-1 in key of {note_alphabet[master_key]}")

for pos in progression251:
    # calc position of root (1st position) for each chord in progression
    root_of_this_chord = pos[1] + master_key
    # go get its name from alphabet
    if root_of_this_chord <= 11:
        chord_root = note_alphabet[root_of_this_chord]
    else:
        chord_root = note_alphabet[root_of_this_chord-12]
    print ('chord is ', chord_root)

    # get its shape of chordtones from chord shapes dict
    chordtones = lyd_chord_shapes.get(pos[0])
    print ('chord shape is', chordtones)

    # for each of chord tones this shape calc the actual note
    for chordtone in chordtones:
        # add the master key & print the chordtone as iterated from note alphabet
        chord_note_position = root_of_this_chord + chordtone[0]
        if chord_note_position <= 11:
            chord_note = note_alphabet[chord_note_position]
        else:
            chord_note = note_alphabet[chord_note_position-12]
        print(f'\t {pos[0]} chord in master key {note_alphabet[master_key]}  = {chord_note}, with weighting {chordtone[1]}%')

