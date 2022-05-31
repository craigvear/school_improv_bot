from dataclasses import dataclass
import config

"""a dataclass containing all the harmonic language
and harmonic decision made by the AI"""

@dataclass
class Harmony:
    """Current harmony data"""

    chord_name: str = "none"
    """current chord name"""

    note: str = "none"
    """name chosen note"""

    bar: int = 0
    """bar position"""

    prog_pos: int = 0
    """position in harmonic progression"""

    root_name: str = "none"
    """root name of current chord in harmonic progression"""

    root_number: str = "none"
    """number of the root in relation to note alphabet"""

    progression: str = config.harmonic_prog
    """the harmonic progression of the session"""

    bpm: int = config.bpm
    """tempo in bpm"""

    key: str = config.master_key
    """Master key of whole session"""

# alphabet of tuples (fluidsynth note name, brown note name)
note_alphabet = [("A", "a"), ("Bb", "bf"), ("B", "b"),
                 ("C", "c"), ("C#", "cs"), ("D", "d"),
                 ("Eb", "ef"), ("E", "e"), ("F", "f"),
                 ("F#", "fs"), ("G", "g"), ("G#", "gs")]

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

# list the name and note alphabet position for each progression
progression = {"2511": [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")],
               "1625": [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")],
               "3625": [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
               }

