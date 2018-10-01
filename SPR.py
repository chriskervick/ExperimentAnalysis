import numpy as np 
from matplotlib import pyplot as plt
%config InlineBackend.figure_format = 'retina'
from scipy.optimize import curve_fit
from scipy.interpolate import *
from SPRFunctions import *


#THE DIRECTORY WITH ALL THE DATA GOES HERE
data = loader("../../../Downloads/spr_500KrasSmgT_20180927/")
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "Myr Nef on 70:30 DOPC:DOPS"
###The various concentrations have to be manually added below in micromolar (first concentation should be zero for baseline)
concs = np.array([0,0.128,0.250,0.509,1.01,2.016,3.972,7,8])


num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5)

###Figsize and fontsize here
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)
matplotlib.rc('font', size = 18)
#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,ShowFits=False)
plotdata[0][0].set_label("Baseline")
for i in range(1,np.size(concs)):
    plotdata[i][0].set_label(str(concs[i])+r' $\mu$ mol') 
try:
    plotdata[(np.size(concs))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")
ax1.set_title(title)

ax1.legend(prop={'size': 12})
matplotlib.rc('font', size = 18)
plt.show(ax1)

