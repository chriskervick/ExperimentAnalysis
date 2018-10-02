import numpy as np 
from matplotlib import pyplot as plt
#%config InlineBackend.figure_format = 'retina'
from scipy.optimize import curve_fit
from scipy.interpolate import *
from SPRFunctions import *


#THE DIRECTORY WITH ALL THE DATA GOES HERE
dire = "../NefSummer2018/Nef082018/"
fname = "7030DOPCDOPS_082018.pdf"
data = loader(dire)
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "Myr Nef on 70:30 DOPC:DOPS @ 10% Glycerol"
###The various concentrations have to be manually added below in micromolar (first concentation should be zero for baseline)
concs = 0.6*np.array([0,0.130,0.252,0.499])


num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5)

###Figsize and fontsize here
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)

plt.rcParams.update({'font.size': 30})
plt.rcParams.update({'axes.titlesize': 30})
#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,ShowFits=False,rinselimit=450)
plotdata[0][0].set_label("Baseline")
for i in range(1,np.size(concs)):
    plotdata[i][0].set_label(str(concs[i])+r' $\mu$ mol') 
try:
    plotdata[(np.size(concs))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")
ax1.set_title(title)

ax1.legend(prop={'size': 12})


plt.rcParams.update({'font.size': 30})
plt.rcParams.update({'axes.titlesize': 30})

for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
    item.set_fontsize(20)


plt.savefig(dire+fname)




