import scrapy
import datetime
import time
import traceback

class GamepediaSpider(scrapy.Spider):
    LANES = ['top','jungle','mid','adc','support']

    name = 'gamepediaspider'

    start_urls = ['http://lol.gamepedia.com/2016_LCK/Spring_Split/Scoreboards/Week_' + str(i) for i in range(1,14)] +\
                 ['http://lol.gamepedia.com/2015_LCK_Summer/Scoreboards/Regular_Split/Week_'  + str(i) for i in range(1,14)] +\
                 ['http://lol.gamepedia.com/2015_LCK_Spring/Scoreboards/Round_Robin/Week_' + str(i) for i in range(1,13)]

    def parse(self, response):
        for t_n, table in enumerate(response.css('table.match-recap')):
            try:
                match = {'blue' : {}, 'red' : {}}
                for lane in GamepediaSpider.LANES:
                    match['blue'][lane] = dict()
                    match['red'][lane] = dict()

                trs = table.css('table.match-recap>tr')
                ths = trs[1].css('th::text').extract()
                name_prefix = '2015_' if '2015' in response.url else ''
                split_prefix = 'spring_' if 'spring' in response.url.lower() else ''
                match['blue']['name'] = name_prefix+ split_prefix + ths[0].strip()
                match['red']['name'] = name_prefix + split_prefix + ths[3].strip()
                blue_winner = int(ths[1])
                red_winner = int(ths[2])
                #also handles best of 3 matches
                if blue_winner > red_winner:
                    match['winner'] = 'blue'
                elif blue_winner < red_winner:
                    match['winner'] = 'red'
                else:
                    match['winner'] = old_winner


                old_winner = match['winner']
                tds = trs[4].css('table td::text').extract()
                try:
                    dt = datetime.datetime.strptime(tds[0].strip()[-10:] + ' ' + tds[3].strip()[:5], "%Y-%m-%d %H:%M")
                except ValueError:
                    dt = datetime.datetime.strptime(tds[0].strip()[-10:] + ' ' + tds[3].strip()[:5], "%m/%d/%Y %H:%M")
                length = tds[5].strip()[-5:].split(':')
                match['timestamp'] = time.mktime(dt.timetuple())
                match['length'] = int(length[0]) + (int(length[1])/60.0)

                player_trs = trs[6].css('table>tr')
                player_trs = {'blue' : player_trs[1:6], 'red' : player_trs[7:12]}
                for team in player_trs:
                    for i,player_tr in enumerate(player_trs[team]):
                        lane = GamepediaSpider.LANES[i]
                        tds = player_tr.css('td::text').extract()
                        tds_a = player_tr.css('td>a::attr(title)').extract()

                        match[team][lane]['champion'] = tds_a[0].strip()
                        match[team][lane]['name'] = tds_a[1].strip()
                        match[team][lane]['spell_1'] = tds_a[2].strip()
                        match[team][lane]['spell_2'] = tds_a[3].strip()
                        match[team][lane]['key_mastery'] = tds_a[4].strip()


                        match[team][lane]['kills'] = int(tds[-12].strip())
                        match[team][lane]['deaths'] = int(tds[-11].strip())
                        match[team][lane]['assists'] = int(tds[-10].strip())
                        #match[team][lane]['gold'] = float(tds[-2].strip().strip('k')) * 1000
                        match[team][lane]['cs'] = int(tds[-1].strip())

                yield match
            except Exception,e:
                print("ERROR " + response.url + " - " + str(t_n) + ": " + str(e))
                continue
