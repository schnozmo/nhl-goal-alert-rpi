#!/bin/bash

export PATH="${PATH}:/home/pi/nhl"

# pull the schedule file once per day
now=`date "+%Y%m%d.%H%M%S"`
if [[ `echo $now | cut -d. -f2 | cut -c1-4` == "0800" ]]
then
    pull-sched-file.bash
fi

dir="/home/pi/nhl/score-check-tmp"
lock_file=$dir/lock_file
if [[ -e $lock_file ]]; then
    echo "Process already running"
    exit
fi

touch $lock_file

sched_file="/home/pi/nhl/2019-2020/SeasonSchedule-20192020.json.csv"


get-near-games.py $sched_file > $dir/games-near.csv

if [[ `wc -l < $dir/games-near.csv` -eq "0" ]]; then
    rm $lock_file
    exit
fi

for l in `cat $dir/games-near.csv`; do
    id=`echo $l | cut -d, -f1`
    date=`echo $l | cut -d, -f2 | cut -c1-8`
    ateam=`echo $l | cut -d, -f3`
    hteam=`echo $l | cut -d, -f4`

    gamedir=${dir}/${id}_${ateam}_${hteam}
    if [[ ! -d $gamedir ]]; then
        mkdir $gamedir
	touch $gamedir/alerted_scoring_eventIdx.txt
    fi
    
    game_box_url="https://statsapi.web.nhl.com/api/v1/game/$id/feed/live"
    game_box_file="$gamedir/${ateam}_${hteam}.live.json"
    curl $game_box_url -o $game_box_file 2> /dev/null

    date >> $gamedir/process.log
    process-game-json.py $game_box_file $gamedir/alerted_scoring_eventIdx.txt /home/pi/nhl/team_colors.txt /home/pi/nhl/score-check-tmp/scoring.log >> $gamedir/process.log

done

rm $lock_file

