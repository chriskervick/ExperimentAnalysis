import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *
import matplotlib

#THE DIRECTORY WITH ALL THE DATA GOES HERE

dire = "../NefSummer2018/Nef091218/"
fname = "7030POPCPOPG_091218_COMPARISON"
data = loader(dire)
#Choose what the default filenames are:
rinsename = "rinse"
filename = "conc"
title = "Myr Nef on 70:30 POPC:POPG @ 8% and 2.5% Glycerol"

concs = np.array([0,0.128,0.250,0.509,1.010,2.016,3.972])
num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5,filename = filename,CalcFits=True)
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,concs,title=title,filename=filename,ShowFits=False,rinselimit=0)


plt.savefig(dire+fname+'.pdf')
plt.savefig(dire+fname+'.png')


#FitToLangmuir(concs,pixels,errors)
FitToDimerAndSingleLangmuir(concs,pixels,errors,dire,fname)
