"""Harmonic parameters

note_alphabet (called 0-11) = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]

list the name and note alphabet position for each progression
progression2511 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")]
progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
progression3625 = [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
"""
# what is the key: 3 = C?
master_key: int = 3

# which progression?
harmonic_prog: str = "2511"

# what tempo?
bpm: float = 120
bpm_to_ms = ((60 / bpm) * 1000)

# what time sig of /4?
time_sig: int = 4

# subdivision of beat
# 3 = triplet quavers, 6 = trip semi
subdivision: int = 3

# instrumental transposition (for notation)?
transposition: int = 0

"""Style parameters"""
# crazyness value for AI response:
# 0.1 is slow and cool, 1 is hot and spicy
temperature: float = 0.5

# style of jazz response from AI
# 0.1 is cool / model, 1 is bebop / experimental
colour: float = 0.5

"""Robot parameters"""
robot_connected: bool = False

# [HARDWARE]
robot = False
eeg = False
eeg_graph = False

# [BITALINO]
baudrate = 100
channels = [0]
mac_address = "/dev/cu.BITalino-3F-AE"

# [DEBUG]
# debug = logging.INFO

# [STAFF]
staff_width = 20

# [STREAMING]
stream_list = ['mic_in',
               'rnd_poetry',
               'move_rnn',
               'affect_rnn',
               'self_awareness']

# todo - CRAIG if this is false then the "feeding" NNets need to be operting too
all_nets_predicting = True
