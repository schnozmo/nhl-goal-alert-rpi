#!/bin/bash

dir="/home/pi/nhl/2019-2020"
sched_file="SeasonSchedule-20192020.json"
sched_url="http://live.nhl.com/GameData/$sched_file"
curl $sched_url -o $dir/$sched_file 2> /dev/null
cat $dir/$sched_file  | sed 's/},/|/g' | tr '|' '\n'  | tr -d '[\[\]{}"]' | sed 's/[a-z]\{1,3\}://g' | tr ' ' '.' | tr -d : > $dir/$sched_file.csv
