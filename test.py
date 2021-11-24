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
chord_shapes = {"1": [(0, 20), (4, 40), (7, 10), (11, 30)],
                "2": [(0, 20), (3, 40), (7, 10), (10, 30)],
                "5": [(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)],
                "6": [[(0, 20), (3, 40), (7, 10), (10, 30)]]
                }
# same as above but with lyd + whole tone extensions to core triad chord tones
# e.g. 9th, #11, 13
lyd_chord_shapes = {"1": [(0, 15), (4, 20), (7, 5), (11, 15),
                   (2, 15), (6, 20), (9, 10)],
                "2": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                "5": [(0, 15), (4, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)],
                  "6": [(0, 15), (3, 20), (7, 5), (10, 15),
                   (2, 15), (5, 20), (9, 10)]
                }

master_key = 3 # Cmajor

# list the name and note alphabet position for each progression
# (scale_position e.g. "5" chord in 2-5-1,
# alphabet_deviation_from_root e.g. 7 semitones from root,
# chord_name e.g. "Dom7"

progression251 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7")] # ii-V-1
progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]  # 6-ii-V-1

progression = progression1625

print(len(progression))

print(f"1625 in key of {note_alphabet[master_key]}")

for pos in progression:
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
        print(f'\t {pos[0]} chord {chord_root}{pos[2]} in master key {note_alphabet[master_key]}  = {chord_note}, with weighting {chordtone[1]}%')

