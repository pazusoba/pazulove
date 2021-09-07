"""
Generate random training data
"""

from math import ceil
from multiprocessing import Process
from pazulove import PazuLove
import traceback, os, time

cpu_count = os.cpu_count()
data_count = int(ceil(100 / cpu_count))

def generate_data(process_number):
    try:
        # 30 for 6 x 5, 42 for 7 x 6
        soba = PazuLove(30, 8, process_number, data_count)
        soba.generate_new_data()
    except Exception as ex:
        # notify via email when crashed
        command = 'emailme "Core {} crashed" "{}"'.format(process_number, ex)
        os.system(command)
        print(traceback.format_exc())

if __name__ == '__main__':

    processes = []
    start_time = time.time()

    # seperate tasks to all cpus
    for i in range(cpu_count):
        processes.append(Process(target=generate_data, args=(i,)))

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    # notify via email when completed, only works on certain devices
    command = 'emailme "DATA GENERATION COMPLETED" "{} core(s), {} per core, took {}s"'.format(cpu_count, data_count, time.time() - start_time)
    print(command)
    os.system(command)
