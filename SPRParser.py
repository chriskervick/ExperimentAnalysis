import numpy as np
from matplotlib import pyplot as plt
from SPRFunctions import *
import matplotlib
import argparse


#THE DIRECTORY WITH ALL THE DATA GOES HERE
parser = argparse.ArgumentParser()
#parser.add_argument('-title',nargs='*',action = 'append')
parser.add_argument('-title',nargs='*')
parser.add_argument('-d')
parser.add_argument('-f')
parser.add_argument('-cname')
parser.add_argument('-rname')
parser.add_argument('--concs',nargs='*',type=float)

args = parser.parse_args()
print(args)


dire = args.d
fname = args.f
filename=args.cname
rinsename = args.rname
concs = np.array(args.concs)
title=' '.join(args.title)
#dire = "../NefSummer2018/Nef091218/"
#fname = "7030POPCPOPG_091218_COMPARISON"
data = loader(dire)
#Choose what the default filenames are:
#rinsename = "rinse"
#filename = "conc"
#title = "Myr Nef on 70:30 POPC:POPG @ 8% and 2.5% Glycerol"

#concs = np.array([0,0.128,0.250,0.509,1.010,2.016,3.972])
num = np.size(concs) - 1
(data,fits,pixels,errors) = Organise(data,num,smoothing=5,filename = filename,CalcFits=True)
fig1 = plt.figure(figsize=(14,10))
ax1 = fig1.add_subplot(1, 1, 1)
(fig1,ax1,plotdata,plotfits) = Plotter(fig1,ax1,data,fits,pixels,errors,num,concs,title=title,filename=filename,ShowFits=False,rinselimit=0,annotate=False)

#Chris Autodate
ax1.annotate("Date of Exp: "+fname[0:6], (0,-0.1), xycoords='axes fraction')
#Dennis Autodate
#ax1.annotate("Date of Exp: "+fname[4:12], (0,-0.1), xycoords='axes fraction')

plt.savefig(dire+fname+'.pdf')
plt.savefig(dire+fname+'.png')
plt.savefig("../AllData/"+fname+'.pdf')
plt.savefig("../AllData/"+fname+'.png')


#FitToLangmuir(concs,pixels,errors,dire,fname)
FitToDimerAndSingleLangmuir(concs,pixels,errors,dire,fname)
