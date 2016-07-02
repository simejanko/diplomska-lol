import numpy as np
from machine_learning.utils import  *
import matplotlib.pyplot as plt
import scipy.stats
fname = 'player_stats2.tab'
LEAGUE_SCORE_TO_TIER = ['Bronze','Silver','Gold','Platinum','Diamond','Master','Challenger']

attributes, target, row_i, col_i = file_to_dataset(fname,0,-1,-1,skip_lines=1)
attributes = np.array(attributes)
target = np.array(target,dtype=float).astype(int)


u_values = np.unique(target)
n_groups = 2
fig, ax = plt.subplots()
index = np.arange(n_groups)
index = index * 1.5
bar_width = 0.2
colors = ['#cd7f32','#C0C0C0','#FFD700','#008080','#00ffff','#800080','#FF00FF']

for i,value in enumerate(np.nditer(u_values)):
    current = attributes[target==value,:2]
    means = np.mean(current, axis=0)
    rects = plt.bar(index + bar_width*i, means, bar_width,
                     color=colors[value],
                     label=LEAGUE_SCORE_TO_TIER[value],
                     alpha=0.6)

#champ_means = np.mean(attributes[:,13:18],axis=0)
#champ_stds = np.std(attributes[:,13:18],axis=0)
#champ_stds = scipy.stats.sem(attributes[:,13:18],axis=0)
"""for i in range(5):
    rects = plt.bar(index+bar_width*i , champ_means[i], bar_width,color='blue',alpha=0.6,yerr=champ_stds[i],ecolor='red')
    print(champ_stds[i])"""




#plt.xlabel('lige')
#plt.ylabel('št.  odigranih iger v obdobju od januarja do junija 2016')
plt.xticks(index + bar_width*3, ('postavljeni razsvetljevalci/min','uničeni razsvetljevalci/min'))
plt.legend(loc='upper right')
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='on') # labels along the bottom edge are off
#plt.boxplot(attributes[:,13:18],showfliers=False)
#plt.xlabel('heroji')
#plt.ylabel('povprečni delež zmag')
plt.show()

