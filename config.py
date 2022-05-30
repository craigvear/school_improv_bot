"""Harmonic parameters

note_alphabet (called 0-11) = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#"]

list the name and note alphabet position for each progression
progression2511 = [("2", 2, "min7"), ("5", 7, "Dom9"), ("1", 0, "Maj7"), ("1", 0, "Maj7")]
progression1625 = [("1", 0, "Maj7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
progression3625 = [("3", 4, "min7"), ("6", 9, "min7"), ("2", 2, "min7"), ("5", 7, "Dom9")]
"""
# what is the key?
master_key = 3 # 3 = C

# which progression?
harmonic_prog = "1625"

# what tempo?
bpm=100

# what time sig?
time_sig = 4

# instrumental transposition?
transposition = 0

"""Style parameters"""
temperature = 1
density = 1
colour = 1

"""Robot parameters"""
# robot connected?
robot_connected = False

arm_connected = False
