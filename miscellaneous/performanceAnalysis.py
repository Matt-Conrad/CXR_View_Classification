import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

data = pd.read_csv("performance.csv", index_col=0)
desktopData = data.iloc[:, 0:3]
laptopData = data.iloc[2:, 3:6]
laptopDataT = laptopData.transpose()

fig, axes = plt.subplots(2, 3)

axes = axes.ravel()

xlabels = None 
for ind, colName in enumerate(laptopDataT.columns.tolist()):
    xlabels = laptopDataT[colName].index.tolist()
    axes[ind].bar(xlabels, laptopDataT[colName].values.tolist(), color=['r','g','b'])
    axes[ind].get_xaxis().set_visible(False)
    axes[ind].set_ylabel("Seconds")
    axes[ind].set_title(colName)

fig.legend(axes[0].patches, xlabels, loc='lower center')
plt.show()