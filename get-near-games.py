#!/usr/bin/python3

import sys
from datetime import datetime as dt

if len(sys.argv) != 2:
    print("Problem with arguments: " + sys.argv[0] + " <sched_file>")
    sys.exit(-1)

exe, sched_file = sys.argv

now = dt.now()

sched_fh = open(sched_file, 'r')
for l in sched_fh:
    gid, gt, ateam, hteam = l.rstrip('\r\n').split(',')
    gt_dt = dt.strptime(gt, "%Y%m%d.%H%M%S")
    seconds_ago = (now - gt_dt).total_seconds()

    # game starts in < 1 hour or started < 4 hours ago
    if seconds_ago > -3600 and seconds_ago < 4*3600:
        print(l.rstrip('\r\n'))

sched_fh.close()
