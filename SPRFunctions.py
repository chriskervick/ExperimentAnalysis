
# coding: utf-8
import numpy as np
from matplotlib import pyplot as plt
#get_ipython().magic("config InlineBackend.figure_format = 'retina'")
from scipy.optimize import curve_fit
from scipy.interpolate import *
import os


### This loads in every .txt file in the specified path
### It is slightly hardcoded for the specific data format produced by SPRAria, but should be easily
### changeable to other formats
def loader(adir):
    i = 0
    names = os.listdir(adir)
    d = {}
    for i in range(0,np.size(names)):
        #print(names[i])
        if names[i][-4:] == ".txt":
            try:
                d[str(names[i][:-4])] = np.loadtxt(adir+str(names[i]),skiprows=1,usecols=(0,3))
            except IndexError:
                print("Data file "+str(names[i])+" did not contain SPR data")
            except ValueError:
                print("Data file "+str(names[i])+" did not contain SPR data")
    #print("FINISHED LOADING")
    #print(d)
    return(d)



### This produces two plots:
### The first is the SPR curve for the files "conc0", "conc1" up to "conc(num)" which you specify /
### when calling the function, and then plots "rinse" at the end.
### "conc" and "rinse" are the default names but can be passed as arguments to the function
### The second plot is the same as the first but with the addition of splines for each concentration.
### The equilibrium pixel valu for each concentration is then taken as the end value of each spline
### The function then returns these pixel values for each concentraion, along with an error which is /
### the width of the grey regions around each spline
### The second plot is to visually confirm that the splines are reasonable. If not, you can change the /
### value of the smoothing parameter from it's default of 10

def Organise(d,num,filename="conc",rinsename="rinse",smoothing=10,CalcFits=False):


    plt.figure(figsize=(14,10))


    for j in range(0,np.size(d[filename+'0'][:,0])):
        d[filename+'0'][j][0] = d[filename+'0'][j][0] - d[filename+'0'][-1][0]

    for i in range(0,num):
        #print(d[filename+str(i+1)][-1,0])
        #print(d[filename+str(i)][-1,0])
        #print(np.size(d[filename+str(i+1)]))
        if np.size(d[filename+str(i+1)])!=0:
            #print(np.size(d[filename+str(i+1)]))

            for j in range(0,np.size(d[filename+str(i+1)][:,0])):
                #print(j)
                if np.size(d[filename+str(i)])!=0:
                    d[filename+str(i+1)][j][0] =d[filename+str(i+1)][j][0] + d[filename+str(i)][-1][0]
                else:
                    d[filename+str(i+1)][j][0] =d[filename+str(i+1)][j][0] + d[filename+str(i-1)][-1][0] + 60*10
        #print(d[filename+str(i+1)][-1][0])
    try:
        for j in range(0,np.size(d[rinsename][:,0])):
            d[rinsename][j][0] =d[rinsename][j][0] + d[filename+str(num)][-1][0]
    except KeyError:
        print("No rinse file present")
        rinse = False
    d2 = {}
    errors = np.zeros(num+1)
    pixels = np.zeros(num+1)
    if CalcFits==True:
        for i in range(0,num+1):
            #print(i)
            #print(np.size(d[filename+str(i)]))
            if np.size(d[filename+str(i)])!=0:
                temparray = np.zeros(np.shape(d[filename+str(i)]))
                errors[i] = np.max(d[filename+str(i)][-50:,1]) - np.min(d[filename+str(i)][-50:,1])
                f = UnivariateSpline(d[filename+str(i)][:,0]/60, d[filename+str(i)][:,1], s=smoothing)
                temparray[:,0] = d[filename+str(i)][:,0]/60
                temparray[:,1] = f(d[filename+str(i)][:,0]/60)
                d2[filename+str(i)] = temparray
                pixels[i] = d2[filename+str(i)][-1,1] - d2[filename+"0"][-1,1]
    #print("ALL DONE")
    return(d,d2,pixels,errors)



