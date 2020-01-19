#!/usr/bin/python3

import json, sys, time
from sense_hat import SenseHat

sense = SenseHat()
sense.set_rotation(180)
sense.low_light = True

if len(sys.argv) != 5:
    print("Problem with arguments: " + sys.argv[0] + " <json_file> <alerted_scoring_file> <color_file> <scoring_log>")
    sys.exit(-1)

exe, game_json_file, alerted_scoring_file, color_file, scoring_log_file = sys.argv

team_colors = {}
color_fh = open(color_file, 'r')
for l in color_fh:
    team, bg, fg = l.rstrip('\r\n').split('|')
    team_colors[team] = [tuple([int(a) for a in bg.split(',')]), 
                         tuple([int(a) for a in fg.split(',')])]
color_fh.close()

alerted_fh = open(alerted_scoring_file, 'r')
alerted_ids = [int(l.rstrip('\r\n')) for l in alerted_fh]
alerted_fh.close()

game_json = json.loads(open(game_json_file, 'r').read())
home_team = game_json['gameData']['teams']['home']['triCode']
away_team = game_json['gameData']['teams']['away']['triCode']
#home_colors = team_colors[home_team]
#away_colors = team_colors[away_team]
#print(home_team, home_colors, away_team, away_colors)


scoring_plays = game_json['liveData']['plays']['scoringPlays']
unalerted_ids = []
for sp in scoring_plays:
    if sp in alerted_ids:
        continue
    else:
        unalerted_ids.append(sp)
        
def blink(c1, c2):
    map1 = [c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, 
            c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, 
            c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, 
            c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1, c1] 
    map2 = [c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2,
            c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2,
            c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2,
            c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2, c2]
    sense.set_pixels(map1)
    time.sleep(0.25)
    sense.set_pixels(map2)
    time.sleep(0.25)
    sense.set_pixels(map1)
    time.sleep(0.25)
    sense.set_pixels(map2)
    time.sleep(0.25)
    sense.set_pixels(map1)
    time.sleep(0.25)
    sense.set_pixels(map2)
    time.sleep(0.25)
    sense.clear()

def draw_goal(x, y):
    bl = [10, 10, 10]
    wh = [240, 240, 240]
    bu = [30, 30, 200]
    goal_map = [bl, bl, bl, bl, bl, bl, bl, bl,
                bl, bl, bl, wh, wh, bl, bl, bl,
                bl, bl, bl, bl, bl, bl, bl, bl,
                bl, bl, bl, bl, bl, bl, bl, bl,
                bl, bl, bl, bl, bl, bl, bl, bl,
                bl, bl, bl, bl, bl, bl, bl, bl,
                bu, bu, bu, bu, bu, bu, bu, bu,
                bl, bl, bl, bl, bl, bl, bl, bl]
    
    if x < 0:
        x *= -1
        y *= -1
        
    row = -1
    col = -1
    if x < 25:
        row = 7
    elif x > 89:
        row = 0
    else:
        # x range = 25-89 -> 6-1
        mod_x = x * -1 + 89
        # mod_x range = 64-0 -> 6-1
        row = int(float(mod_x) * 5 / 52)
        
    # y range = -42.5-42.5 -> 7-0
    mod_y = y * -1 + 42.5
    # mod_y range = 85-0 -> 7-0
    col = max(7, int(float(mod_y)/85)*8)
    
    goal_pixel = 8*row + col
    
    sense.set_pixels(goal_map)
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(wh))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(bl))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(wh))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(bl))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(wh))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(bl))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(wh))
    time.sleep(0.25)
    sense.set_pixel(row, col, tuple(bl))
    time.sleep(0.25)
    sense.clear()


for sp_idx in unalerted_ids:
    sp_json = game_json['liveData']['plays']['allPlays'][sp_idx]

    desc = sp_json['result']['description']

    goal_time = sp_json['about']['dateTime']
    scoring_team = sp_json['team']['triCode']
    home_goals = sp_json['about']['goals']['home']
    away_goals = sp_json['about']['goals']['away']
    pd = sp_json['about']['ordinalNum']
    pd_time = sp_json['about']['periodTime']

    msg = scoring_team + " -> " + desc + " (" + away_team + " " + str(away_goals) + ":" + str(home_goals) + " " + home_team + ") @ " + pd_time + "/" + pd + " (" + goal_time + ")\n"

    print(scoring_team, team_colors[scoring_team][0], tuple(team_colors[scoring_team][0]))
    
    scoring_log_fh = open(scoring_log_file, 'a')
    scoring_log_fh.write(msg)
    scoring_log_fh.close()

    blink(team_colors[scoring_team][0], team_colors[scoring_team][1])
    sense.show_message(msg,
                       text_colour = tuple(team_colors[scoring_team][1]),
                       back_colour = tuple(team_colors[scoring_team][0]),
                       scroll_speed = 0.03)
    sense.clear()

    alerted_app_fh = open(alerted_scoring_file, 'a')
    alerted_app_fh.write(str(sp_idx) + "\n")
    alerted_app_fh.close()
    
    
