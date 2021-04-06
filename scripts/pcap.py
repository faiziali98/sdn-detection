import pyshark
from copy import deepcopy
import glob
import os
import sys

filename = str(sys.argv[1])

print("Operating on PCAP files")

# for filename in glob.glob('*.pcap'):
print(filename)
cap = pyshark.FileCapture(filename)

start = 0
end = 0

check_point = 1

epochs = []
flows = set([])

stats = {
	'count': 0,
	'avergae_packet_size': 0,
	'syn_packets': 0,
	'synack_packets': 0,
	'ack_packets': 0,
	'data_packets': 0,
	'total_bytes': 0,
	'flow_count': 0
}

tot = 0

dest = filename.split('.')[0]

f = open(f"{dest}_stats.txt", "w")
f.write("start,end,count,avergae_packet_size,syn_packets,synack_packets,ack_packets,data_packets,total_bytes,flow_count\n")

for pkt in cap:
	
	if 'TCP' in pkt:
		if start == 0 or float(pkt.sniff_timestamp) > end:
			if start != 0:
				stats['avergae_packet_size'] = stats['total_bytes']//stats['count']
				stats['flow_count'] = len(flows)
				to_write = [str(start), str(end)]
				flows = set([])

				for key in stats.keys():
					to_write.append(str(stats[key]))
					stats[key] = 0
				f.write(','.join(to_write))
				f.write('\n')

			if start==0:
				start = float(pkt.sniff_timestamp)
			else:
				start = end
			end = start + 10

			tot += 1

			if tot % 100 == 0:
				tot = 0
				f.close()
				f = open(f"{dest}_stats.txt", "a")

		stats['count'] += 1

		try:
			source_address = pkt.ip.src
			source_port = pkt.tcp.srcport
			destination_address = pkt.ip.dst
			destination_port = pkt.tcp.dstport
			flows.add(f'{source_address}_{destination_address}_{source_port}_{destination_port}')
		except:
			print("error")

		if pkt.tcp.flags == '0x00000012':
			stats['synack_packets'] += 1
		elif pkt.tcp.flags == '0x00000002':
			stats['syn_packets'] += 1
		elif pkt.tcp.flags == '0x00000010':
			stats['ack_packets'] +=1 

		if len(pkt.layers) > 3:
			stats['data_packets'] +=1 

		stats['total_bytes'] += int(pkt.length)



to_write = [str(start), str(end)]
for key in stats.keys():
	to_write.append(str(stats[key]))
f.write(','.join(to_write))
f.write('\n')

f.close()

