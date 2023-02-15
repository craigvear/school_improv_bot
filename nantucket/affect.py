# install python modules
import sys
import os
from time import time, sleep
from random import randrange, getrandbits, random
import logging

# import project modules
from nantucket.hivemind import DataBorg
from sound.player import Player
import config

class Affect:
    """Feels the music and datastreams and
    """

    def __init__(self,
                 ai_signal_obj,
                 # harmony_signal,
                 # duration_of_piece: int = 120,
                 # continuous_line: bool = True,
                 speed: int = 5,
                 # staves: int = 1,
                 # pen: bool = True
                 ):

        # set global path
        sys.path.insert(0, os.path.abspath('.'))

        # own the dataclass
        self.hivemind = DataBorg()

        # start operating vars
        # self.duration_of_piece = duration_of_piece
        # self.continuous_line = continuous_line
        self.running = True
        self.old_value = 0
        self.local_start_time = time()
        # self.end_time = self.start_time + duration_of_piece
        # self.pen = pen

        # calculate the inverse of speed
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        self.global_speed = ((speed - 1) * (0.1 - 1) / (10 - 1)) + 1
        print(f'user def speed = {speed}, global speed = {self.global_speed}')

        # own the signal object for emission
        self.ai_signal = ai_signal_obj
        # self.harmony_signal = harmony_signal

        # own the sound bot object and send harmony emitter
        # self.soundbot = Bot(self.harmony_signal)
        self.player = Player() #self.harmony_signal)

    def gesture_manager(self):
        """Listens to the realtime incoming signal that is stored in the dataclass ("mic_in")
        and calculates an affectual response based on general boundaries:
            HIGH - if input stream is LOUD (0.8+) then emit, smash a random fill and break out to Daddy cycle...
            MEDIUM - if input energy is 0.3-0.8 then emit, a jump out of child loop
            LOW - nothing happens, continues with cycles
        """

        # names for affect listening
        stream_list = config.stream_list
        stream_list_len = len(stream_list)
        # little val for emission control avoiding repeated vals
        self.old_val = 0

        while self.running:
            # flag for breaking a phrase from big affect signal
            self.hivemind.interrupt_bang = True

            #############################
            # Phrase-level gesture gate: 3 - 8 seconds
            #############################
            # todo CRAIG calls the robot arm to do different modes
            # todo CRAIG global speed and self-awareness stretch
            # calc rhythmic intensity based on self-awareness factor & global speed
            intensity = self.hivemind.self_awareness
            logging.debug(f'////////////////////////   intensity =  {intensity}')

            phrase_length = (randrange(300, 800) / 100) # + self.global_speed
            phrase_loop_end = time() + phrase_length

            logging.debug('\t\t\t\t\t\t\t\t=========AFFECT - Daddy cycle started ===========')
            logging.debug(f"                 interrupt_listener: started! Duration =  {phrase_length} seconds")

            while time() < phrase_loop_end:
                print('================')

                # if a major break out then go to Daddy cycle and restart
                if not self.hivemind.interrupt_bang:
                    print("-----------------------------INTERRUPT----------------------------")
                    break

                # todo - CRAIG sort this out. think Intensity needs to be inversed!!
                # generate rhythm rate here
                self.rhythm_rate = (randrange(10,
                                         80) / 100) #* self.global_speed


                # rhythm_rate = self.rhythm_rate * intensity #) / self.global_speed
                #
                # # self.rhythm_rate = self.rhythm_rate / self.global_speed
                self.hivemind.rhythm_rate = self.rhythm_rate
                logging.info(f'////////////////////////   rhythm rate = {self.rhythm_rate}')
                logging.debug('\t\t\t\t\t\t\t\t=========Hello - child cycle 1 started ===========')

                ##################################################################
                # choose thought stream from data streams from Nebula/ live inputs
                ##################################################################

                # randomly pick an input stream for this cycle
                # either mic_in, random, net generation or self-awareness
                rnd = randrange(stream_list_len)
                rnd_stream = stream_list[rnd]
                self.hivemind.thought_train_stream = rnd_stream
                logging.info(f'Random stream choice = {rnd_stream}')
                print(self.hivemind.thought_train_stream)

                #############################
                # Rhythm-level gesture gate: .5-2 seconds
                # THis streams the chosen data
                #############################
                # todo CRAIG add global time stretch here (from self awareness)
                # rhythmic loop 0.5-2 (or 1-4) secs, unless interrupt bang
                rhythm_loop = time() + (randrange(500, 2000) / 1000)
                logging.debug(f'end time = {rhythm_loop}')

                while time() < rhythm_loop:
                    logging.debug('\t\t\t\t\t\t\t\t=========Hello - baby cycle 2 ===========')

                    # make the master output the current value of the affect stream
                    # 1. go get the current value from dict
                    thought_train = getattr(self.hivemind, rnd_stream)
                    logging.info(f'######################           Affect stream output {rnd_stream} == {thought_train}')

                    # 2. send to Master Output
                    # setattr(self.hivemind, 'master_stream', thought_train)
                    self.hivemind.master_stream = thought_train

                    # emit data
                    # self.emitter(thought_train)
                    logging.info(f'\t\t ==============  thought_train output = {thought_train}')

                    # 3. modify speed and accel through self awareness
                    # # todo CRAIG this should be decided in line with self.awareness
                    # calc rhythmic intensity based on self-awareness factor & global speed
                    self_awareness = getattr(self.hivemind, 'self_awareness')
                    logging.debug(f'////////////////////////   self_awareness =  {self_awareness}')

                    ######################################
                    #
                    # Makes a response to chosen thought stream
                    #
                    ######################################

                    # todo - sort out robot mode here

                    if thought_train > 0.7:
                        logging.info('interrupt > HIGH !!!!!!!!!')

                        # A - refill dict with random
                        self.hivemind.randomiser()

                        # B - jumps out of this loop into daddy
                        self.hivemind.interrupt_bang = False

                        # C - emit
                        self.emitter(thought_train)

                        # D- break out of this loop, and next (cos of flag)
                        break

                    # MEDIUM
                    # if middle loud fill dict with random, all processes norm
                    elif 0.1 < thought_train < 0.7:
                        logging.info('interrupt MIDDLE -----------')

                        # emit
                        self.emitter(thought_train)

                        # A. jumps out of current local loop, but not main one
                        break

                    # LOW
                    # nothing happens here
                    elif thought_train <= 0.1:
                        logging.info('interrupt LOW -----------')

                    # and wait for a cycle
                    sleep(self.rhythm_rate)

        logging.info('quitting gesture manager thread')


    def emitter(self, incoming_emission):
        if incoming_emission != self.old_val:
            emission_dict = {}
            emission_dict["emission_data"] = incoming_emission
            emission_dict["rhythm_rate"] = self.rhythm_rate

            self.ai_signal.ai_str.emit(str(emission_dict))
            print('//////////////////                   EMITTING and making sound')

            # send make sound signal to piano
            self.player.note_to_play(emission_dict)

        self.old_val = incoming_emission


    # def mid_energy_response(self, peak):
    #     (x, y, z, r, j1, j2, j3, j4) = self.drawbot.pose()
    #     logging.debug(f'Current position: x:{x} y:{y} z:{z} j1:{j1} j2:{j2} j3:{j3} j4:{j4}')
    #
    #     """between 2 and 8 make shapes in situ"""
    #     # randomly choose from the following c hoices
    #     randchoice = randrange(6)
    #     logging.debug(f'randchoice == {randchoice}')
    #
    #     # 0= line to somewhere
    #     if randchoice == 0:
    #         self.drawbot.bot_move_to(x + self.rnd(peak),
    #                              y + self.rnd(peak),
    #                              z, 0,
    #                              False)
    #         logging.info('Emission 3-8: draw line')
    #
    #     # 1 = messy squiggles
    #     if randchoice == 1:
    #         squiggle_list = []
    #         for n in range(randrange(2, 4)):
    #             squiggle_list.append((randrange(-5, 5) / 5,
    #                                   randrange(-5, 5) / 5,
    #                                   randrange(-5, 5) / 5)
    #                                  )
    #         self.drawbot.squiggle(squiggle_list)
    #         logging.info('Emission 3-8: small squiggle')
    #
    #     # 2 = dot & line
    #     elif randchoice == 2:
    #         self.drawbot.dot()
    #         self.drawbot.bot_move_to(x + self.rnd(peak),
    #                              y + self.rnd(peak),
    #                              z, 0,
    #                              False)
    #         logging.info('Emission 3-8: dot')
    #
    #     # 3 = note head
    #     elif randchoice == 3:
    #         note_size = randrange(5)
    #         # note_shape = randrange(20)
    #         self.drawbot.note_head(size=note_size)
    #         logging.info('Emission 3-8: note head')
    #
    #     # 4 = note head and line
    #     elif randchoice == 4:
    #         note_size = randrange(1, 10)
    #         self.drawbot.note_head(size=note_size)
    #         self.drawbot.bot_move_to(x + self.rnd(peak),
    #                              y + self.rnd(peak),
    #                              z, 0,
    #                              False)
    #         logging.info('Emission 3-8: note head and line')
    #
    #     # 5 = dot
    #     elif randchoice == 5:
    #         self.drawbot.dot()
    #         # self.move_y_random()
    #         logging.info('Emission 3-8: dot and line')
    #
    # def high_energy_response(self):
    #     """move to a random x, y position"""
    #     self.drawbot.clear_commands()
    #     self.drawbot.move_y_random()

    def terminate(self):
        """Smart collapse of all threads and comms"""
        print('TERMINATING')
        self.drawbot.home()
        self.drawbot.close()
        self.running = False

    def rnd(self, power_of_command: int) -> int:
        """Returns a randomly generated + or - integer,
        influenced by the incoming power factor"""
        pos = 1
        if getrandbits(1):
            pos = -1
        result = (randrange(1, 5) + randrange(power_of_command)) * pos
        logging.debug(f'Rnd result = {result}')
        return result
