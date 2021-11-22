from time import time, sleep

# state BPM
bpm = 80
time_sig = 3

# convert bar and beat to ms
bpm_to_ms = ((60 / bpm) * 1000)
# bar_pulse = bpm_to_ms * time_sig

# print (f'tempo = {bpm}, tim sig = {time_sig}')
# print (f'bar tempo in ms = {bar_pulse}, beat in ms = {bpm_to_ms}')

# start the clock
# start_time = time()
# print(start_time)

# start the counting process
bar = 1
beat = 1
tick = 0

while True:
    tick += 1
    print(f'doin stuff - BAR BEAT TICK {bar}, {beat}, {tick}')

    if tick >= 12:
        beat += 1
        tick = 0

    if beat > time_sig:
        bar += 1
        beat = 1


    # sleep in 12 divisions of a beat
    sleep_dur = (bpm_to_ms / 12) / 1000
    sleep(sleep_dur)

