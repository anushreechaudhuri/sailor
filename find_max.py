import pandas as pd
import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import progressbar
import os

directory = '/home/anushree/Documents/sailor/7-24-19/'
filelist = []
for filename in os.listdir(directory):
    if filename.endswith('.txt') and filename.startswith('50'):
        filelist.append(os.path.join(directory,filename))

sortList = sorted(filelist, reverse=True)
i = len(sortList)
full_df = pd.DataFrame()
for file in progressbar.progressbar(sortList):
       i -= 1
       with open(file, 'r') as f:
            df = pd.read_csv(f, names = ['Wavelength', 'INT' + str(i)], skiprows= 16, delim_whitespace = True)
            if full_df.empty:
                full_df = df
            else:
                full_df.insert(1, 'INT' + str(i), df['INT' + str(i)])

import matplotlib.style as style
style.use('seaborn-poster')
style.use('ggplot')

intensity = list(full_df.max())[1:]
smoothed = scipy.signal.savgol_filter(intensity, 201, 4)

plt.title('PL Intensity vs. Minutes Elapsed', fontsize=24)
plt.xlabel('Minutes Elapsed', fontsize=20)
plt.ylabel('PL Intensity', fontsize=20)
plt.axvline(x=np.argmax(smoothed), linestyle='--', label='t = ' + str(np.argmax(smoothed)))
plt.plot(range(len(intensity)), intensity, alpha=0.3)
plt.plot(range(len(intensity)), smoothed)
plt.legend()
plt.savefig('newplot.png', dpi=300)
