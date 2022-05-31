# import python libs
from threading import Thread
import trio

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
        self.nebula_engine = NebulaDataEngine(self.ai_signal, self.harmony_signal, speed=1)

        # instantiate the controller client and pass AI engine
        self.audio_engine = AudioEngine(self.nebula_engine)

        trio.run(self.flywheel)
        print('I got here daddy')


    async def flywheel(self):
        print("parent: started!")
        async with trio.open_nursery() as nursery:

            # spawning affect listener and master clocks
            print("parent: spawning affect listener and clocks ...")
            nursery.start_soon(self.audio_engine.snd_listen)

            # spawning all the data making
            print("parent: spawning affect module")
            nursery.start_soon(self.nebula_engine.affect)

            # spawning affect listener and master clocks
            print("parent: spawning making data ...")
            nursery.start_soon(self.nebula_engine.make_data)



        #
        #
        # # declares all threads
        # t1 = Thread(target=nebula_engine.make_data)
        # t2 = Thread(target=nebula_engine.affect)
        # t3 = Thread(target=audio_engine.snd_listen)
        #
        # # assigns them all daemons
        # t1.daemon = True
        # t2.daemon = True
        #
        # # starts them all
        # t1.start()
        # t2.start()
        # t3.start()



