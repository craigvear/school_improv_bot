from dataclasses import dataclass
import config

"""a dataclass containing all the harmonic language
and harmonic decision made by the AI"""

@dataclass
class NebulaData:
    """Current harmony data"""

    move_rnn = 0

    affect_rnn = 0

    move_affect_conv2 = 0

    affect_move_conv2 = 0

    master_output = 0

    user_in = 0

    rnd_poetry = 0

    rhythm_rnn = 0

    affect_net = 0

    self_awareness = 0

    affect_decision = 0

    rhythm_rate = 0.1

    width = 0

    height = 0



# name list for nets
netnames = ['move_rnn',
                 'affect_rnn',
                 'move_affect_conv2',
                 'affect_move_conv2',
                 'self_awareness',  # Net name for self-awareness
                 'master_output']  # input for self-awareness

# names for affect listening
affectnames = ['user_in',
                    'rnd_poetry',
                    'affect_net',
                    'self_awareness']