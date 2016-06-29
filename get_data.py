import os
import os.path
import time
import zipfile
import random
from riotwatcher import RiotWatcher, EUROPE_WEST, LoLException
from tools import save_obj, load_obj
unpulled_summoners = [35076397, 41527671, 80239244, 78377150] #Insert some starting summoner ids here
pulled_summoners = list()
#matchId : file number
pulled_matches = dict()
pulled_matches_count = 0
saved_files = 0
match_data_to_save = []

w = RiotWatcher("YOUR-API-KEY", default_region=EUROPE_WEST)

def wait_for_request_availability(w):
    while not w.can_make_request():
        time.sleep(0.2)

#alt_list is for further prevention of requestion same match_ids multiple times
def get_match_details_from_history(match_history, match_created, num_old_matches=10, alt_list = []):
    if 'matches' not in match_history:
        #history is empty
        return []
    newer_match_ids = [match['matchId'] for match in match_history['matches'] if match['timestamp'] > match_created]
    older_match_ids = [match['matchId'] for match in match_history['matches'] if match['timestamp'] < match_created]
    #this is to avoid queries that take way too long
    if len(newer_match_ids)>40:
        #-1 means skip this summoner - too many matches to get - time consuming
        return [{'matchId':-1, 'saved_file':-1}]
    alt_list_match_id_to_index = {m['matchId'] : i for i,m in enumerate(alt_list)}
    if len(older_match_ids)<num_old_matches:
        num_old_matches = len(older_match_ids)

    match_ids = newer_match_ids + older_match_ids[:num_old_matches]
    matches_data = []
    for match_id in match_ids:
        if match_id in pulled_matches:
            matches_data.append({'matchId':match_id, 'saved_file':pulled_matches[match_id]})
        elif match_id in alt_list_match_id_to_index:
            matches_data.append(alt_list[alt_list_match_id_to_index[match_id]])
        else:
            num_try = 0
            while num_try<11:
                num_try += 1
                try:
                    wait_for_request_availability(w)
                    match_d = w.get_match(match_id, include_timeline=False)
                    matches_data.append(match_d)
                    break
                except Exception, e:
                    print("Error occured when trying to get match history details for " + str(match_id) + " data: " + str(e))
                    time.sleep(1)
                    continue
            if num_try >=11:
                if match_id in newer_match_ids:
                    return [{'matchId':-1, 'saved_file':-1}]
                    
    return matches_data

#restore program state
while os.path.isfile('game_data_{0}.zip'.format(saved_files)):
    with zipfile.ZipFile('game_data_{0}.zip'.format(saved_files), 'r') as myzip:
        myzip.extractall()
    match = load_obj('game_data_{0}.pkl'.format(saved_files))
    pulled_matches[match['matchId']] = saved_files
    pulled_matches_count += 1
    os.remove('game_data_{0}.pkl'.format(saved_files))

    saved_files += 1

