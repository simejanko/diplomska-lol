from tools import load_obj
import os.path

LEAGUE_TIER_TO_SCORE = {'BRONZE':0.0,'SILVER':1.0,'GOLD':2.0,'PLATINUM':3.0,'DIAMOND':4.0,'MASTER':5.0,'CHALLENGER':6.0}
#TODO: role

data_file = open("player_stats2.tab","a")
"""data_file.write("wards placed/min\twards killed/min\tkill participation\tdragon kills/min\tbaron kills/min\t")
data_file.write("games played\tminion kills/game\tn.m. kills/game\tturrets killed/game\t")
data_file.write("diffrent champions/game\tchamp mastery 5\tchamp mastery 10\tchamp mastery 20\t")
data_file.write("".join(["champ winrate " + str(i)+ "\t" for i in range(5)]))
data_file.write("tier\n")"""

read_files = 0
pulled_summoners = list()

def write_attribute(file, value):
    file.write(str(value) + '\t')

while os.path.isfile('../data/game_data_{0}.zip'.format(read_files)):
    game = load_obj('../data/game_data_{0}.zip'.format(read_files))
    if not game or (game['matchVersion'][:4] != '6.10' and game['matchVersion'][:3] != '6.9') :
        read_files += 1
        print(str(read_files) + "/" + str(6000))
        continue

    for summoner_stats in game['participantStats']:
        summoner_id = summoner_stats['summonerId']
        if summoner_id not in pulled_summoners and summoner_id in game['participantTier']:
            wards_placed=wards_killed=kill_participation=dragon_kills=baron_kills=total_games=0
            summoner_match_history = game['participantMatchHistory'][summoner_id]
            for g in summoner_match_history:
                if g['matchId'] == -1:
                    continue

                # check if we acttualy need to open another file to access this match
                if 'saved_file' in g:
                    saved_file = g['saved_file']
                    g = load_obj('../data/game_data_{0}.zip'.format(saved_file))
                    if not g:
                        continue

                # we only need stats for player with current summoner_id
                try:
                    participant_id = \
                    [p['participantId'] for p in g['participantIdentities'] if p['player']['summonerId'] == summoner_id][0]
                except Exception:
                    continue

                participant = [p for p in g['participants'] if p['participantId'] == participant_id][0]
                team_id = participant['teamId']
                team_stats = [t for t in g['teams'] if t['teamId']==team_id][0]
                stats = participant['stats']
                timeline = participant['timeline']

                game_duration_min = g['matchDuration'] / 60.0
                total_games += 1
                wards_placed += stats['wardsPlaced'] / game_duration_min
                wards_killed += stats['wardsKilled'] / game_duration_min
                total_team_kills = sum(
                    [p['stats']['kills'] for p in g['participants'] if p['teamId'] == participant['teamId']])
                total_team_kills = total_team_kills if total_team_kills > 0 else 1
                kill_participation += (stats['kills'] + stats['assists'])/float(total_team_kills)
                dragon_kills += team_stats['dragonKills'] / game_duration_min
                baron_kills += team_stats['baronKills'] / game_duration_min
            if total_games<=0:
                continue

            #write attributes
            total_games = float(total_games)
            write_attribute(data_file, wards_placed / total_games)
            write_attribute(data_file, wards_killed / total_games)
            write_attribute(data_file, kill_participation / total_games)
            write_attribute(data_file, dragon_kills / total_games)
            write_attribute(data_file, baron_kills / total_games)

            #all season stats
            uniq_champs = list()
            champ_mastery_5 = champ_mastery_10 = champ_mastery_20 = 0
            champ_to_winrate = list()
            for champion in summoner_stats['champions']:
                stats = champion['stats']
                if champion['id'] == 0:
                    total_sessions_played = float(stats['totalSessionsPlayed'])
                    write_attribute(data_file, stats['totalSessionsPlayed'])
                    write_attribute(data_file, stats['totalMinionKills']/total_sessions_played)
                    write_attribute(data_file, stats['totalNeutralMinionsKilled']/total_sessions_played)
                    write_attribute(data_file, stats['totalTurretsKilled'] / total_sessions_played)
                else:
                    if champion['id'] not in uniq_champs:
                        uniq_champs.append(champion['id'])
                        champ_to_winrate.append([stats['totalSessionsWon'], stats['totalSessionsPlayed']])
                        if stats['totalSessionsPlayed'] >= 5:
                            champ_mastery_5 += 1
                        if stats['totalSessionsPlayed'] >= 10:
                            champ_mastery_10 += 1
                        if stats['totalSessionsPlayed'] >= 20:
                            champ_mastery_20 += 1

            while len(champ_to_winrate)<5:
                champ_to_winrate.append([0.5,1])
            champ_to_winrate = sorted(champ_to_winrate, key=lambda x:x[1], reverse=True)[:5]
            champ_to_winrate = sorted(champ_to_winrate, key=lambda x:x[0]/float(x[1]), reverse=True)

            #write attributes
            write_attribute(data_file, len(uniq_champs)/total_sessions_played)
            write_attribute(data_file, champ_mastery_5)
            write_attribute(data_file, champ_mastery_10)
            write_attribute(data_file, champ_mastery_20)

            for won,played in champ_to_winrate:
                write_attribute(data_file, won/float(played))

            data_file.write(str(LEAGUE_TIER_TO_SCORE[game['participantTier'][summoner_id]]) + '\n')

            pulled_summoners.append(summoner_id)

    read_files += 1
    print(str(read_files) + "/" + str(6000))