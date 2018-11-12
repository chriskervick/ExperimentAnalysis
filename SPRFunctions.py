
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



def Plotter(fig1, ax1,d,d2,pixels,errors,num,concs,title="Blank",filename="conc",rinsename="rinse",ShowFits = False,rinselimit = 0,linewidth=1,alpha=1,legend=True,annotate=False):
    plotdata1 = []
    plotfits = []
    plt.rcParams.update({'axes.titlesize': 30})

    import SPRColor
 
    colordict=SPRColor.GetColors()
    colors=colordict[num]
 
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


    
    ax1.set_title(title)
    ax1.set_ylabel("SPR Response (pixels)")
    ax1.set_xlabel("Time (minutes)")

    if legend==True:
        plotdata1[0][0].set_label("Baseline")
        for i in range(1,np.size(concs)):
            plotdata1[i][0].set_label(str(concs[i])+r' $\mu$M') 
        try:
            plotdata1[(np.size(concs))][0].set_label("Rinse")
        except IndexError:
            print("Final rinse is not plotted if ShowFits==True")
        ax1.legend(fontsize=16)    
        
    if annotate==True:
        #####Attempt at autolabelling of data on plot
        baseline = d[filename+'0'][-1,1]
        maxt=d[filename+str(num)][-1][0]
        maxR=d[filename+str(num)][-1][1]
        for i in range(1,num + 1):
            timecenter = (d[filename+str(i)][0,0] + d[filename+str(i)][-1,0] )/2
            timecenterindex = int(np.floor(np.size(d[filename+str(i)][:,0])/2))
            print(timecenter)
            print(d[filename+str(i)][timecenterindex,1])
            ax1.annotate(str(concs[i])+r' $\mu$M', xy=(timecenter/60,d[filename+str(i)][timecenterindex,1]-baseline),xytext=(timecenter/60 + 0.05*maxt/60,d[filename+str(i)][timecenterindex,1]-baseline - (maxR-baseline)*0.05),arrowprops=dict(arrowstyle='->'))



    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
                 ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(20)



    return(fig1,ax1,plotdata1,plotfits)



def Langmuir(concs,bmax,kd):
    return (concs*bmax)/(concs+kd)
def DimerLangmuir(concs,c1,c2,scale):
    return scale*(c1*concs + 2*concs**2)/(c2 + c1*concs + concs**2)


def FitToLangmuir(concs,pixels,errors,dire,fname):
    spopt, spopv = curve_fit(Langmuir,concs,pixels,sigma=errors,bounds=(0,[10000,10000]))
    fig1 = plt.figure(figsize=(10,8))
    ax1 = fig1.add_subplot(1, 1, 1)
    plt.errorbar(concs,pixels,yerr=errors/2,fmt='o',color='orange',label='Data')
    c2 = np.arange(0.01,1000,0.01)
    ax1.plot(c2,Langmuir(c2,*spopt),color='red',label='Langmuir Model')
    ax1.set_title("Langmuir Binding Curve")
    ax1.set_xscale('log')
    ax1.set_ylabel("Response")
    ax1.set_xlabel(r'Concentration ($\mu M$)')
    s_string = r'$\beta_{max}$ = ' + str(round(spopt[0],2))+r'$\pm$'+str(round(np.sqrt(spopv[0][0]),2)) + "\n" + r'$k_d$ = ' + str(round(spopt[1],2))+r'$\pm$' +str(round(np.sqrt(spopv[1][1]),2))
    ax1.text(0.2, 0.475, s_string, horizontalalignment='center',verticalalignment='top', transform=ax1.transAxes,bbox=dict(facecolor='red', alpha=0.2))

    ax1.legend(loc=2,fontsize=16)

    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(20)

    plt.savefig(dire+fname + '_binding.pdf')
    plt.savefig(dire+fname + '_binding.png')
    #plt.savefig("../AllData/"+fname + '_binding.pdf')
    #plt.savefig("../AllData/"+fname + '_binding.png')


