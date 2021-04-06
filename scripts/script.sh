#!/bin/bash

for filename in *.argus; do
	name="${filename%.*}"
	ra -u -s +1dur dur, proto -c ',' -r $filename > "$name.csv"
done

