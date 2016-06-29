import os
import os.path
import time
import zipfile
import random
from riotwatcher import RiotWatcher, EUROPE_WEST, LoLException
from tools import save_obj, load_obj
unpulled_summoners = [52333251,72343187,22403890] #Insert some starting summoner ids here
pulled_summoners = list()
#matchId : file number
pulled_matches = list()
pulled_matches_count = 0
#saved_files = 0
#match_data_to_save = []
data_file = open("data_composition.tab","a")

BLUE = 100
RED = 200

w = RiotWatcher("YOUR-API-KEY", default_region=EUROPE_WEST)

def wait_for_request_availability(w):
    while not w.can_make_request():
        time.sleep(0.2)

champions = w.get_all_champions()
if not os.path.isfile('pulled_matches.txt'):
    data_file.write("matchId\tcreateDate\t")
    for champion in champions['champions']:
        data_file.write("b chmp " + str(champion['id']) + "\t")
    for champion in champions['champions']:
        data_file.write("r chmp " + str(champion['id']) + "\t")
    data_file.write("winner\n")

    data_file.write("c\t"*2)
    data_file.write("c\t" * (2*len(champions['champions'])))
    data_file.write("d\n")

    data_file.write("meta\t"*2)
    data_file.write("\t" * (2*len(champions['champions'])))
    data_file.write("class\n")
else:
#restore program state
    with open('pulled_matches.txt','r') as file:
        for line in file:
            pulled_matches.append(int(line))
            pulled_matches_count +=1
pulled_matches_file = open('pulled_matches.txt', 'a')
while True:
    if len(unpulled_summoners) == 0:
        #if we run out of summoners, hopefully older summoners already played new matches
        unpulled_summoners = random.sample(pulled_summoners, 30)
        pulled_summoners = list()

    current_summoner_id = unpulled_summoners.pop(0)

    try:
        wait_for_request_availability(w)
        match_history = w.get_recent_games(current_summoner_id)
    except Exception,e:
            print("An ERROR occurred when pulling match history data for summonerId {0}! {1}".format(current_summoner_id,e))
            unpulled_summoners.insert(0, current_summoner_id)
            continue

    pulled_summoners.append(current_summoner_id)
    for match in match_history['games']:
        matchId = match['gameId']
        if matchId not in pulled_matches and match['subType'] in ('RANKED_SOLO_5x5','RANKED_PREMADE_5x5') and match['createDate'] > int(time.time()*1000) - 3*24*60*60000:
            pulled_matches.append(matchId)
            pulled_matches_file.write(str(matchId) + '\n')
            participants_ids = [player['summonerId'] for player in match['fellowPlayers']]
            try:
                wait_for_request_availability(w)
                participants_league_data = w.get_league(summoner_ids=participants_ids)
            except Exception, e:
                print("Error occured when trying to get league data: " + str(e))
                continue

            for p_id in participants_ids:
                try:
                    for league_info in participants_league_data[str(p_id)]:
                        #add participant to unpulled_summoners only if he is currently in high league
                        if league_info['queue'] == 'RANKED_SOLO_5x5':
                            if p_id not in unpulled_summoners and p_id not in pulled_summoners:
                                unpulled_summoners.append(p_id)
                except KeyError, e:
                    print("Error occured when trying to get summoners to pull: " + str(e))
                    continue

            #now get compositions
            composition = dict()
            composition[BLUE] = [player['championId'] for player in match['fellowPlayers'] if player['teamId']==BLUE]
            composition[RED] = [player['championId'] for player in match['fellowPlayers'] if player['teamId']==RED]
            #add pulled summoner to the mix
            composition[match['teamId']].append(match['championId'])
            #get winner
            if match['stats']['win']:
                if match['teamId'] == BLUE:
                    winner = "blue"
                else:
                    winner = "red"
            else:
                if match['teamId'] == BLUE:
                    winner = "red"
                else:
                    winner = "blue"
            data_file.write(str(matchId)+"\t"+str(match['createDate'])+"\t")
            data_file.write("\t".join("1" if champion['id'] in composition[BLUE] else "0" for champion in champions['champions'] ))
            data_file.write("\t" + "\t".join("1" if champion['id'] in composition[RED] else "0" for champion in champions['champions'] ))
            data_file.write("\t" + winner + "\n")

            pulled_matches_count += 1
            #match_data_to_save.append(match_data)

            print "pulled {0} matches so far".format(pulled_matches_count)


data_file.close()
pulled_matches_file.close()
