from brown.common import *
import PyQt5
import os
import random



brown.setup()

number_of_notes = 5 # random.randrange(1, 5)
print (number_of_notes)

flow = Flowable((Mm(0), Mm(0)), Mm(20), Mm(30))
# staff = Staff((Mm(0), Mm(0)), Mm(20), flowable)
staff = Staff((Mm(0), Mm(0)), Mm((number_of_notes + 1) * 10), flow, Mm(1))

upper_staff_clef = Clef(staff, Mm(0), 'treble')
upper_staff_key_signature = KeySignature(Mm(0), staff, 'af_major')

chord_name = 'BbMaj9'
# sfz = Dynamic.sfz((Mm(10), staff.unit(6)), staff)


clef = Clef(staff, Mm(0), 'treble')
text = Text((Mm(3), staff.unit(-2)), chord_name)
# musictext = MusicText(staff, Mm(1), 'G')
# note1 = Notehead(Mm(10), "g'", (1, 2), staff)
# line = Stem(100, 30, staff)
note1 = Chordrest(Mm(10), staff, ["c'"], Beat(2, 4))
note2 = Chordrest(Mm(20), staff, ["a'", "bs"], Beat(2, 4))


note3 = Chordrest(Mm(30), staff, ["a'", "bs"], Beat(2, 4))
note4 = Chordrest(Mm(40), staff, ["a'", "bs"], Beat(2, 4))

note5 = Chordrest(Mm(50), staff, ["a'", "bs"], Beat(2, 4))

slur = Slur((Mm(0), Mm(0), note1),
            (Mm(0), Mm(0), note5))

image_path = os.path.join(os.path.dirname(__file__), 'vtests/output',
                           'vtest_image.png')
brown.render_image((Mm(0), Mm(0), Inch(2), Inch(2)), image_path,
                   bg_color=Color(0, 120, 185, 0),
                   autocrop=True)



#
# brown.show()