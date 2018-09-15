# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("train_graph.csv", index_col='step')

fig, ax1 = plt.subplots()
df_acc = data.iloc[:, [0]]
df_val_acc = data.iloc[:, [1]]

ax1.plot(df_acc, 'r', label='acc')
ax1.set_xlabel('epoch')
ax1.set_ylabel('acc')
# ax1.set_ylim([0,1])
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(df_val_acc, 'b', label='val_acc')
ax2.set_ylabel('val_acc')
ax2.set_ylim(bottom=0)
ax2.legend(loc='lower left')

# plt.xlim([0,200])
plt.savefig("plot.png")
plt.show()
