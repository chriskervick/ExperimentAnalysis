import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *


#THE DIRECTORY WITH ALL THE DATA GOES HERE

dire = "../NefSummer2018/Nef091218/"
fname = "7030POPCPOPG_091218_COMPARISON"
data = loader(dire)
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "Myr Nef on 70:30 POPC:POPG @ 8% and 2.5% Glycerol"
###The various concentrations have to be manually added below in micromolar (first concentation should be zero for baseline)
concs = np.array([0,0.128,0.250,0.509,1.010,2.016,3.972])



num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5,filename = filename)

###Figsize and fontsize here
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)



#THIS AUTOLABELS VIA THE CONCENTRATIONS
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,filename=filename,ShowFits=False,rinselimit=0)
plotdata[0][0].set_label("Baseline")
for i in range(1,np.size(concs)):
    plotdata[i][0].set_label(str(concs[i])+r' $\mu$M') 

try:
    plotdata[(np.size(concs))][0].set_label("Rinse")
except IndexError:
    print("Final rinse is not plotted if ShowFits==True")
    

ax1.set_title(title)

ax1.legend(prop={'size': 12})




for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
    item.set_fontsize(20)


    

plt.savefig(dire+fname+'.pdf')
plt.savefig(dire+fname+'.png')

ax1.set_title(title)

FitToLangmuir(concs,pixels,errors,title)
