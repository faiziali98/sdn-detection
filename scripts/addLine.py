import glob
import os
import sys
from shutil import move

for filename in glob.glob('./stats/*.txt'):
        print(filename)
        dest = filename.split('.')[0]
        with open(f'temp_{dest}.txt', 'w') as wf:
                with open(filename, 'r') as f:
                        first = f.readline()
                        if 'start' not in first:
                                wf.write("start,end,count,avergae_packet_size,syn_packets,synack_packets,ack_packets,data_packets,total_bytes,flow_count\n")
                        wf.write(first)

                        for l in f.readlines():
                                wf.write(l)

        os.remove(filename)
        move(f'temp_{dest}.txt', filename)
