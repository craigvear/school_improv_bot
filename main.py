import concurrent.futures
from threading import Thread

# from visuals import main as gui
from controller import Client
from ai import AiDataEngine


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
    # t6 = Thread(target=gui)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    # t6.start()


if __name__ == '__main__':
    # instantiate the AI server
    engine = AiDataEngine(speed=1)

    # instantiate the controller client and pass AI engine
    cl = Client(engine)

    # instantiate Gui and pass AI engine
    # gui = Gui(engine)

    # set the ball rolling
    main()

