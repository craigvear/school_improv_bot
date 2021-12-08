import glob
import random
from operator import itemgetter
from PyQt5.QtGui import QImage, QPainter

MAX_SIZE = 500
MAX_LIFESPAN = 100

class ProcessVisuals:
    def __init__(self):

        self.queue = []
        self.visual_types = ("line",
                             "ellipse",
                             "rect",
                             "image")

        # todo - replace temp content.
        #  Currently 2-5-1 images taken from https://www.jazzguitar.be/blog/ii-v-i-jazz-guitar-licks/
        self.external_images = [QImage(image_to_load) for image_to_load in glob.glob("images/*.png")]

        self.image_composition_modes = (QPainter.CompositionMode_HardLight,
                                        QPainter.CompositionMode_Difference,
                                        QPainter.CompositionMode_ColorBurn,
                                        QPainter.CompositionMode_ColorDodge,
                                        QPainter.CompositionMode_Multiply,
                                        QPainter.CompositionMode_SoftLight)

    def add_to_queue(self, ai_signal_dict):
        # if len(self.queue) < 10:
        self.process_AI_signal(ai_signal_dict)

    def process_AI_signal(self, ai_signal_dict):
        # print("processing signal")

        master_output, rhythm_rate, width, height = itemgetter("master_output",
                                                             "rhythm_rate",
                                                             "width",
                                                             "height")(ai_signal_dict)


        final_visual = dict(type=random.choice(self.visual_types),
                            lifespan=self.lifespan(rhythm_rate),
                            color={"r": random.randint(0, 255),
                                   "g": random.randint(0, 255),
                                   "b": random.randint(0, 255),
                                   "a": random.randint(0, 255)},
                            image=random.randint(0, len(self.external_images) - 1),
                            image_transparency=random.random(),
                            image_composition_mode=random.choice(self.image_composition_modes),
                            pen=random.randint(1, MAX_SIZE),
                            size=random.randint(1, MAX_SIZE),
                            position={"x": random.randint(0, width),
                                      "y": random.randint(0, height)},
                            direction=random.randint(1, 11),
                            zoom=random.randrange(1, 4))

        # print(final_visual)
        self.queue.append(final_visual)
        # print('length of queue = ', len(self.queue))

    def lifespan(self, rate):
        lifespan = rate * random.randint(10, 100)
        if lifespan < 0:
            lifespan *= -1
        while lifespan > MAX_LIFESPAN:
            lifespan /= random.randint(2, 10)

        # print('////////////////             lifespan = ', lifespan)
        return int(lifespan)

    def update_queue(self):
        if len(self.queue):
            for i, val in enumerate(self.queue):
                lifespan = val["lifespan"] - 1
                # if not lifespan:
                if lifespan <= 0:
                    del self.queue[i]

                else:
                    self.queue[i]["lifespan"] = lifespan
                    direction = self.queue[i]["direction"]
                    if direction == 0:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 1
                    elif direction == 1:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 1
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 1
                    elif direction == 2:
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 1
                    elif direction == 3:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 1
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 1
                    elif direction == 4:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 1
                    elif direction == 5:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 1
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 1
                    elif direction == 6:
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 1
                    elif direction == 7:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 1
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 1
                    elif direction >= 10:
                        if bool(random.getrandbits(1)):
                            if bool(random.getrandbits(1)):
                                self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 1
                            else:
                                self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 1
                        else:
                            if bool(random.getrandbits(1)):
                                self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 1
                            else:
                                self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 1
