import zipfile
from tools import load_obj
import os.path
import sys
import itertools

#Constant that tells us whether to use relative or absolute attributes
RELATIVE_ATTRS = True
BLUE = 100
RED = 200
LEAGUE_TIER_TO_SCORE = {'BRONZE':0.0,'SILVER':1.0,'GOLD':2.0,'PLATINUM':3.0,'DIAMOND':4.0,'MASTER':5.0,'CHALLENGER':6.0}

#first pass through the composition data to obtain champion winrates.
compositions = open('data_composition.tab','r')
champion_ids = [int(atr_name.split(' ')[2]) for atr_name in compositions.readline().split('\t')[2:-1]]
champion_ids = champion_ids[:len(champion_ids)/2]
composition_to_winrate = dict()
#this is for skipping certain datas
composition_match_ids = list()
#skip 2 rows
compositions.readline()
compositions.readline()

for line in compositions:
    split_line = line.split('\t')
    composition_match_ids.append(int(split_line[0].strip()))
    comp = {'blue':[],'red':[]}
    for i, champ in enumerate(split_line[2:-1]):
        if int(champ) == 1:
            side = 'blue' if i<len(champion_ids) else 'red'
            champion_id = champion_ids[i%len(champion_ids)]
            comp[side].append(champion_id)

    winner = split_line[-1].strip('\n')
    for side in comp:
        win = 1 if side==winner else 0
        comp[side].sort()
        for r in range(1,6):
            combinations = itertools.combinations(comp[side], r)
            for c in combinations:
                if c not in composition_to_winrate:
                    composition_to_winrate[c] = [0,0]
                composition_to_winrate[c][0] += 1
                composition_to_winrate[c][1] += win
composition_match_ids = set(composition_match_ids)

read_files = 2080
if read_files == 0:
    data_file = open("data.tab","w")
    if RELATIVE_ATTRS:
        data_file.write("num pulled summoners\tr KDA\tr win ratio\tr r. games played\tr. minion kills/game\tr. n.m. kills/game\tr. turrets killed\tr. gold earned/game\tr. demage dealt ratio\tr. tier\tr. previous tier\tr. num same role")
        data_file.write("\trc KDA\trc win ratio\trc r. games played\trc. minion kills/game\trc. turrets killed\trc. gold earned/game\trc. demage dealt ratio")
        data_file.write("\trr KDA\trr win ratio\trr. minion kills/min\trr. n.m. kills/min\trr. turrets killed\trr. gold earned/min\trr. wards placed/min\trr. wards killed/min\trr. kill participation\trr. damage dealt ratio")
        data_file.write("\trr 0-10 csDiffPerMinDeltas\trr 0-10 goldPerMinDeltas\trr 0-10 wardsPerMinDeltas\trr 0-10 xpDiffPerMinDeltas")
        data_file.write("\trr 10-20 csDiffPerMinDeltas\trr 10-20 goldPerMinDeltas\trr 10-20 wardsPerMinDeltas\trr 10-20 xpDiffPerMinDeltas")
        data_file.write("\trrc KDA\trrc win ratio\trrc. minion kills/min\trrc. n.m. kills/min\trrc. turrets killed\trrc. gold earned/min\trrc. wards placed/min\trrc. wards killed/min\trrc. kill participation\trrc. damage dealt ratio")
        data_file.write("\trrc 0-10 csDiffPerMinDeltas\trrc 0-10 goldPerMinDeltas\trrc 0-10 wardsPerMinDeltas\trrc 0-10 xpDiffPerMinDeltas")
        data_file.write("\trrc 10-20 csDiffPerMinDeltas\trrc 10-20 goldPerMinDeltas\trrc 10-20 wardsPerMinDeltas\trrc 10-20 xpDiffPerMinDeltas")
        data_file.write("\tr. solo champions win rate\tr. c. pair winrate\tr. c. triplet winrate\tr. c. quad winrate\tcomposition winrate")
        data_file.write("\twinner\n")
        data_file.write("c\t"*60)
        data_file.write("d\n")
        data_file.write("meta" + "\t"*60)
    else:
        data_file.write("num pulled summoners\tb KDA\tb win ratio\tb r. games played\tb. minion kills/game\tb. n.m. kills/game\tb. turrets killed\tb. gold earned/game\tb. demage dealt ratio\tb. tier\tb. previous tier\tb. num same role")
        data_file.write("\tbc KDA\tbc win ratio\tbc r. games played\tbc. minion kills/game\tbc. turrets killed\tbc. gold earned/game\tbc. demage dealt ratio")
        #for champion_id in champion_ids:
        #    data_file.write('\tb chmp {}'.format(champion_id))
        data_file.write("\tbr KDA\tbr win ratio\tbr. minion kills/min\tbr. n.m. kills/min\tbr. turrets killed\tbr. gold earned/min\tbr. wards placed/min\tbr. wards killed/min\tbr. kill participation\tbr. damage dealt ratio")
        data_file.write("\tbr 0-10 csDiffPerMinDeltas\tbr 0-10 goldPerMinDeltas\tbr 0-10 wardsPerMinDeltas\tbr 0-10 xpDiffPerMinDeltas")
        data_file.write("\tbr 10-20 csDiffPerMinDeltas\tbr 10-20 goldPerMinDeltas\tbr 10-20 wardsPerMinDeltas\tbr 10-20 xpDiffPerMinDeltas")
        data_file.write("\tbrc KDA\tbrc win ratio\tbrc. minion kills/min\tbrc. n.m. kills/min\tbrc. turrets killed\tbrc. gold earned/min\tbrc. wards placed/min\tbrc. wards killed/min\tbrc. kill participation\tbrc. damage dealt ratio\tb. champions win rate")
        data_file.write("\tbrc 0-10 csDiffPerMinDeltas\tbrc 0-10 goldPerMinDeltas\tbrc 0-10 wardsPerMinDeltas\tbrc 0-10 xpDiffPerMinDeltas")
        data_file.write("\tbrc 10-20 csDiffPerMinDeltas\tbrc 10-20 goldPerMinDeltas\tbrc 10-20 wardsPerMinDeltas\tbrc 10-20 xpDiffPerMinDeltas")
        data_file.write("\tr KDA\tr win ratio\tr r. games played\tr. minion kills/game\tr. n.m. kills/game\tr. turrets killed\tr. gold earned/game\tr. demage dealt ratio\tr. tier\tr. previous tier\tr. num same role")
        data_file.write("\trc KDA\trc win ratio\trc r. games played\trc. minion kills/game\trc. turrets killed\trc. gold earned/game\trc. demage dealt ratio")
        data_file.write("\trr KDA\trr win ratio\trr. minion kills/min\trr. n.m. kills/min\trr. turrets killed\trr. gold earned/min\trr. wards placed/min\trr. wards killed/min\trr. kill participation\trr. damage dealt ratio")
        data_file.write("\trr 0-10 csDiffPerMinDeltas\trr 0-10 goldPerMinDeltas\trr 0-10 wardsPerMinDeltas\trr 0-10 xpDiffPerMinDeltas")
        data_file.write("\trr 10-20 csDiffPerMinDeltas\trr 10-20 goldPerMinDeltas\trr 10-20 wardsPerMinDeltas\trr 10-20 xpDiffPerMinDeltas")
        data_file.write("\trrc KDA\trrc win ratio\trrc. minion kills/min\trrc. n.m. kills/min\trrc. turrets killed\trrc. gold earned/min\trrc. wards placed/min\trrc. wards killed/min\trrc. kill participation\trrc. damage dealt ratio\tr. champions win rate")
        data_file.write("\trrc 0-10 csDiffPerMinDeltas\trrc 0-10 goldPerMinDeltas\trrc 0-10 wardsPerMinDeltas\trrc 0-10 xpDiffPerMinDeltas")
        data_file.write("\trrc 10-20 csDiffPerMinDeltas\trrc 10-20 goldPerMinDeltas\trrc 10-20 wardsPerMinDeltas\trrc 10-20 xpDiffPerMinDeltas")
        #for champion_id in champion_ids:
        #    data_file.write('\tr chmp {}'.format(champion_id))

        data_file.write("\twinner\n")
        data_file.write("c\t"*111)
        data_file.write("d\n")
        data_file.write("meta" + "\t"*111)
    data_file.write("class\n")
