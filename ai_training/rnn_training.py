import collections
import datetime
# import fluidsynth
import glob
import numpy as np
import pathlib
import pandas as pd
import pretty_midi
# import seaborn as sns
import tensorflow as tf

"""https://www.tensorflow.org/tutorials/audio/music_generation"""

# declare variables
seed = 42
tf.random.set_seed(seed)
np.random.seed(seed)
data_dir = pathlib.Path('data/maestro-v2.0.0')
key_order = ['pitch', 'step', 'duration']
seq_length = 25
vocab_size = 128
epochs = 5

filenames = glob.glob(str(data_dir/'**/*.mid*'))
print('Number of files:', len(filenames))

def midi_to_notes(midi_file: str) -> pd.DataFrame:
  pm = pretty_midi.PrettyMIDI(midi_file)
  instrument = pm.instruments[0]
  notes = collections.defaultdict(list)

  # Sort the notes by start time
  sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
  prev_start = sorted_notes[0].start

  for note in sorted_notes:
    start = note.start
    end = note.end
    notes['pitch'].append(note.pitch)
    notes['start'].append(start)
    notes['end'].append(end)
    notes['step'].append(start - prev_start)
    notes['duration'].append(end - start)
    prev_start = start

  return pd.DataFrame({name: np.array(value) for name, value in notes.items()})

# def notes_to_midi(
#   notes: pd.DataFrame,
#   out_file: str,
#   instrument_name: str,
#   velocity: int = 100,  # note loudness
# ) -> pretty_midi.PrettyMIDI:
#
#   pm = pretty_midi.PrettyMIDI()
#   instrument = pretty_midi.Instrument(
#       program=pretty_midi.instrument_name_to_program(
#           instrument_name))
#
#   prev_start = 0
#   for i, note in notes.iterrows():
#     start = float(prev_start + note['step'])
#     end = float(start + note['duration'])
#     note = pretty_midi.Note(
#         velocity=velocity,
#         pitch=int(note['pitch']),
#         start=start,
#         end=end,
#     )
#     instrument.notes.append(note)
#     prev_start = start
#
#   pm.instruments.append(instrument)
#   pm.write(out_file)
#   return pm

def create_training_dataset():
    """Create the training dataset by extracting notes from the MIDI files.
    You can start by using a small number of files, and experiment later with more."""
    num_files = 5
    all_notes = []
    for f in filenames[:num_files]:
        notes = midi_to_notes(f)
        all_notes.append(notes)

    all_notes = pd.concat(all_notes)

    n_notes = len(all_notes)
    print('Number of notes parsed:', n_notes)

    # Next, create a tf.data.Dataset from the parsed notes.
    # key_order = ['pitch', 'step', 'duration']
    train_notes = np.stack([all_notes[key] for key in key_order], axis=1)

    notes_ds = tf.data.Dataset.from_tensor_slices(train_notes)
    # notes_ds.element_spec

    # create sequences
    # seq_length = 25
    # vocab_size = 128
    seq_ds = create_sequences(notes_ds, seq_length, vocab_size)
    # seq_ds.element_spec

    for seq, target in seq_ds.take(1):
        print('sequence shape:', seq.shape)
        print('sequence elements (first 10):', seq[0: 10])
        print()
        print('target:', target)

    batch_size = 64
    buffer_size = n_notes - seq_length  # the number of items in the dataset
    train_ds = (seq_ds
                .shuffle(buffer_size)
                .batch(batch_size, drop_remainder=True)
                .cache()
                .prefetch(tf.data.experimental.AUTOTUNE))

    return train_ds
    # train_ds.element_spec

def create_sequences(
        dataset: tf.data.Dataset,
        seq_length: int,
        vocab_size = 128,
        ) -> tf.data.Dataset:
    """Returns TF Dataset of sequence and label examples."""
    seq_length = seq_length+1

    # Take 1 extra for the labels
    windows = dataset.window(seq_length, shift=1, stride=1,
                              drop_remainder=True)

    # `flat_map` flattens the" dataset of datasets" into a dataset of tensors
    flatten = lambda x: x.batch(seq_length, drop_remainder=True)
    sequences = windows.flat_map(flatten)

    # Normalize note pitch
    def scale_pitch(x):
        x = x/[vocab_size,1.0,1.0]
        return x

    # Split the labels
    def split_labels(sequences):
        inputs = sequences[:-1]
        labels_dense = sequences[-1]
        labels = {key:labels_dense[i] for i,key in enumerate(key_order)}

        return scale_pitch(inputs), labels

    return sequences.map(split_labels, num_parallel_calls=tf.data.AUTOTUNE)

# Create and train the model

def mse_with_positive_pressure(y_true: tf.Tensor, y_pred: tf.Tensor):
  mse = (y_true - y_pred) ** 2
  positive_pressure = 10 * tf.maximum(-y_pred, 0.0)
  return tf.reduce_mean(mse + positive_pressure)

def train():
    input_shape = (seq_length, 3)
    learning_rate = 0.005

    inputs = tf.keras.Input(input_shape)
    x = tf.keras.layers.LSTM(128)(inputs)

    outputs = {
        'pitch': tf.keras.layers.Dense(128, name='pitch')(x),
        'step': tf.keras.layers.Dense(1, name='step')(x),
        'duration': tf.keras.layers.Dense(1, name='duration')(x),
    }

    model = tf.keras.Model(inputs, outputs)

    loss = {
        'pitch': tf.keras.losses.SparseCategoricalCrossentropy(
            from_logits=True),
        'step': mse_with_positive_pressure,
        'duration': mse_with_positive_pressure,
    }

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    model.compile(loss=loss, optimizer=optimizer)

    model.summary()

    losses = model.evaluate(train_ds, return_dict=True)
    # losses

    model.compile(
        loss=loss,
        loss_weights={
            'pitch': 0.05,
            'step': 1.0,
            'duration': 1.0,
        },
        optimizer=optimizer,
    )

    model.evaluate(train_ds, return_dict=True)

    # Train the model.
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath='./training_checkpoints/ckpt_{epoch}',
            save_weights_only=True),
        tf.keras.callbacks.EarlyStopping(
            monitor='loss',
            patience=5,
            verbose=1,
            restore_best_weights=True),
    ]

    history = model.fit(
        train_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    print("saving model")
    model.save(f"rnn_seqlen{seq_length}_vocabsize{vocab_size}_epochs{epochs}/model.h5")


if __name__ == "__main__":
    # training
    train_ds = create_training_dataset()
    train()



