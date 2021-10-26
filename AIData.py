# import python libs
from threading import Thread

# import project libs
from controller import Client
from ai import AiDataEngine


class AIData:
    """start all the data threading
     pass it the master signal class for emmission"""

    def __init__(self, ai_signal_obj):
        self.ai_signal = ai_signal_obj

        self.final_data = {}

        # instantiate the AI server
        engine = AiDataEngine(self.ai_signal, speed=1)

        # instantiate the controller client and pass AI engine
        cl = Client(engine)

        # declares all threads
        t1 = Thread(target=engine.make_data)
        t2 = Thread(target=engine.affect)
        t3 = Thread(target=cl.snd_listen)
        t4 = Thread(target=cl.data_exchange)
        t5 = Thread(target=cl.sound_bot)

        # assigns them all daemons
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True

        # starts them all
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()