def Plotter(fig1, ax1,d,d2,pixels,errors,num,filename="conc",rinsename="rinse",ShowFits = False,isColorless = False,rinselimit = 0,linewidth=1,alpha=1):
    plotdata1 = []
    plotfits = []
    plt.rcParams.update({'axes.titlesize': 30})

    import SPRColor

    colordict=SPRColor.GetColors()
    colors=colordict[num]
    if isColorless == True:
        colors = np.array(['#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591','#929591',])
    baseline = d[filename+'0'][-1,1]

    if ShowFits==False:
        for i in range(0,num+1):
            #print(i)
            if np.size(d[filename+str(i)])!=0:
                plotdata1.append(ax1.plot(d[filename+str(i)][:,0]/60,d[filename+str(i)][:,1]-baseline,label=filename+str(i),color=colors[i],linewidth=linewidth,alpha=alpha))
        if rinselimit == 0:
            try:
                plotdata1.append(ax1.plot(d[rinsename][:,0]/60,d[rinsename][:,1]-baseline,label=rinsename,color=colors[num+1],linewidth=linewidth,alpha=alpha))
            except KeyError:
                print("No rinse file present")
        else:
            plotdata1.append(ax1.plot(d[rinsename][:rinselimit,0]/60,d[rinsename][:rinselimit,1]-baseline,label=rinsename,color=colors[num+1],linewidth=linewidth,alpha=alpha))
    else:
         for i in range(0,num+1):
            if np.size(d[filename+str(i)])!=0:
                plotdata1.append(ax1.plot(d[filename+str(i)][:,0]/60,d[filename+str(i)][:,1],label=filename+str(i),color=colors[i]))
                plotfits.append(ax1.plot(d2[filename+str(i)][:,0],d2[filename+str(i)][:,1],color='black',linewidth=3))
                plotfits.append(ax1.fill_between(d2[filename+str(i)][:,0],d2[filename+str(i)][:,1]-errors[i]/2,d2[filename+str(i)][:,1]+errors[i]/2,color='gray',edgecolor='black',alpha=0.4))
                plotfits.append(ax1.plot(d2[filename+str(i)][:,0],d2[filename+str(i)][:,1],color='white',linewidth=1))



    ax1.set_title("Title goes here")

    ax1.set_ylabel("SPR Response (pixels)")
    ax1.set_xlabel("Time (minutes)")


    return(fig1,ax1,plotdata1,plotfits)



def Langmuir(concs,bmax,kd):
    return (concs*bmax)/(concs+kd)
def DimerLangmuir(concs,c1,c2,scale):
    return scale*(c1*concs + 2*concs**2)/(c2 + c1*concs + concs**2)


def FitToLangmuir(concs,pixels,errors):
    popt, popv = curve_fit(Langmuir,concs,pixels,sigma=errors,bounds=(0,[100,100]))
    plt.figure(figsize=(10,8))
    plt.errorbar(concs,pixels,yerr=errors/2,fmt='o')
    c2 = np.arange(0.01,1000,0.01)
    plt.plot(c2,Langmuir(c2,*popt))
    plt.title("Langmuir Binding Curve")
    plt.xscale('log')
    plt.ylabel("R_eq")
    plt.xlabel("Concentration (um)")
    string = "bmax = " + str(popt[0])+" +- "+str(np.sqrt(popv[0][0])) + "\n" + "kd = " + str(popt[1])+" +- "+str(np.sqrt(popv[1][1]))
    #plt.text(0.4, 1.4, string, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,bbox=dict(facecolor='red', alpha=0.2))
    plt.show()

    print("bmax = ",str(popt[0])+" +- "+str(np.sqrt(popv[0][0])))
    print("kd = ",str(popt[1])+" +- "+str(np.sqrt(popv[1][1])))

def FitToDimerLangmuir(concs,pixels,errors):
    popt, popv = curve_fit(DimerLangmuir,concs,pixels,sigma=errors,bounds=(0,[10000,100000,10000]))
    plt.figure(figsize=(10,8))
    plt.errorbar(concs,pixels,yerr=errors/2,fmt='o')
    c2 = np.arange(0.01,1000,0.01)
    plt.plot(c2,DimerLangmuir(c2,*popt))
    plt.title("Langmuir Dimer Binding Curve")
    plt.xscale('log')
    plt.ylabel("R_eq")
    plt.xlabel("Concentration (um)")
    string = "bmax = " + str(popt[0])+" +- "+str(np.sqrt(popv[0][0])) + "\n" + "kd = " + str(popt[1])+" +- "+str(np.sqrt(popv[1][1]))
    #plt.text(0.4, 1.4, string, horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,bbox=dict(facecolor='red', alpha=0.2))
    plt.show()

    print("c1 = ",str(popt[0])+" +- "+str(np.sqrt(popv[0][0])))
    print("c2 = ",str(popt[1])+" +- "+str(np.sqrt(popv[1][1])))
    print("scale = ",str(popt[2])+" +- "+str(np.sqrt(popv[2][2])))
