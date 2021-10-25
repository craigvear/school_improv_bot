import glob
import random
from operator import itemgetter

from PySide2.QtGui import QImage, QPainter

MAX_SIZE = 500
MAX_LIFESPAN = 250


class ProcessOscSignal:
    def __init__(self):
        self.queue = []
        self.visual_types = ("line",
                             "ellipse",
                             "rect",
                             "image")

        self.external_images = [QImage(image_to_load) for image_to_load in glob.glob("images/*.png")]

        self.image_composition_modes = (QPainter.CompositionMode_HardLight,
                                        QPainter.CompositionMode_Difference,
                                        QPainter.CompositionMode_ColorBurn,
                                        QPainter.CompositionMode_ColorDodge,
                                        QPainter.CompositionMode_Multiply,
                                        QPainter.CompositionMode_SoftLight)

    def add_to_queue(self, osc_signal_dict):
        axisa = osc_signal_dict["axisa"]
        axisb = osc_signal_dict["axisb"]

        if (axisa < -0.2 or axisa > 0.2 or axisb < 0.2 or axisb > 0.2) and len(self.queue) < 10:
            self.process_osc_signal(osc_signal_dict)

    def process_osc_signal(self, osc_signal_dict):
        # print("processing signal")

        axisa, axisb, mlx, mly, kinx, kinz, width, height = itemgetter("axisa",
                                                                       "axisb",
                                                                       "mlx",
                                                                       "mly",
                                                                       "kinx",
                                                                       "kinz",
                                                                       "width",
                                                                       "height")(osc_signal_dict)

        final_visual = dict(type=random.choice(self.visual_types),
                            lifespan=self.lifespan(axisa, axisb, mlx, mly, kinx, kinz),
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
                            direction=random.randint(0, 11))

        self.queue.append(final_visual)

    def lifespan(self, a, b, c, d, e, f):
        lifespan = a + b + c + d + e + f
        if lifespan < 0:
            lifespan *= -1
        while lifespan > MAX_LIFESPAN:
            lifespan /= random.randint(2, 10)
        return int(lifespan)

    def update_queue(self):
        if len(self.queue):
            for i, val in enumerate(self.queue):
                lifespan = val["lifespan"] - 1
                if not lifespan:
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
