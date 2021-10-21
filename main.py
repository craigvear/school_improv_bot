import concurrent.futures
from threading import Thread


from controller import Client
from ai import AiDataEngine


class Gui:
    # todo Fabrizio - some kind of face gesture
    #  triggered by robot movement

    def __init__(self, cl):
        # robot_data = cl.data_exchange
        pass


def main():
    # # lis of task for concurrency
    # tasks = [engine.make_data,
    #          engine.affect,
    #          cl.snd_listen,
    #          cl.data_exchange,
    #          cl.robot_sax] # add Gui to this list
    #
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futures = {executor.submit(task): task for task in tasks}

    t1 = Thread(target=engine.make_data)
    t2 = Thread(target=engine.affect)
    t3 = Thread(target=cl.snd_listen)
    t4 = Thread(target=cl.data_exchange)
    t5 = Thread(target=cl.sound_bot)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()


if __name__ == '__main__':
    # instantiate the AI server
    engine = AiDataEngine()

    # instantiate the controller client and pass AI engine
    cl = Client(engine)

    # instantiate GUI and pass it the cl object for data coordination
    gui = Gui(cl)

    # set the ball rolling
    main()

