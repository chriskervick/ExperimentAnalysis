import numpy as np


def GetColors():
    
    blue = '#069af3'
    red = '#fd3c06'
    crimson = '#be013c'
    black = '#000000'
    teal = '#53fca1'
    purple = '#c875c4'
    yellow = '#f5bf03'
    orange = '#fb7d07'
    grey = '#929591'
    turquoise = '#06c2ac'
    
    colordict = {}
    
    colordict[1] = np.array([black,red,grey])
    colordict[2] = np.array([black,red,purple,grey])
    colordict[3] = np.array([black,red,purple,blue,grey])
    colordict[4] = np.array([black,red,yellow,purple,blue,grey])
    colordict[5] = np.array([black,red,yellow,purple,turquoise,blue,grey])
    colordict[6] = np.array([black,red,orange,yellow,purple,turquoise,blue,grey])
    colordict[7] = np.array([black,red,orange,yellow,purple,teal,turquoise,blue,grey])
    colordict[8] = np.array([black,crimson,red,orange,yellow,purple,teal,turquoise,blue,grey])
    return(colordict)


#colors=np.array(['xkcd:purple','xkcd:rose red','xkcd:red orange','xkcd:pumpkin orange','xkcd:golden','xkcd:orchid','xkcd:sea green','xkcd:turquoise','xkcd:azure','xkcd:slate','black'])
