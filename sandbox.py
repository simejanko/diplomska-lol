import itertools
import matplotlib.pyplot as plt
import numpy as np

compositions = open('data_composition_diamond_challenger.tab','r')
champion_ids = [int(atr_name.split(' ')[2]) for atr_name in compositions.readline().split('\t')[2:-1]]
champion_ids = champion_ids[:len(champion_ids)//2]
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

winrates = sorted([composition_to_winrate[c][1]/float(composition_to_winrate[c][0]) for c in composition_to_winrate if len(c)==1], reverse=True)
winrates = winrates[:3] + winrates[-3:]


n_groups = 1
fig, ax = plt.subplots()
index = np.arange(n_groups)
index = index * 1.5
bar_width = 0.2

for i in range(6):
    color  = 'blue' if i<3 else 'red'
    rects = plt.bar(index+bar_width*i , winrates[i], bar_width,color=color,alpha=0.6)
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
plt.xlabel('heroji')
plt.ylabel('delež zmag')
# plt.xticks(index + bar_width*2, ('sodelovanje pri ubojih (kill participation)'))
#plt.legend(loc='lower right')

plt.show()