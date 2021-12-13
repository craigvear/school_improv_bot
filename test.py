from brown.common import *
import PyQt5
import os
from random import randrange

chord = [(0, 15), (11, 15), (4, 20), (2, 15), (9, 10), (6, 20), (7, 5)]
staff_unit = 8
first_note_offset = staff_unit / 2

def remove(obj):
    """Remove a GraphicObject from the document"""
    if (obj.parent):
        obj.parent.children.remove(obj)

brown.setup()

number_of_loops = 3

for _n in range(number_of_loops):
    number_of_notes = randrange(2, 6)
    print(f'IMAGE MAKER: number_of_notes == {number_of_notes}')

    manuscript_width = (number_of_notes + 1) * staff_unit # + first_note_offset
    print(f'manuscript width = {manuscript_width}')

    # create coordinate space container
    flow = Flowable((Mm(0), Mm(0)), Mm(manuscript_width), Mm(30))

    # generate a staff in the container
    # staff = Staff((Mm(0), Mm(0)), Mm(100), flow, Mm(1))
    staff = Staff((Mm(0), Mm(0)), Mm(manuscript_width), flow, Mm(1))

    # populate it with music furniture
    # todo get ket and current chord from harmony_dict
    Clef(staff, Mm(0), 'treble')
    KeySignature(Mm(0), staff, 'af_major')

    # todo get current chord from harmony_dict
    Text((Mm(3), staff.unit(-2)), 'af_major')

    note_list = ["c", "f", "d"]
    print('note list = ', note_list)

    for n in range(number_of_notes):
    # for n, note in enumerate(note_list):
        # use the 2nd part of note alphabet tuple
        note = note_list[n % 3]
        printed_note = note + "'"

        printed_note_pos = first_note_offset + ((n + 1) * staff_unit)

        print(f"position for {printed_note} is {printed_note_pos}")

        print(f'printed note  ===== {printed_note}')
        cr = Chordrest(Mm(printed_note_pos), staff, ["c,", printed_note], Beat(1, 4))
        # Chordrest(Mm(printed_note_pos), staff, ["c"], Beat(1, 4))

    brown.show()
    # cr.remove()

    flow.remove()

# number_of_notes = 5 # random.randrange(1, 5)
# print (number_of_notes)
#
# flow = Flowable((Mm(0), Mm(0)), Mm(20), Mm(30))
# # staff = Staff((Mm(0), Mm(0)), Mm(20), flowable)
# staff = Staff((Mm(0), Mm(0)), Mm((number_of_notes + 1) * 10), flow, Mm(1))
#
# upper_staff_clef = Clef(staff, Mm(0), 'treble')
# upper_staff_key_signature = KeySignature(Mm(0), staff, 'af_major')
#
# chord_name = 'BbMaj9'
# # sfz = Dynamic.sfz((Mm(10), staff.unit(6)), staff)
#
#
# clef = Clef(staff, Mm(0), 'treble')
# text = Text((Mm(3), staff.unit(-2)), chord_name)
# # musictext = MusicText(staff, Mm(1), 'G')
# # note1 = Notehead(Mm(10), "g'", (1, 2), staff)
# # line = Stem(100, 30, staff)
# note1 = Chordrest(Mm(10), staff, ["c'"], Beat(2, 4))
# note2 = Chordrest(Mm(20), staff, ["a'", "bs"], Beat(2, 4))
#
#
# note3 = Chordrest(Mm(30), staff, ["a'", "bs"], Beat(2, 4))
# note4 = Chordrest(Mm(40), staff, ["a'", "bs"], Beat(2, 4))
#
# note5 = Chordrest(Mm(50), staff, ["a'", "bs"], Beat(2, 4))
#
# slur = Slur((Mm(0), Mm(0), note1),
#             (Mm(0), Mm(0), note5))
#
# image_path = os.path.join(os.path.dirname(__file__), 'vtests/output',
#                            'vtest_image.png')
# brown.render_image((Mm(0), Mm(0), Inch(2), Inch(2)), image_path,
#                    bg_color=Color(0, 120, 185, 0),
#                    autocrop=True)
#
#
#
# #
# # brown.show()