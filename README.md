# nhl-goal-alert-rpi
Poll NHL live data and display goal alerts on raspberry pi Sense HAT. Try it out and let me know what additions you made!

How it works
------------
The script 'check-for-scores.bash' runs every minute by cron job on the Raspberry Pi. This script determines whether there are any current NHL games and, if there are, pulls the live data from the NHL JSON data feeds. The JSON data for each current game is examined for any goals were scored since the last check. If there are, the details are written to a raspberry pi Sense HAT 8x8 LED screen in the colors of the team that scored.

Known issues
------------
- the season values are hard-coded :(
- NHL will sometimes update old goals with new values, which look like a new goal was scored.

Cron entry
----------

`* * * * *     check-for-scores.bash`
