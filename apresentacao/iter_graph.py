import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('log_dists.csv', index_col='iter')
df.columns = ['Custo']
df.index.name = 'Iteração'
df.plot()
plt.axhline(y=784, color='r', linestyle='-')
plt.xlim(0, len(df))
plt.ylim(700, 1020)
plt.xticks(range(0,len(df),50))
#plt.show()
plt.savefig('grafico_iter.png', dpi=350)