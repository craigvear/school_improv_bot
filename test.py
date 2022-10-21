import mingus
from mingus.midi import fluidsynth
from time import sleep

SF2 = "sound/soundfontGM.sf2"
fluidsynth.init(SF2)



fluidsynth.set_instrument(0, 1)
fluidsynth.set_instrument(1, 35)

fluidsynth.play_Note(26, 0, 127)
sleep(1)
fluidsynth.play_Note(26, 1, 127)
sleep(1)



# def play_note(self, note_to_play, dynamic):
#     """play_note determines the coordinates of a note on the keyboard image
#     and sends a request to play the note to the fluidsynth server"""
#
#     # dynamic = 90 + randrange(1, 30)
#     fluidsynth.play_Note(note=note_to_play, channel=self.channel, velocity=dynamic)
#     print(f'\t\t\t\t\tplaying {note_to_play}, channel {self.channel}, velocity {dynamic}')
#
#
# play_note(Note(note_name, octave), dynamic)


