import random
from operator import itemgetter
from PyQt5.QtGui import QPainter
import os

# import project modules
from visuals.neoscore_generator import ImageGen

MAX_SIZE = 500
MAX_LIFESPAN = 200 # 20 seconds
MIN_LIFESPAN = 10 # 1 second

class ProcessVisuals:
    def __init__(self):

        self.queue = []
        self.visual_types = ("line",
                             "ellipse",
                             "rect"
                             "image",
                             "image")
                             # "complex")

        # todo - add complex (breathe) type image
        # todo - add a note (from pre-mades) into centre of each ellipse, rect

        # instantiate image generator class
        self.image_gen = ImageGen()

        # self.external_images = [QImage(image_to_load) for image_to_load in glob.glob("images/*.png")]

        self.image_composition_modes = (QPainter.CompositionMode_HardLight,
                                        QPainter.CompositionMode_Difference,
                                        QPainter.CompositionMode_ColorBurn,
                                        QPainter.CompositionMode_ColorDodge,
                                        QPainter.CompositionMode_Multiply,
                                        QPainter.CompositionMode_SoftLight)

    def add_to_queue(self, ai_signal_dict): #, harmony_dict):
        if len(self.queue) < 10:
            # print(f'\t\t\t\t\t ADDING PAINT EVENT TO QUEUE')
            self.process_AI_signal(ai_signal_dict) #, harmony_dict)

    def process_AI_signal(self, ai_signal_dict): #, harmony_dict):
        # print("processing signal")
        emission_data, rhythm_rate, width, height = itemgetter("emission_data",
                                                             "rhythm_rate",
                                                             "width",
                                                             "height")(ai_signal_dict)

        image_type = random.choice(self.visual_types)

        if image_type == "image":
            generated_image = self.image_gen.make_image() #harmony_dict)
            # print('generated_image_path')
            # generated_image = random.randint(0, len(self.external_images) - 1)
        else:
            generated_image = 0

        # if image_type == "complex":
        #     image_type = random.choice(self.visual_types[:3])

        final_visual = dict(type=image_type,
                            lifespan=self.lifespan(rhythm_rate * 10),
                            color={"r": random.randint(0, 255),
                                   "g": random.randint(0, 255),
                                   "b": random.randint(0, 255),
                                   "a": random.randint(0, 255)},
                            image=generated_image,
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
        elif lifespan > MAX_LIFESPAN:
            lifespan = MAX_LIFESPAN
        elif lifespan < MIN_LIFESPAN:
            lifespan = MIN_LIFESPAN

        # print('////////////////             lifespan = ', lifespan)
        return int(lifespan)

    def update_queue(self):
        if len(self.queue):
            for i, val in enumerate(self.queue):
                lifespan = val["lifespan"] - 1
                # if not lifespan:
                if lifespan <= 0:
                    # if event is an image: remove .png from folder
                    if self.queue[i]["type"] == 'image':
                        # print("DDDDDDDEEEEEELLLLLLLLEEEEEEEETTTTTTTEEEEEEEEEE")
                        os.remove(self.queue[i]["image"])
                    del self.queue[i]


                else:
                    self.queue[i]["lifespan"] = lifespan
                    direction = self.queue[i]["direction"]
                    move_factor = random.randrange(1, 20)
                    if direction == 0:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 10
                    elif direction == 1:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 10
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 10
                    elif direction == 2:
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 10
                    elif direction == 3:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 10
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + 10
                    elif direction == 4:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 10
                    elif direction == 5:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + 10
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 10
                    elif direction == 6:
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 10
                    elif direction == 7:
                        self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - 10
                        self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - 10
                    elif direction >= 10:
                        if bool(random.getrandbits(1)):
                            if bool(random.getrandbits(1)):
                                self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] - move_factor
                            else:
                                self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] - move_factor
                        else:
                            if bool(random.getrandbits(1)):
                                self.queue[i]["position"]["x"] = self.queue[i]["position"]["x"] + move_factor
                            else:
                                self.queue[i]["position"]["y"] = self.queue[i]["position"]["y"] + move_factor
