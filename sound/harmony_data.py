from dataclasses import dataclass

"""a dataclass containing all the harmonic language
and harmonic decision made by the AI"""

class HarmonyBorg:
    __hivemind = None

    def __init__(self):
        if not HarmonyBorg.__hivemind:
            HarmonyBorg.__hivemind = self.__dict__
            """Current harmony data"""

            self.chord_shape_list: list = []
            """current chord shape dict"""

            self.chord_name: str = "none"
            """current chord name"""

            self.chord_shape: str = "none"
            """current chord name"""

            self.note: str = "none"
            """name chosen note"""

            self.bar: int = 0
            """bar position"""

            self.prog_pos: int = 0
            """position in harmonic progression"""

            self.root_name: str = "c"
            """root name of current chord in harmonic progression"""

            self.root_number: int = 3
            """number of the root in relation to note alphabet"""

        else:
            self.__dict__ = HarmonyBorg.__hivemind





# alphabet of tuples (fluidsynth note name, Neoscore note name)
note_alphabet = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]

# note_alphabet = [("A", "a"), ("Bb", "bf"), ("B", "b"),
#                  ("C", "c"), ("C#", "cs"), ("D", "d"),
#                  ("Eb", "ef"), ("E", "e"), ("F", "f"),
#                  ("F#", "fs"), ("G", "g"), ("G#", "gs")]

# chord types are 1: tonic Maj7; 2: minor 7th; 4: sub dom maj7; 5: dom 7th etc
# todo change these to chord shape names e.g. "maj7", "Dom7"
# todo add extra field for modal distortions e.g. A harmonic minor = E Phrygian dominant?????
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
# dict inside dicts for gears and weights of differnt chord shapes
# e.g. "Maj7" has 2 arrays for gears 1 (major chord tones), gear 2 (lydian + whole tone)
chord_shapes = {"Maj7": [[(0, 20), (4, 40), (7, 10), (11, 30)],
                         [(0, 15), (4, 20), (7, 5), (11, 15),
                          (2, 15), (6, 20), (9, 10)]
                         ],
                "min7": [[(0, 20), (3, 40), (7, 10), (10, 30)],
                         [(0, 15), (3, 20), (7, 5), (10, 15),
                          (2, 15), (5, 20), (9, 10)]
                         ],
                "Dom9": [[(0, 15), (4, 35), (7, 5), (10, 20), (2, 25)],
                         [(0, 15), (4, 20), (7, 5), (10, 15),
                          (2, 15), (5, 20), (9, 10)],
                         ],
                "min7b5": [[(0, 20), (3, 40), (6, 10), (10, 30)],
                         [(0, 15), (3, 20), (6, 5), (10, 15),
                          (2, 15), (5, 20), (8, 10)] # todo - check this!!!
                           ]
}


# list the name and note alphabet position for each progression
# format: chord shape, note alphabet for root, description
# todo change to root of chord (from tonic); shape (e.g Maj7), slash bass note (from root??), modal shift??
# progression = {"2511": [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")],
#                "1625": [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")],
#                "3625": [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")],
#                "1362": [("1", 0, "Maj7"), ("3", 4, "Dom7"), ("6", 9, "Dom7"), ("2", 2, "min7")],
#                "all of me": [("1", 0, "Maj7"), ("5", 4, "Dom7"), ("5", 9, "Dom7"), ("2", 2, "min7"),
#                              ("5", 4, "Dom7"), ("2", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
#                }
# format = name of progression (key): [(root of chord), chord shape, bass substitute,
# advanced harmony scales for each gear
progression = {"2511": [(2, "min7", None, [None, None]),
                            (7, "Dom9", None, [None, None]),
                            (0, "Maj7", None, [None, None]),
                            (0, "Maj7", None, [None, None])
                            ],
                   "2511tritone": [(2, "min7", None, [None, None]),
                            (7, "Dom9", 1, [None, None]),
                            (0, "Maj7", None, [None, None]),
                            (0, "Maj7", None, [None, None])
                            ],
                   "2511min": [(2, "min7b5", None, [None, None]),
                            (7, "Dom9", None, [None, None]),
                            (0, "min7", None, [None, None]),
                            (0, "min7", None, [None, None])
                            ],
                   "all of me": [(0, "Maj7", None, [(0, "maj"), (0, "maj")]),
                                 (4, "Dom9", None, [None, None]),
                                 (9, "Dom9", None, [None, None]),
                                 (2, "min7", None, [None, None]),
                                 (4, "Dom9", None, [None, None]),
                                 (9, "min7", None, [None, None]),
                                 (2, "min7", None, [None, None]),
                                 (7, "Dom9", None, [None, None])
                                 ]
                   }

# todo - calculate a scale based on key harmonic info such as parent, mode, master key etc

