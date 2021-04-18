#!/bin/bash

for filename in 18-10-*.pcap; do
	python pcap.py $filename
done
