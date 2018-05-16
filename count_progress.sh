#!/bin/bash

for d in `ls -d {jan,feb,march,april,may,june,july,aug,sept,oct,nov,dec}_*_url/`; do
	ls "$d" | wc -l | sed "s/$/ $d";
done | column -t | sort -n