def FitToDimer(concs,pixels,errors,dire,fname):
    dpopt, dpopv = curve_fit(DimerLangmuir,concs,pixels,sigma=errors,bounds=(0,[10000,100000,10000]))
    fig1 = plt.figure(figsize=(10,8))
    ax1 = fig1.add_subplot(1, 1, 1)
    plt.errorbar(concs,pixels,yerr=errors/2,fmt='o',color='orange',label='Data')
    c2 = np.arange(0.01,1000,0.01)
    ax1.plot(c2,DimerLangmuir(c2,*dpopt),color='blue',label='Dimer Model')
    ax1.set_title("Dimer Binding Curve")
    ax1.set_xscale('log')
    ax1.set_ylabel("Response")
    ax1.set_xlabel(r'Concentration ($\mu M$)')
    d_string = r'$c_1$ = ' + str(round(dpopt[0],2))+r'$\pm$'+str(round(np.sqrt(dpopv[0][0]),2)) + "\n" + r'$c_2$ = ' + str(round(dpopt[1],2))+r'$\pm$' +str(round(np.sqrt(dpopv[1][1]),2)) + "\n" + 'Scale = ' + str(round(dpopt[2],2))+r'$\pm$' +str(round(np.sqrt(dpopv[2][2]),2))
    ax1.text(0.2, 0.5, d_string, horizontalalignment='center',verticalalignment='bottom', transform=ax1.transAxes,bbox=dict(facecolor='blue', alpha=0.2))

    ax1.legend(loc=2,fontsize=16)

    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(20)

    plt.savefig(dire+fname + '_binding.pdf')
    plt.savefig(dire+fname + '_binding.png')
    #plt.savefig("../AllData/"+fname + '_binding.pdf')
    #plt.savefig("../AllData/"+fname + '_binding.png')


    print("c1 = ",str(dpopt[0])+" +- "+str(np.sqrt(dpopv[0][0])))
    print("c2 = ",str(dpopt[1])+" +- "+str(np.sqrt(dpopv[1][1])))
    print("scale = ",str(dpopt[2])+" +- "+str(np.sqrt(dpopv[2][2])))


def FitToDimerAndSingleLangmuir(concs,pixels,errors,dire,fname):
    dpopt, dpopv = curve_fit(DimerLangmuir,concs,pixels,sigma=errors,bounds=(0,[10000,100000,10000]))
    spopt, spopv = curve_fit(Langmuir,concs,pixels,sigma=errors,bounds=(0,[2*dpopt[2],10000]))
    fig1 = plt.figure(figsize=(10,8))
    ax1 = fig1.add_subplot(1, 1, 1)
    plt.errorbar(concs,pixels,yerr=errors/2,fmt='o',color='orange',label='Data')
    c2 = np.arange(0.01,1000,0.01)
    ax1.plot(c2,DimerLangmuir(c2,*dpopt),color='blue',label='Dimer Model')
    ax1.plot(c2,Langmuir(c2,*spopt),color='red',label='Single Ligand Model')
    ax1.set_title("Langmuir/Dimer Binding Curve")
    ax1.set_xscale('log')
    ax1.set_ylabel("Response")
    ax1.set_xlabel(r'Concentration ($\mu M$)')
    s_string = r'$\beta_{max}$ = ' + str(round(spopt[0],2))+r'$\pm$'+str(round(np.sqrt(spopv[0][0]),2)) + "\n" + r'$k_d$ = ' + str(round(spopt[1],2))+r'$\pm$' +str(round(np.sqrt(spopv[1][1]),2))
    ax1.text(0.2, 0.475, s_string, horizontalalignment='center',verticalalignment='top', transform=ax1.transAxes,bbox=dict(facecolor='red', alpha=0.2))

    d_string = r'$c_1$ = ' + str(round(dpopt[0],2))+r'$\pm$'+str(round(np.sqrt(dpopv[0][0]),2)) + "\n" + r'$c_2$ = ' + str(round(dpopt[1],2))+r'$\pm$' +str(round(np.sqrt(dpopv[1][1]),2)) + "\n" + 'Scale = ' + str(round(dpopt[2],2))+r'$\pm$' +str(round(np.sqrt(dpopv[2][2]),2))
    ax1.text(0.2, 0.5, d_string, horizontalalignment='center',verticalalignment='bottom', transform=ax1.transAxes,bbox=dict(facecolor='blue', alpha=0.2))

    ax1.legend(loc=2,fontsize=16)

    for item in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label] +
             ax1.get_xticklabels() + ax1.get_yticklabels()):
        item.set_fontsize(20)

    plt.savefig(dire+fname + '_binding.pdf')
    plt.savefig(dire+fname + '_binding.png')
    #plt.savefig("../AllData/"+fname + '_binding.pdf')
    #plt.savefig("../AllData/"+fname + '_binding.png')


    print("c1 = ",str(dpopt[0])+" +- "+str(np.sqrt(dpopv[0][0])))
    print("c2 = ",str(dpopt[1])+" +- "+str(np.sqrt(dpopv[1][1])))
    print("scale = ",str(dpopt[2])+" +- "+str(np.sqrt(dpopv[2][2])))




