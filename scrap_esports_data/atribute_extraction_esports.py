import json

#convert scrapped data to attributes by only using information that was given to us before some given match
SIDES = ['blue', 'red']
R_SIDES = ['relative']
LANES = ['top', 'jungle', 'mid', 'adc', 'support']
TEAM_META = ['name']
TEAM_ATTRIBUTES = ['win ratio', 'blue win ratio', 'red win ratio','avg. win game length','avg. lose game length']
PLAYER_ATTRIBUTES = ['kda ratio',  'cs/min', 'kill participation', 'champion winrate']
NON_PREFIX_PER_PLAYER_ATTRIBUTES = ['global champion winrate']
TOTAL_ATR = (len(SIDES)*(len(TEAM_META) + 2*(len(TEAM_ATTRIBUTES)+len(LANES)*len(PLAYER_ATTRIBUTES))))
CLASS_ATTRIBUTE = 'winner'

file = open('esports.tab', 'w')
#headers
for team in SIDES:
    for t_meta in TEAM_META:
        file.write(team + ' ' +t_meta + '\t')
#we'll all have attributes for entire split and recent matches separately
for team in R_SIDES:
    for prefix in ['', 'recent ', 'head to head ']:
        for t_atr in TEAM_ATTRIBUTES:
            file.write(prefix + team + ' ' +t_atr + '\t')
        for lane in LANES:
            for p_atr in PLAYER_ATTRIBUTES:
                file.write(prefix + team + ' ' + lane + ' ' + p_atr + '\t')
    for lane in LANES:
        for np_atr in NON_PREFIX_PER_PLAYER_ATTRIBUTES:
            file.write(team + ' ' + lane + ' ' + np_atr + '\t')

file.write(CLASS_ATTRIBUTE + '\n')

with open('kr_items.json') as data_file:
    data = json.load(data_file)

#quick helper
def write_attribute(file,attribute):
    file.write(str(attribute) + '\t')

def update_global_champion_winrate(match):
    global global_champion_winrate
    for side in SIDES:
        for lane in LANES:
            champion = match[side][lane]['champion']
            if champion not in global_champion_winrate:
                global_champion_winrate[champion] = [0,0]
            global_champion_winrate[champion][0] += 1
            if match['winner'] == side:
                global_champion_winrate[champion][1] += 1

def calculate_attributes_from_history(team_name, team_champions, team_history, team_values):
    #TEAM_ATR
    wins = {'red':0,'blue':0}
    games_count = dict(wins)
    win_duration=lose_duration=0
    #PLAYER_ATR
    kda = {lane : 0 for lane in LANES}
    gold_min = dict(kda)
    cs_min = dict(kda)
    kill_participation = dict(kda)
    champion_winrate = {lane : [0,0] for lane in LANES}
    for h_match in team_history:
        h_side = 'blue' if h_match['blue']['name'] == team_name else 'red'
        games_count[h_side] += 1
        is_winner = h_match['winner'] == h_side
        if is_winner:
            wins[h_side] += 1
            win_duration += h_match['length']
        else:
            lose_duration += h_match['length']

        total_kills = sum([h_match[h_side][lane]['kills'] for lane in LANES])
        total_kills = float(total_kills) if total_kills>0 else 1
        for lane in LANES:
            h_lane = h_match[h_side][lane]
            deaths = float(h_lane['deaths']) if h_lane['deaths']>0 else 1
            kills_assists = h_lane['kills'] + h_lane['assists']

            kda[lane] += kills_assists/deaths
            #gold_min[lane] += h_lane['gold']/float(h_match['length'])
            cs_min[lane] += h_lane['cs']/float(h_match['length'])
            kill_participation[lane] += kills_assists/total_kills

            if h_lane['champion'] == team_champions[lane]:
                champion_winrate[lane][0] += 1
                if is_winner:
                    champion_winrate[lane][1] += 1


    history_size = float(len(team_history))
    #set some default values in special cases
    if len(team_history)==0:
        history_size = 2.0
        for s in wins:
            wins[s] = 0.5


    #team attrs - win ratio, sides win_ratio, avg win duration, avg lose duration
    team_values.append(sum(wins.values())/history_size)
    for s in wins:
        g_count = float(games_count[s]) if games_count[s] > 0 else 1
        team_values.append(wins[s]/g_count)
    team_values.append(win_duration/history_size)
    team_values.append(lose_duration/history_size)

    #player attrs
    for lane in LANES:
        team_values.append(kda[lane]/history_size)
        #team_values.append(gold_min[lane]/history_size)
        team_values.append(cs_min[lane]/history_size)
        team_values.append(kill_participation[lane]/history_size)

        #default winrate should be 50%
        champion_winrate[lane] = champion_winrate[lane] if champion_winrate[lane][0]>0 else [2,1]
        team_values.append(champion_winrate[lane][1]/float(champion_winrate[lane][0]))

def write_attributes(values, match, file, relative = False):
    #meta
    for side in SIDES:
        write_attribute(file, match[side]['name'])

    if not relative:
        for side in SIDES:
            for value in values[side]:
                write_attribute(file, value)
    else:
        for i in range(len(values[SIDES[0]])):
            write_attribute(file, values[SIDES[0]][i]-values[SIDES[1]][i])

    file.write(match['winner'] + '\n')

#first sort matches oldest to newset
data.sort(key=lambda x:x['timestamp'])
team_history = dict()
global_champion_winrate = dict()
for match in data:
    skip_this_match = False
    #first pass just to see if we have enough of teams history already
    for side in SIDES:
        team_name = match[side]['name']
        if team_name not in team_history:
            team_history[team_name] = list()
        if len(team_history[team_name])<15:
            skip_this_match = True
        team_history[team_name].append(match)

    if skip_this_match:
        update_global_champion_winrate(match)
        continue

    values = dict()
    #get history for head to head matchups
    t1,t2 = [match[side]['name'] for side in SIDES]
    head_to_head_h = [m for m in team_history[t1][:-1] if m['blue']['name']==t2 or m['red']['name']==t2]

    #we have enough history data for this match
    for side in SIDES:
        values[side] = list()
        team_name = match[side]['name']

        #current champions extraction before calculating history
        team_champions = dict()
        for lane in LANES:
            team_champions[lane] = match[side][lane]['champion']

        #all avalilable hisotry - we exclude last match since it's this one
        calculate_attributes_from_history(team_name, team_champions , team_history[team_name][:-1], values[side])
        #recent history - last 2 matches
        calculate_attributes_from_history(team_name, team_champions, team_history[team_name][-5:-1], values[side])
        #head to head history
        calculate_attributes_from_history(team_name, team_champions, head_to_head_h , values[side])

        for lane in LANES:
            #default value
            champion_winrate = 0.5
            if team_champions[lane] in global_champion_winrate:
                champion_winrate = global_champion_winrate[team_champions[lane]]
                champion_winrate = champion_winrate[1]/float(champion_winrate[0])

            values[side].append(champion_winrate)

    write_attributes(values, match, file, relative=True)

    update_global_champion_winrate(match)