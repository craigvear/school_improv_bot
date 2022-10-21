from mingus.containers import *
from mingus.midi import fluidsynth
from time import sleep
from random import randrange

SF2 = "sound/soundfontGM.sf2"
fluidsynth.init(SF2)



fluidsynth.set_instrument(0, 1)
fluidsynth.set_instrument(1, 35)

# play_note(26, 0, 127)



def play_note(note_to_play_list):



    # dynamic = 90 + randrange(1, 30)
    fluidsynth.play_NoteContainer(nc=note_to_play_list)


# play_note(Note(note_name, octave), dynamic)


# for n in range(10):
#     rnd_n




play_note([Note(name="C",
               octave=4,
               channel=0,
               velocity=127),
           Note(name="E",
               octave=4,
               channel=0,
               velocity=127),
           Note(name="G",
               octave=4,
               channel=0,
               velocity=127)
          ]
          )
sleep(1)
# play_note(26, 1, 127)
# sleep(1)
