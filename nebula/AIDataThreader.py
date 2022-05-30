# import python libs
from threading import Thread

# import project libs
from sound.audio_control import AudioEngine
from nebula.nebula import NebulaDataEngine


class AIData:
    """start all the data threading
     pass it the master signal class for emmission"""

    def __init__(self, ai_signal_obj, harmony_signal):
        self.ai_signal = ai_signal_obj
        self.harmony_signal = harmony_signal

        # instantiate the AI server
        nebula_engine = NebulaDataEngine(self.ai_signal, self.harmony_signal, speed=1)

        # instantiate the controller client and pass AI engine
        audio_engine = AudioEngine(nebula_engine)

        # declares all threads
        t1 = Thread(target=nebula_engine.make_data)
        t2 = Thread(target=nebula_engine.affect)
        t3 = Thread(target=audio_engine.snd_listen)

        # assigns them all daemons
        t1.daemon = True
        t2.daemon = True

        # starts them all
        t1.start()
        t2.start()
        t3.start()



