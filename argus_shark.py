import glob
import os

print("Operating on CSV files")

for filename in glob.glob('*.csv'):
	print(filename)
	dest = filename.split('.')[0]
	with open(f'{dest}_tcp_flows.txt', 'w') as tf:
		with open(os.path.join(os.getcwd(), filename), 'r') as f:
			print(f.readline())

			for line in f.readlines():
				spl = line.split(',')
				start = float(spl[0])
				end = start + float(spl[1])
				if 'tcp' in line:
					tf.write(f"{start},{end}\n")


