import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *

#Specify data directory, plot title
dire = "./data/"
title = "Myr Nef on 70:30 POPC:POPG @ 8% and 2.5% Glycerol"

#Specify measured concentrations in micromolar (first should be zero for baseline)
concs = np.array([0,0.128,0.250,0.509,1.010,2.016,3.972])

data = loader(dire)

#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"

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
ax1.legend(prop={'size': 12},loc=0)

ax1.grid(axis='y',alpha=0.4)

#Set the font size of labels
for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
    item.set_fontsize(16)

###Adding text or arrow annotations to plot
#ax1.annotate("2.0" + r' $\mu$$M$' + " \novernight",(315,20),fontsize=14)
#ax1.annotate(" ",xytext=(330,20),xy = (330,13),arrowprops=dict(facecolor='black',shrink=0.05,width=1,headwidth=5))
#ax1.annotate(" ",xytext=(330,21),xy = (330,29),arrowprops=dict(facecolor='black',shrink=0.05,width=1,headwidth=5))

#Adds date below the plot
ax1.annotate('Date of Exp: 20181003', (0,0), (0, -50), xycoords='axes fraction', textcoords='offset points', va='top')

plt.savefig(fname+'.pdf')
plt.savefig(name+'.png')

#FitToLangmuir(concs,pixels,errors,title)
