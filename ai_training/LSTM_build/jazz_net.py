import tensorflow as tf
import numpy as np
import random
import tensorflow as tf
import pickle
import pretty_midi
from tqdm import tqdm
from numpy.random import choice
import numpy as np
import csv
import random
from datetime import datetime
from music21 import stream, converter, clef, meter
from data.nautilusTraining import SeqSelfAttention

model = tf.keras.models.load_model('model_ep4.h5', custom_objects=SeqSelfAttention.get_custom_objects())
note_tokenizer  = pickle.load( open( "tokenizer(1).p", "rb" ) )


# load the trained model
self.model = tf.keras.models.load_model('data/epochs4-long-model_ep4.h5',
                                   custom_objects=SeqSelfAttention.get_custom_objects())

with open("data/epochs4-long-tokenizer.p", "rb") as t:
    self.note_tokenizer = pickle.load(t)
