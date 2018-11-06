import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *

#THE DIRECTORY WITH ALL THE DATA GOES HERE
data = loader("../../../Downloads/spr_500KrasSmgT_20180927/")
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "Myr Nef on 70:30 DOPC:DOPS"
###The various concentrations have to be manually added below in micromolar (first concentation should be zero for baseline)
concs = np.array([0,0.128,0.250,0.509,1.01,2.016,3.972,7,8])


#INFO FOR SECOND DATA SET
data2 = loader("../Nef091218/")
rinsename2 = "rinse"
filename2 = "conc"
concs2 =np.array([0,0.128,0.250,0.509,1.01,2.016,3.972])


num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5)


#Figsize and fonts here
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)


#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,ShowFits=False)
plotdata[0][0].set_label("Baseline")
for i in range(1,np.size(concs)):
    plotdata[i][0].set_label(str(concs[i])+r' $\mu$M')
try:
    plotdata[(np.size(concs))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")
ax1.set_title(title)




num2 = np.size(concs2) - 1
(data2,fits2,pixels2,errors2) = Organise(data2,num2,smoothing=5)
#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata2,plotfits2) = Plotter(fig1,ax1,data2,fits2,pixels2,errors2,num2,ShowFits=False,linewidth=2,alpha=0.5)
plotdata2[0][0].set_label("Baseline")
for i in range(1,np.size(concs2)):
    plotdata2[i][0].set_label(str(concs2[i])+r' $\mu$M')
try:
    plotdata2[(np.size(concs2))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")



#THIS CREATES TWO SEPARATE LEGENDS
labels1 = []
for i in range(0,np.size(concs)):
    labels1.append(plotdata[i][0])

labels2 = []
for i in range(0,np.size(concs2)):
    labels2.append(plotdata2[i][0])
legend1 = ax1.legend(handles=labels1,prop={'size': 12},loc=0)####CHANGE LEGEND POSITIONS HERE. Zero is autoplace
ax1.add_artist(legend1)
ax1.legend(handles=labels2,prop={'size': 12},loc=0)######CHANGE LEGEND POSITIONS HERE

plt.show(ax1)
