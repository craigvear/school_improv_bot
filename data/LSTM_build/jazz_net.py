import tensorflow as tf
import numpy as np
import random

model = tf.keras.models.load_model('data/models/exp5_model_human20_16len_ep1068-acc0.5773.h5')

input_val = random.random()
input_val = np.reshape(input_val, (1, 1, 1))
input_val = tf.convert_to_tensor(input_val,  np.float32)


pred1 = model.predict(input_val)

print(pred1)

