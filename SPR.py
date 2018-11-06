import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *


#THE DIRECTORY WITH ALL THE DATA GOES HERE
data = loader("/Users/dennismichalak/research/SmgGDS+KRas/data/spr_KRasT_20181008/")
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "KRasFMe-GDP Titration"
###The various concentrations have to be manually added below in micromolar (first concentation should be zero for baseline)
concs = np.array([0,0.15,0.30,0.50,1.0,2.0,3.0])


num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5)

###Figsize and fontsize here
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)
matplotlib.rc('font', size = 18)
#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,ShowFits=True)
plotdata[0][0].set_label("Baseline")
for i in range(1,np.size(concs)):
    plotdata[i][0].set_label(str(concs[i])+r'$\mu$M')
try:
    plotdata[(np.size(concs))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")

FitToLangmuir(concs,pixels,errors,title)

ax1.set_title(title)

ax1.legend(prop={'size': 12})
matplotlib.rc('font', size = 18)
# plt.show(ax1)
plt.savefig('spr.png')
plt.savefig('spr.pdf')
