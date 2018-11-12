# ExperimentAnalysis

Python scripts for plotting and fitting SPR binding curves

Can either run SPR.py by editing the file to include the correct directory and filenames, or use SPRParser.py which takes command line arguments and can be used with a shell script (runallexps.sh)

Inputs are:
dire: Directory containing the files
fname: Output filename for saved figures
filename: Name of concentration files. Defaults to "conc". Reads in files conc0.txt, conc1.txt etc
rinsename: Name of rinse file. Defaults to rinse.txt
title: Title to be used for plots
concs: Array of concentrations. First entry should be 0 for baseline


Three main functions are then called, each with their own flags
________
Organise: Puts concentrations in sequential order and subtracts the baseline. Also fits the curves to get a pixel value.
Has the following optional flags:
smoothing: (float, default: 5) Smoothing parameter for fitting. Change only if the fits do not match the exp data well.
CalcFits: (Bool, default:False) Whether or not to perform the fitting. Can be switched off for speedup if Binding curve is not needed and large (e.g Overnight) data is being plotted

________
Plotter: Plots the SPR curves
Has the following optional flags:
ShowFits: (Bool, default:False) Whether to show the fits to the data on top of the data. Mainly for visual inspection to ensure the smooothing is correct, and that the end of the fit matches the end of the data, as this is where the pixel value for each concentration is extracted from
rinselimit (int, default:0) How much of the rinse to show (in seconds). If 0, it shows the entire rinse (which in retrospect is kind of dumb). Useful for if long (overnight) rinses were recorded
legend: (Bool, default:True) Whether or not to show the legend, labelled via concentrations
annotate: (Bool, default:False) Whether or not to show annotations of each curve by concentration


________
FitToLangmuir: Fits to a Langmuir curve and saves pdf and png to dire/fname
FitToDimer: Fits to a dimer saturation curve and saves pdf and png to dire/fname
FitToDimerAndSingleLangmuir: Does both of the above on the same plot for comparison



________________
Using the shell script

AllExperiments.txt should contain the inputparameters in the following format:

dire
fname
filename
rinsename
title
conc0 conc1 conc2 ...
##########################

This is then repeated (with no spaces) for each new experiment. 
Then edit the for loop in runallexps.sh to loop from 0 to N, the number of seperate experiments. 
When doing this, it may be useful to uncomment the lines which save the figures all to the same folder, in my case AllData, which makes for easier comparison
