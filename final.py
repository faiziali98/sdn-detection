import os
from shutil import move
import glob

from_prev_epoch = []
last_line = []

epoch_flows = 0

print("Operating on ALL files")

filenames = ['18-06-09.pcap', '18-05-29.pcap', '18-10-12.pcap', '18-05-30.pcap']

for filename in filenames:
	print(filename)
	dest = filename.split('.')[0]
	with open(f'temp_{dest}.txt', 'w') as wf:
		with open(f'{dest}_stats.txt', 'r') as f:
			with open(f'{dest}_tcp_flows.txt', 'r') as tf:
				f.readline()
				wf.write(f.readline())
				for line in f.readlines():
					line = line.strip()
					spl = line.split(',')
					start = float(spl[0])
					end = float(spl[1])
					last_line.sort(key=lambda tup: tup[0])

					for strt, ended in last_line:
						if strt>=start and ended<=end:
							epoch_flows += 1
							last_line.remove((strt, ended))
						else:
							if strt>= start and strt < end:
								epoch_flows += 1
							elif ended > start and ended<=end:
								epoch_flows += 1
								last_line.remove((strt, ended))

					l2 = tf.readline()

					while l2:
						spl2 = l2.split(',')

						strt = float(spl2[0])
						ended = float(spl2[1])

						if strt>=start and ended<end:
							epoch_flows += 1
						else:
							if strt>= start and strt < end:
								epoch_flows += 1
							wf.write(','.join(spl[:9]+[str(epoch_flows)]))
							wf.write('\n')
							
							last_line.append((strt, ended))
							epoch_flows = 0
							break
					
						l2 = tf.readline()

		os.remove(f'{dest}_stats.txt')
		move(f'temp_{dest}.txt', f'{dest}_stats.txt')