while True:
    if len(unpulled_summoners) == 0:
        #if we run out of summoners, hopefully older summoners already played new matches
        unpulled_summoners = random.sample(pulled_summoners, 15)
        pulled_summoners = list()

    current_summoner_id = unpulled_summoners.pop(0)

    try:
        wait_for_request_availability(w)
        match_history = w.get_match_list(current_summoner_id, season='SEASON2016',ranked_queues=('RANKED_SOLO_5x5', 'TEAM_BUILDER_DRAFT_RANKED_5x5') , begin_index=0, end_index=15)
    except Exception,e:
            print("An ERROR occurred when pulling match history data for summonerId {0}! {1}".format(current_summoner_id,e))
            unpulled_summoners.insert(0, current_summoner_id)
            continue
    try:
        matchIdsToTimestamp = { match['matchId']:match['timestamp'] for match in match_history['matches'] }
    except KeyError,e:
        print("Some field you tried to access did not exist in the pulled summoner data: {0}".format(e))
        continue

    pulled_summoners.append(current_summoner_id)
    for matchId, timestamp in matchIdsToTimestamp.items():
        if matchId not in pulled_matches and timestamp > int(time.time()*1000) - 3*24*60*60000:
            try:
                wait_for_request_availability(w)
                match_data = w.get_match(matchId, include_timeline=False)
                participants_ids = [pIdentity['player']['summonerId'] for pIdentity in match_data['participantIdentities']]
                match_specific_pids = [pIdentity['participantId'] for pIdentity in match_data['participantIdentities']]
                participants_champion_played = {participants_ids[match_specific_pids.index(participant['participantId'])]:participant['championId'] for participant in match_data['participants']}
            except Exception, e:
                print("Error occured when trying to get match details: " + str(e))
                continue
            pulled_matches[matchId] = saved_files

            try:
                wait_for_request_availability(w)
                participants_league_data = w.get_league(summoner_ids=participants_ids)
            except Exception, e:
                print("Error occured when trying to get league data: " + str(e))
                continue

            #get aditional summoners to pull and add league info data to match_data
            match_data['participantTier'] = dict()
            for p_id in participants_ids:
                try:
                    for league_info in participants_league_data[str(p_id)]:
                        #add participant to unpulled_summoners only if he is currently in high league
                        if league_info['queue'] == 'RANKED_SOLO_5x5':
                            match_data['participantTier'][p_id] = league_info['tier']
                            if p_id not in unpulled_summoners and p_id not in pulled_summoners:
                                unpulled_summoners.append(p_id)
                except KeyError, e:
                    print("Error occured when trying to get summoners to pull: " + str(e))
                    continue
            #add match history and stats for every participant
            match_data['participantStats'] = list()
            #needed later on
            stats_last_update = dict()
            for p_id in participants_ids:
                while(True):
                    try:
                        wait_for_request_availability(w)
                        ranked_stats = w.get_ranked_stats(p_id)
                        match_data['participantStats'].append(ranked_stats)
                        stats_last_update[p_id] = ranked_stats['modifyDate']
                        break
                    except Exception, e:
                        print("Error occured when trying to get ranked stats data: " + str(e))
                        time.sleep(2)
                        continue

            match_data['participantMatchHistory'] = dict()
            match_data['participantChampionMatchHistory'] = dict()
            match_data['participantMatchListHistory'] = dict()

            match_created = match_data['matchCreation']


            for p_id in participants_ids:
                while(True):
                    try:
                        match_list_end_time = stats_last_update[p_id] if stats_last_update>match_created-1 else match_created-1
                        wait_for_request_availability(w)
                        player_match_history = w.get_match_list(p_id,end_time=match_list_end_time , season='SEASON2016',ranked_queues=('RANKED_SOLO_5x5', 'TEAM_BUILDER_DRAFT_RANKED_5x5'))
                        wait_for_request_availability(w)
                        player_champion_match_history = w.get_match_list(p_id,end_time=match_created-1 , season='SEASON2016',ranked_queues=('RANKED_SOLO_5x5', 'TEAM_BUILDER_DRAFT_RANKED_5x5'), champion_ids=participants_champion_played[p_id])

                        
                        match_data['participantMatchHistory'][p_id] = get_match_details_from_history(player_match_history, match_created)
                        match_data['participantChampionMatchHistory'][p_id] = get_match_details_from_history(player_champion_match_history, match_created, alt_list=match_data['participantMatchHistory'][p_id])
                        match_data['participantMatchListHistory'][p_id] = player_match_history

                        break
                    except Exception, e:
                        print("Error occured when trying to get summoner history data: " + str(e))
                        time.sleep(1)
                        continue

            pulled_matches_count += 1
            #match_data_to_save.append(match_data)
            print "pulled {0} matches so far".format(pulled_matches_count)

            #save match data to file every  match
            #if len(match_data_to_save) >= 1:
            save_obj(match_data,'game_data_{0}.pkl'.format(saved_files))
            match_data = None
            with zipfile.ZipFile('game_data_{0}.zip'.format(saved_files), 'w', zipfile.ZIP_DEFLATED) as myzip:
                myzip.write('game_data_{0}.pkl'.format(saved_files))
            os.remove('game_data_{0}.pkl'.format(saved_files))
            saved_files += 1
            #match_data_to_save = list()