else:
    data_file = open("data.tab","a")
    data_file.write("\n")


def get_winner(game):
    team = game['teams'][0]
    if team['teamId'] == BLUE:
        blue_team_winner = team['winner']
    else:
        blue_team_winner = not team['winner']

    if blue_team_winner:
        return BLUE
    else:
        return RED

while os.path.isfile('data/game_data_{0}.zip'.format(read_files)):
    game = load_obj('data/game_data_{0}.zip'.format(read_files))
    if not game or (game['matchVersion'][:4] != '6.10' and game['matchVersion'][:3] != '6.9'):
        print(str(read_files) + "/" + str(6000))
        read_files += 1
        continue
    m_id = game['matchId']

    #list of all atributes to be written in file
    blue_attributes = list()
    red_attributes = list()

    #map summoner ids to team_ids and summoner ids to champion ids - commonly needed
    summoner_team = dict()
    summoner_champion = dict()
    summoner_p_id = dict()

    for participant in game['participants']:
        for participantIdentity in game['participantIdentities']:
            if participant['participantId'] == participantIdentity['participantId']:
                summoner_team[participantIdentity['player']['summonerId']] = participant['teamId']
                summoner_champion[participantIdentity['player']['summonerId']] = participant['championId']
                summoner_p_id[participantIdentity['player']['summonerId']] = participant['participantId']
                break


    kda = dict()
    kda[BLUE] = 0
    kda[RED] = 0

    win_rate = dict(kda)
    r_games_played = dict(kda)
    minion_kills = dict(kda)
    n_monster_kills = dict(kda)
    turret_kills = dict(kda)
    gold_earned = dict(kda)
    demage_dealt_ratio = dict(kda)
    firstbloods = dict(kda)
    tier = dict(kda)
    previous_tier = dict(kda)
    same_role = dict(kda)

    #same attributes but only for specificly picked champion
    kda_c = dict(kda)
    win_rate_c = dict(kda)
    r_games_played_c = dict(kda)
    minion_kills_c = dict(kda)
    #n_monster_kills_c = dict(kda)
    turret_kills_c = dict(kda)
    gold_earned_c = dict(kda)
    demage_dealt_ratio_c = dict(kda)
    firstbloods_c = dict(kda)

    composition = dict()
    composition[BLUE] = []
    composition[RED] = []

    #more or less same attributes but only for the last 10 matches played before this one -> represents recent player skill
    #also contains some new attributes (becaouse more info is given) and some attributes are altered, for example: gold per game --> gold per minute. We have match duration! more useful
    kda_r = dict(kda)
    win_rate_r = dict(kda)
    minion_kills_r = dict(kda)
    n_monster_kills_r = dict(kda)
    turret_kills_r = dict(kda)
    gold_earned_r = dict(kda)

    wards_placed_r = dict(kda)
    wards_killed_r = dict(kda)
    kill_participation_r = dict(kda)
    damage_dealt_ratio_r = dict(kda)

    cs_diff_0_10_r = dict(kda)
    cs_diff_10_20_r = dict(kda)
    gold_delta_0_10_r = dict(kda)
    gold_delta_10_20_r = dict(kda)
    wards_delta_0_10_r = dict(kda)
    wards_delta_10_20_r = dict(kda)
    xp_diff_0_10_r = dict(kda)
    xp_diff_10_20_r = dict(kda)

    #same attributes but for specific champions
    kda_r_c = dict(kda)
    win_rate_r_c = dict(kda)
    minion_kills_r_c = dict(kda)
    n_monster_kills_r_c = dict(kda)
    turret_kills_r_c = dict(kda)
    gold_earned_r_c = dict(kda)
    wards_placed_r_c = dict(kda)
    wards_killed_r_c = dict(kda)
    kill_participation_r_c = dict(kda)
    damage_dealt_ratio_r_c = dict(kda)

    cs_diff_0_10_r_c = dict(kda)
    cs_diff_10_20_r_c = dict(kda)
    gold_delta_0_10_r_c = dict(kda)
    gold_delta_10_20_r_c = dict(kda)
    wards_delta_0_10_r_c = dict(kda)
    wards_delta_10_20_r_c = dict(kda)
    xp_diff_0_10_r_c = dict(kda)
    xp_diff_10_20_r_c = dict(kda)

    #we need this because sometimes data for certain summoners is corrupt and needs to be skipped
    num_summoners = dict(kda)
    #same info for champion specefic data
    num_summoners_c = dict(kda)
    num_summoners_tier = dict(kda)
    num_summoners_p_tier = dict(kda)



    #we need this so we can ignore stats that occurred during/after this match -> sometimes impossible(potentially just throw out games where we cant do that) -> need to truly evaluate model by hand at the end
    game_creation_timestamp = game['matchCreation']
    for summoner_stats in game['participantStats']:
        summoner_id = summoner_stats['summonerId']
        team_id = summoner_team[summoner_id]
        game_participant = [p for p in game['participants'] if p['participantId'] == summoner_p_id[summoner_id]][0]
        game_participant_lane = game_participant['timeline']['lane']
        game_participant_role = game_participant['timeline']['role']
        champion_id = summoner_champion[summoner_id]
        composition[team_id].append(int(champion_id))
        stats_modify_timestamp = summoner_stats['modifyDate']
        match_history_gathered = 0
        skip_this_summoner = False

        p_kda_r = p_kda_r_c = 0
        p_win_rate_r = p_win_rate_r_c = 0
        p_minion_kills_r = p_minion_kills_r_c = 0
        p_n_monster_kills_r = p_n_monster_kills_r_c = 0
        p_turret_kills_r = p_turret_kills_r_c = 0
        p_gold_earned_r = p_gold_earned_r_c = 0
        p_wards_placed_r = p_wards_placed_r_c = 0
        p_wards_killed_r = p_wards_killed_r_c =0
        p_kill_participation_r = p_kill_participation_r_c = 0
        p_damage_dealt_ratio_r = p_damage_dealt_ratio_r_c = 0

        p_cs_diff_0_10_r = p_cs_diff_0_10_r_c = 0
        p_cs_diff_10_20_r= p_cs_diff_10_20_r_c = 0
        p_gold_delta_0_10_r = p_gold_delta_0_10_r_c = 0
        p_gold_delta_10_20_r = p_gold_delta_10_20_r_c =0
        p_wards_delta_0_10_r = p_wards_delta_0_10_r_c = 0
        p_wards_delta_10_20_r = p_wards_delta_10_20_r_c = 0
        p_xp_diff_0_10_r = p_xp_diff_0_10_r_c = 0
        p_xp_diff_10_20_r = p_xp_diff_10_20_r_c = 0

        #here is where stats that need to be subtracted are gathered -> becaouse they are newer than played game
        #since we are looping through the same data we also gather data for the last 10 games summoner played before current one (attributes with _r(ecent) ending)
        total_sessions_played_s=total_assists_s=total_champion_kills_s=total_deaths_s=total_won_s=total_firstbloods_s=0
        total_minion_kills_s=total_neutral_m_s=total_turrets_killed_s=total_gold_earned_s=demage_dealt_s=demage_taken_s=0

        total_sessions_played_c_s=total_assists_c_s=total_champion_kills_c_s=total_deaths_c_s=total_won_c_s=total_firstbloods_c_s=0
        total_minion_kills_c_s=total_turrets_killed_c_s=total_gold_earned_c_s=demage_dealt_c_s=demage_taken_c_s=0


        summoner_match_history = game['participantMatchHistory'][summoner_id]
        #last 10 games before this match played with this champion
        summoner_champion_match_history = game['participantChampionMatchHistory'][summoner_id]
        summoner_match_history_roles = game['participantMatchListHistory'][summoner_id]['matches']
        #also append this game to match history so we can properly subtract it's stats
        if m_id not in [g['matchId'] for g in summoner_match_history]:
            summoner_match_history.append(game)
        for g in summoner_match_history:
            if g['matchId'] == -1:
                #match history for this summoner is corrupted
                skip_this_summoner = True
                break


            #check if we acttualy need to open another file to access this match
            if 'saved_file' in g:
                saved_file = g['saved_file']
                g = load_obj('data/game_data_{0}.zip'.format(saved_file))
                if not g:
                    skip_this_summoner = True
                    break


            #we only need stats for player with current summoner_id
            try:
                participant_id = [p['participantId'] for p in g['participantIdentities'] if p['player']['summonerId'] == summoner_id][0]
            except Exception:
                #match history for this summoner is corrupted
                skip_this_summoner = True
                break
            participant = [p for p in g['participants'] if p['participantId'] == participant_id][0]
            stats = participant['stats']
            timeline = participant['timeline']

            if g['matchCreation'] >= game_creation_timestamp and g['matchCreation'] + g['matchDuration'] < stats_modify_timestamp:
                #in this case we need to subtract stats
                total_sessions_played_s += 1
                total_assists_s += stats['assists']
                total_champion_kills_s += stats['kills']
                total_deaths_s += stats['deaths']
                if stats['winner']:
                    total_won_s += 1
                total_minion_kills_s += stats['minionsKilled']
                total_neutral_m_s += stats['neutralMinionsKilled']
                total_turrets_killed_s += stats['towerKills']
                total_gold_earned_s += stats['goldEarned']
                demage_dealt_s += stats['totalDamageDealt']
                demage_taken_s += stats['totalDamageTaken']


                if participant['championId'] == champion_id:
                    #also subtract champion specific stats
                    total_sessions_played_c_s += 1
                    total_assists_c_s += stats['assists']
                    total_champion_kills_c_s += stats['kills']
                    total_deaths_c_s += stats['deaths']
                    if stats['winner']:
                        total_won_c_s += 1
                    total_minion_kills_c_s += stats['minionsKilled']
                    total_turrets_killed_c_s += stats['towerKills']
                    total_gold_earned_c_s += stats['goldEarned']
                    demage_dealt_c_s += stats['totalDamageDealt']
                    demage_taken_c_s += stats['totalDamageTaken']

            elif g['matchCreation'] < game_creation_timestamp and match_history_gathered<10:
                game_duration_min = g['matchDuration']/60.0
                deaths = stats['deaths'] if stats['deaths']!=0 else 1
                p_kda_r += ((stats['assists'] + stats['kills'])/deaths)
                if stats['winner']:
                    p_win_rate_r += 1
                p_minion_kills_r += (stats['minionsKilled']/game_duration_min)
                p_n_monster_kills_r += (stats['neutralMinionsKilled']/game_duration_min)
                p_turret_kills_r += stats['towerKills']
                p_gold_earned_r += (stats['goldEarned']/game_duration_min)
                p_wards_placed_r += (stats['wardsPlaced']/game_duration_min)
                p_wards_killed_r += (stats['wardsKilled']/game_duration_min)
                total_team_kills = sum([p['stats']['kills'] for p in g['participants'] if p['teamId'] == participant['teamId']])
                total_team_kills = total_team_kills if total_team_kills>0 else 1
                p_kill_participation_r += (stats['kills'] + stats['assists'])/float(total_team_kills)
                p_damage_dealt_ratio_r += stats['totalDamageDealtToChampions']/float(stats['totalDamageDealtToChampions']+stats['totalDamageTaken']+0.1)

                #participant timelane data
                try:
                    p_cs_diff_0_10_r += timeline['csDiffPerMinDeltas']['zeroToTen']
                    p_gold_delta_0_10_r += timeline['goldPerMinDeltas']['zeroToTen']
                    #p_wards_delta_0_10_r += timeline['wardsPerMinDeltas']['zeroToTen']
                    p_xp_diff_0_10_r += timeline['xpDiffPerMinDeltas']['zeroToTen']
                except KeyError,e:
                    pass

                try:
                    p_cs_diff_10_20_r += timeline['csDiffPerMinDeltas']['tenToTwenty']
                    p_gold_delta_10_20_r += timeline['goldPerMinDeltas']['tenToTwenty']
                    #p_wards_delta_10_20_r += timeline['wardsPerMinDeltas']['tenToTwenty']
                    p_xp_diff_10_20_r += timeline['xpDiffPerMinDeltas']['tenToTwenty']

                except KeyError, r:
                    pass

                match_history_gathered += 1
        if skip_this_summoner or match_history_gathered==0:
            continue

        kda_r[team_id] += p_kda_r/float(match_history_gathered)
        win_rate_r[team_id] += p_win_rate_r/float(match_history_gathered)
        minion_kills_r[team_id] += p_minion_kills_r/float(match_history_gathered)
        n_monster_kills_r[team_id] += p_n_monster_kills_r/float(match_history_gathered)
        turret_kills_r[team_id] += p_turret_kills_r/float(match_history_gathered)
        gold_earned_r[team_id] += p_gold_earned_r/float(match_history_gathered)
        wards_placed_r[team_id] += p_wards_placed_r/float(match_history_gathered)
        wards_killed_r[team_id] += p_wards_killed_r/float(match_history_gathered)
        kill_participation_r[team_id] += p_kill_participation_r/float(match_history_gathered)
        damage_dealt_ratio_r[team_id] += p_damage_dealt_ratio_r/float(match_history_gathered)

        cs_diff_0_10_r[team_id] += p_cs_diff_0_10_r/float(match_history_gathered)
        cs_diff_10_20_r[team_id] += p_cs_diff_10_20_r/float(match_history_gathered)
        gold_delta_0_10_r[team_id] += p_gold_delta_0_10_r/float(match_history_gathered)
        gold_delta_10_20_r[team_id] += p_gold_delta_10_20_r/float(match_history_gathered)
        wards_delta_0_10_r[team_id] += p_wards_delta_0_10_r/float(match_history_gathered)
        wards_delta_10_20_r[team_id] += p_wards_delta_10_20_r/float(match_history_gathered)
        xp_diff_0_10_r[team_id] += p_xp_diff_0_10_r/float(match_history_gathered)
        xp_diff_10_20_r[team_id] += p_xp_diff_10_20_r/float(match_history_gathered)


        for champion in summoner_stats['champions']:
            if champion['id'] == 0:
                stats = champion['stats']
                total_sessions_played = float(stats['totalSessionsPlayed'] - total_sessions_played_s)
                #id 0 represents general stats - for all champions
                kda[team_id] += (stats['totalAssists'] - total_assists_s + stats['totalChampionKills'] - total_champion_kills_s)/float(stats['totalDeathsPerSession']-total_deaths_s)
                win_rate[team_id] += (stats['totalSessionsWon'] - total_won_s)/total_sessions_played
                r_games_played[team_id] += stats['totalSessionsPlayed'] - total_sessions_played_s

                minion_kills[team_id] += (stats['totalMinionKills'] - total_minion_kills_s)/total_sessions_played
                n_monster_kills[team_id] += (stats['totalNeutralMinionsKilled'] - total_neutral_m_s)/total_sessions_played
                turret_kills[team_id] += (stats['totalTurretsKilled'] - total_turrets_killed_s)/total_sessions_played
                gold_earned[team_id] += (stats['totalGoldEarned'] - total_gold_earned_s)/total_sessions_played
                demage_dealt_ratio[team_id] += stats['totalDamageDealt']/float(stats['totalDamageDealt'] + stats['totalDamageTaken'])
                firstbloods[team_id] += (stats['totalFirstBlood'] - total_firstbloods_s)/total_sessions_played
            elif champion['id'] == champion_id:
                #stats for the specific champion this player played that game
                stats = champion['stats']
                total_sessions_played_c = stats['totalSessionsPlayed'] - total_sessions_played_c_s

                if total_sessions_played_c > 0:
                    total_sessions_played_c = float(total_sessions_played_c)
                    deaths = stats['totalDeathsPerSession'] - total_deaths_c_s
                    if deaths == 0:
                        deaths = 1
                    kda_c[team_id] += (stats['totalAssists'] - total_assists_c_s + stats['totalChampionKills'] - total_champion_kills_c_s)/(float(deaths))
                    win_rate_c[team_id] += (stats['totalSessionsWon'] - total_won_c_s)/total_sessions_played_c
                    r_games_played_c[team_id] += stats['totalSessionsPlayed'] - total_sessions_played_c_s

                    minion_kills_c[team_id] += (stats['totalMinionKills'] - total_minion_kills_c_s)/total_sessions_played_c
                    #n_monster_kills_c[team_id] += stats['totalNeutralMinionsKilled']/float(stats['totalSessionsPlayed'])
                    turret_kills_c[team_id] += (stats['totalTurretsKilled'] - total_turrets_killed_c_s)/total_sessions_played_c
                    gold_earned_c[team_id] += (stats['totalGoldEarned'] - total_gold_earned_c_s)/total_sessions_played_c
                    demage_dealt_ratio_c[team_id] += stats['totalDamageDealt']/float(stats['totalDamageDealt'] + stats['totalDamageTaken'])
                    firstbloods_c[team_id] += (stats['totalFirstBlood'] - total_firstbloods_c_s)/total_sessions_played_c

        corrupt_champion_history_num = 0
        for g in summoner_champion_match_history:
             #check if we acttualy need to open another file to access this match
            if 'saved_file' in g:
                saved_file = g['saved_file']
                if saved_file == -1:
                    corrupt_champion_history_num += 1
                    continue
                g = load_obj('data/game_data_{0}.zip'.format(saved_file))
                if not g or g['matchId']==m_id:
                    corrupt_champion_history_num += 1
                    continue

            #we only need stats for player with current summoner_id
            try:
                participant_id = [p['participantId'] for p in g['participantIdentities'] if p['player']['summonerId'] == summoner_id][0]
            except Exception:
                corrupt_champion_history_num += 1
                continue
            participant = [p for p in g['participants'] if p['participantId'] == participant_id][0]
            stats = participant['stats']
            timeline = participant['timeline']

            game_duration_min = g['matchDuration']/60.0
            deaths = stats['deaths'] if stats['deaths']!=0 else 1
            p_kda_r_c += ((stats['assists'] + stats['kills'])/float(deaths))
            if stats['winner']:
                p_win_rate_r_c += 1
            p_minion_kills_r_c += (stats['minionsKilled']/game_duration_min)
            p_n_monster_kills_r_c += (stats['neutralMinionsKilled']/game_duration_min)
            p_turret_kills_r_c += stats['towerKills']
            p_gold_earned_r_c += (stats['goldEarned']/game_duration_min)
            p_wards_placed_r_c += (stats['wardsPlaced']/game_duration_min)
            p_wards_killed_r_c += (stats['wardsKilled']/game_duration_min)
            total_team_kills = sum([p['stats']['kills'] for p in g['participants'] if p['teamId'] == participant['teamId']])
            total_team_kills = total_team_kills if total_team_kills>0 else 1
            p_kill_participation_r_c += (stats['kills'] + stats['assists'])/float(total_team_kills)
            p_damage_dealt_ratio_r_c += stats['totalDamageDealtToChampions']/float(stats['totalDamageDealtToChampions']+stats['totalDamageTaken']+0.1)

            #participant timelane data
            try:
                p_cs_diff_0_10_r_c += timeline['csDiffPerMinDeltas']['zeroToTen']
                p_cs_diff_10_20_r_c += timeline['csDiffPerMinDeltas']['tenToTwenty']
                p_gold_delta_0_10_r_c += timeline['goldPerMinDeltas']['zeroToTen']
                p_gold_delta_10_20_r_c += timeline['goldPerMinDeltas']['tenToTwenty']
                #p_wards_delta_0_10_r_c += timeline['wardsPerMinDeltas']['zeroToTen']
                #p_wards_delta_10_20_r_c += timeline['wardsPerMinDeltas']['tenToTwenty']
                p_xp_diff_0_10_r_c += timeline['xpDiffPerMinDeltas']['zeroToTen']
                p_xp_diff_10_20_r_c += timeline['xpDiffPerMinDeltas']['tenToTwenty']
            except KeyError:
                pass


        num_valid_matches = len(summoner_champion_match_history)-corrupt_champion_history_num
        if num_valid_matches>0:
            kda_r_c[team_id] += p_kda_r_c/float(num_valid_matches)
            win_rate_r_c[team_id] += p_win_rate_r_c/float(num_valid_matches)
            minion_kills_r_c[team_id] += p_minion_kills_r_c/float(num_valid_matches)
            n_monster_kills_r_c[team_id] += p_n_monster_kills_r_c/float(num_valid_matches)
            turret_kills_r_c[team_id] += p_turret_kills_r_c/float(num_valid_matches)
            gold_earned_r_c[team_id] += p_gold_earned_r_c/float(num_valid_matches)
            wards_placed_r_c[team_id] += p_wards_placed_r_c/float(num_valid_matches)
            wards_killed_r_c[team_id] += p_wards_killed_r_c/float(num_valid_matches)
            kill_participation_r_c[team_id] += p_kill_participation_r_c/float(num_valid_matches)
            damage_dealt_ratio_r_c[team_id] += p_damage_dealt_ratio_r_c/float(num_valid_matches)

            cs_diff_0_10_r_c[team_id] += p_cs_diff_0_10_r_c/float(num_valid_matches)
            cs_diff_10_20_r_c[team_id] += p_cs_diff_10_20_r_c/float(num_valid_matches)
            gold_delta_0_10_r_c[team_id] += p_gold_delta_0_10_r_c/float(num_valid_matches)
            gold_delta_10_20_r_c[team_id] += p_gold_delta_10_20_r_c/float(num_valid_matches)
            wards_delta_0_10_r_c[team_id] += p_wards_delta_0_10_r_c/float(num_valid_matches)
            wards_delta_10_20_r_c[team_id] += p_wards_delta_10_20_r_c/float(num_valid_matches)
            xp_diff_0_10_r_c[team_id] += p_xp_diff_0_10_r_c/float(num_valid_matches)
            xp_diff_10_20_r_c[team_id] += p_xp_diff_10_20_r_c/float(num_valid_matches)
            num_summoners_c[team_id] += 1

        num_same_role = 0
        for g in summoner_match_history_roles:
            if g['timestamp']<game_creation_timestamp:
                if 'lane' in g and g['lane'] == game_participant_lane and 'role' in g and g['role'] == game_participant_role:
                    num_same_role += 1

        if summoner_id in game['participantTier']:
            tier[team_id] += LEAGUE_TIER_TO_SCORE[game['participantTier'][summoner_id]]
            num_summoners_p_tier[team_id] += 1


        if game_participant['highestAchievedSeasonTier'] != 'UNRANKED':
            previous_tier[team_id] += LEAGUE_TIER_TO_SCORE[game_participant['highestAchievedSeasonTier']]
            num_summoners_tier[team_id] += 1
        same_role[team_id] += num_same_role
        num_summoners[team_id] += 1

    #get composition winrates
    win_rate_compositions = {BLUE:[],RED:[]}
    winning_side = get_winner(game)
    for side in composition:
        composition[side].sort()
        for r in range(1,6):
            c_sum = 0
            c_count = 0
            combinations = itertools.combinations(composition[side], r)
            for c in combinations:
                if c in composition_to_winrate:
                    count = composition_to_winrate[c][0]
                    win = composition_to_winrate[c][1]
                    if m_id in composition_match_ids:
                        count -= 1
                        if winning_side == side:
                            win -= 1
                    if count > 0:
                        c_count += 1
                        c_sum += win/float(count)
            win_rate_compositions[side].append(c_sum/float(c_count) if c_count>0 else 0.5)



    num_summoners_tier[BLUE] = num_summoners_tier[BLUE] if num_summoners_tier[BLUE]>0 else 1
    num_summoners_tier[RED] = num_summoners_tier[RED] if num_summoners_tier[RED]>0 else 1
    num_summoners_p_tier[BLUE] = num_summoners_p_tier[BLUE] if num_summoners_p_tier[BLUE]>0 else 1
    num_summoners_p_tier[RED] = num_summoners_p_tier[RED] if num_summoners_p_tier[RED]>0 else 1
    if num_summoners[BLUE] > 0 and num_summoners[RED] > 0 and num_summoners_c[BLUE] > 0 and num_summoners_c[RED] > 0:
        blue_attributes.append(kda[BLUE]/num_summoners[BLUE])
        blue_attributes.append(win_rate[BLUE]/num_summoners[BLUE])
        blue_attributes.append(r_games_played[BLUE]/num_summoners[BLUE])
        blue_attributes.append(minion_kills[BLUE]/num_summoners[BLUE])
        blue_attributes.append(n_monster_kills[BLUE]/num_summoners[BLUE])
        blue_attributes.append(turret_kills[BLUE]/num_summoners[BLUE])
        blue_attributes.append(gold_earned[BLUE]/num_summoners[BLUE])
        blue_attributes.append(demage_dealt_ratio[BLUE]/num_summoners[BLUE])
        blue_attributes.append(tier[BLUE]/num_summoners_p_tier[BLUE])
        blue_attributes.append(previous_tier[BLUE]/num_summoners_tier[BLUE])
        blue_attributes.append(same_role[BLUE]/num_summoners[BLUE])
        #blue_attributes.append(firstbloods[BLUE]/num_summoners[BLUE])

        blue_attributes.append(kda_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(win_rate_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(r_games_played_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(minion_kills_c[BLUE]/num_summoners[BLUE])
        #blue_attributes.append(n_monster_kills_c[BLUE]/5.0)
        blue_attributes.append(turret_kills_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(gold_earned_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(demage_dealt_ratio_c[BLUE]/num_summoners[BLUE])
        #blue_attributes.append(firstbloods_c[BLUE]/num_summoners[BLUE])

        blue_attributes.append(kda_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(win_rate_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(minion_kills_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(n_monster_kills_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(turret_kills_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(gold_earned_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(wards_placed_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(wards_killed_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(kill_participation_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(damage_dealt_ratio_r[BLUE]/num_summoners[BLUE])

        blue_attributes.append(cs_diff_0_10_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(cs_diff_10_20_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(gold_delta_0_10_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(gold_delta_10_20_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(wards_delta_0_10_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(wards_delta_10_20_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(xp_diff_0_10_r[BLUE]/num_summoners[BLUE])
        blue_attributes.append(xp_diff_10_20_r[BLUE]/num_summoners[BLUE])

        blue_attributes.append(kda_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(win_rate_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(minion_kills_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(n_monster_kills_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(turret_kills_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(gold_earned_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(wards_placed_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(wards_killed_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(kill_participation_r_c[BLUE]/num_summoners[BLUE])
        blue_attributes.append(damage_dealt_ratio_r_c[BLUE]/num_summoners[BLUE])


        blue_attributes.append(cs_diff_0_10_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(cs_diff_10_20_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(gold_delta_0_10_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(gold_delta_10_20_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(wards_delta_0_10_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(wards_delta_10_20_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(xp_diff_0_10_r_c[BLUE]/num_summoners_c[BLUE])
        blue_attributes.append(xp_diff_10_20_r_c[BLUE]/num_summoners_c[BLUE])
        for wr in win_rate_compositions[BLUE]:
            blue_attributes.append(wr)



        red_attributes.append(kda[RED]/num_summoners[RED])
        red_attributes.append(win_rate[RED]/num_summoners[RED])
        red_attributes.append(r_games_played[RED]/num_summoners[RED])
        red_attributes.append(minion_kills[RED]/num_summoners[RED])
        red_attributes.append(n_monster_kills[RED]/num_summoners[RED])
        red_attributes.append(turret_kills[RED]/num_summoners[RED])
        red_attributes.append(gold_earned[RED]/num_summoners[RED])
        red_attributes.append(demage_dealt_ratio[RED]/num_summoners[RED])
        red_attributes.append(tier[RED]/num_summoners[RED])
        red_attributes.append(previous_tier[RED]/num_summoners_p_tier[RED])
        red_attributes.append(same_role[RED]/num_summoners[RED])
        #red_attributes.append(firstbloods[RED]/num_summoners[RED])

        red_attributes.append(kda_c[RED]/num_summoners[RED])
        red_attributes.append(win_rate_c[RED]/num_summoners[RED])
        red_attributes.append(r_games_played_c[RED]/num_summoners[RED])
        red_attributes.append(minion_kills_c[RED]/num_summoners[RED])
        #red_attributes.append(n_monster_kills_c[RED]/5.0)
        red_attributes.append(turret_kills_c[RED]/num_summoners[RED])
        red_attributes.append(gold_earned_c[RED]/num_summoners[RED])
        red_attributes.append(demage_dealt_ratio_c[RED]/num_summoners[RED])
       # red_attributes.append(firstbloods_c[RED]/num_summoners[RED])

        red_attributes.append(kda_r[RED]/num_summoners[RED])
        red_attributes.append(win_rate_r[RED]/num_summoners[RED])
        red_attributes.append(minion_kills_r[RED]/num_summoners[RED])
        red_attributes.append(n_monster_kills_r[RED]/num_summoners[RED])
        red_attributes.append(turret_kills_r[RED]/num_summoners[RED])
        red_attributes.append(gold_earned_r[RED]/num_summoners[RED])
        red_attributes.append(wards_placed_r[RED]/num_summoners[RED])
        red_attributes.append(wards_killed_r[RED]/num_summoners[RED])
        red_attributes.append(kill_participation_r[RED]/num_summoners[RED])
        red_attributes.append(damage_dealt_ratio_r[RED]/num_summoners[RED])
        
        red_attributes.append(cs_diff_0_10_r[RED]/num_summoners[RED])
        red_attributes.append(cs_diff_10_20_r[RED]/num_summoners[RED])
        red_attributes.append(gold_delta_0_10_r[RED]/num_summoners[RED])
        red_attributes.append(gold_delta_10_20_r[RED]/num_summoners[RED])
        red_attributes.append(wards_delta_0_10_r[RED]/num_summoners[RED])
        red_attributes.append(wards_delta_10_20_r[RED]/num_summoners[RED])
        red_attributes.append(xp_diff_0_10_r[RED]/num_summoners[RED])
        red_attributes.append(xp_diff_10_20_r[RED]/num_summoners[RED])

        red_attributes.append(kda_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(win_rate_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(minion_kills_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(n_monster_kills_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(turret_kills_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(gold_earned_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(wards_placed_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(wards_killed_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(kill_participation_r_c[RED]/num_summoners[RED])
        red_attributes.append(damage_dealt_ratio_r_c[RED]/num_summoners[RED])


        red_attributes.append(cs_diff_0_10_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(cs_diff_10_20_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(gold_delta_0_10_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(gold_delta_10_20_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(wards_delta_0_10_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(wards_delta_10_20_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(xp_diff_0_10_r_c[RED]/num_summoners_c[RED])
        red_attributes.append(xp_diff_10_20_r_c[RED]/num_summoners_c[RED])
        for wr in win_rate_compositions[RED]:
            red_attributes.append(wr)

        #get winner - goal atribute
        if get_winner(game)==BLUE:
            winner_atr = "blue"
        else:
            winner_atr = "red"

        #write attributes to file
        data_file.write(str(num_summoners[BLUE]+num_summoners[RED]) + "\t")
        if RELATIVE_ATTRS:
            for i in range(len(blue_attributes)):
                data_file.write(str(blue_attributes[i] - red_attributes[i])+"\t")
            data_file.write(winner_atr + "\n")
        else:
            for atr in blue_attributes:
                data_file.write(str(atr)+"\t")
            for atr in red_attributes:
                data_file.write(str(atr)+"\t")
            data_file.write(winner_atr + "\n")
    read_files += 1
    print(str(read_files) + "/" + str(6000))

data_file.close()
