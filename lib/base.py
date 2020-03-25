import csv,os,math,urllib.parse
from lib.functions import *
from joblib import Parallel, delayed
from lib.display import *

class Base:
    def __init__(self,filename):
        self.target = ''
        if not os.path.isfile(filename): 
            print("Can't find CSV file !")
            exit(1)
        self.dict = []
        self.nearbase = None
        with open(filename, newline='\n') as csvfile:    #test : csv mal formaté
            csvbase = csv.DictReader(csvfile, delimiter=',')
            for row in csvbase:
                self.dict.append(row)

    
    def near(self,target,maxseparation,obs):
        self.target = target
        self.obs = obs

        #self.nearbase = Parallel(n_jobs=-1,backend="multiprocessing",verbose=0)(delayed(starload)(star,target,maxseparation,frame) for star in self.dict)
        self.nearbase = list(filter(None,Parallel(n_jobs=-1,backend="multiprocessing",verbose=0)(delayed(starload)(star,target,maxseparation,obs.frame) for star in self.dict)))
        #self.nearbase = list(filter(None,[starload(star,target,maxseparation,frame) for star in self.dict]))   #without joblib.Parallel
        self.nearbase = sorted(self.nearbase, key=lambda item: math.fabs(item['Delta']))

    def html(self):
        text = '<table id="stars"><thead><tr><th><abbr title="Click a result to see alt/az over time">#</abbr></th><th><abbr title="Link to SIMBAD">Star</abbr></th><th><abbr title="Separation from target in degrees">Sep</abbr></th><th><abbr title="V band magnitude">VMag</abbr></th><th><abbr title="Right ascension">RA</abbr></th><th><abbr title="Declinaison">Dec</abbr></th><th><abbr title="Height above horizon in degrees (90°=zenith)">Height</abbr></th><th><abbr title="Δ height above horizon with target">ΔH</abbr></th><th><abbr title="Color index">B-V</abbr></th><th><abbr title="how do I translate  excès de couleur  ?!">E<sub>(B-V)</sub></abbr></th><th><abbr title="Object type">OType</abbr></th><th><abbr title="Spectral type">SpType</abbr></th><th><abbr title="Medium resolution INT Library of Empirical Spectra">Miles</abbr></th></tr></thead>'
        line=1
        for star in self.nearbase:
            text = text + ('\n\t<tr>'
                + '<td>'+str(line).zfill(2)+'</td>' 
                + Name(star['Name']).html(star['CDSName'],star['SAO']) 
                + Separation(star['Separation']).html() 
                + VMag(star['V']).html() 
                + RADec(star['Sky']).html()
                + Alt(star['Alt']).html(star['secz'],star['Az'])
                + Delta(star['Delta']).html()
                + BV(star['B-V']).html()
                + EBV(star['EB-V']).html()
                + OType(star['OType']).html()
                + SPType(star['Sp']).html()
                + Miles(star['Miles']).html()
            +'</tr>')
            line+=1
        text = text + '\n</table>'
        return text
    
    def txt(self):
        line=1
        text = '##  Star:\tSep:\tVMag:\tRA:\t  Dec:\t\tHeight:\t\tB-V:\tEb-v:\tSpTy:\tMiles:'
        for star in self.nearbase:
            text = text + ( "\n"
                + str(line).zfill(2)
                + "  " + Name(star['Name']).txt()
                + "\t" + Separation(star['Separation']).txt()
                + "\t" + VMag(star['V']).txt()
                + "\t" + RADec(star['Sky']).txt()
                + "\t" + Alt(star['Alt']).txt()
                + ", Δh=" + Delta(star['Delta']).txt()
                + "\t" + BV(star['B-V']).txt()
                + "\t" + EBV(star['EB-V']).txt()
                + "\t" + SPType(star['Sp']).txt()
                #+ "\t " + str(round(star['secz'],2))
                + "\t" + Miles(star['Miles']).txt()
            )
            line += 1
        return text
