#!/usr/bin/bash

for ticket in ./tickets/*.png; do
    output_name=`basename $ticket .png`
    python ticketbuild.py -t $ticket -o tickets/$output_name.pdf -u 580 -w 1160 -x 390 -y 138 -z 72 -n 450
done

echo "ALL DONE!"
