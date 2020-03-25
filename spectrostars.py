#!/usr/bin/python3

'''
SpectroStars : Find reference stars for spectroscopy
https://github.com/serge-golovanow/SpectroStars
Copyright © 2019, Serge Golovanow

Based on an idea and the stars database from ReferenceStarFinder, made by François Teyssier

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.

Requirements installation : (astropy version >= 3.1)
# pip3 install timezonefinder pytz numpy astropy astroquery joblib
On Windows, give a try to MiniConda

v19-03-05
'''
from lib.functions import *
from lib.target import Target
from lib.observer import Observer
from lib.base import Base

#https://www.usno.navy.mil/ : USNO websites [...] are undergoing modernization efforts. The expected completion of the work and return of service is estimated as 30 April 2020.
from astropy.utils import iers
iers.conf.auto_download = False

#avoid "No known catalog could be found" warning
import warnings
warnings.filterwarnings(action="ignore")

csvfilename = 'base.csv'
#targetname = "16h41m42s +36d27m41s"
#targetname = "PNV J06095740+1212255"
#targetname = "08 10 14 22 12 16"
targetname = 'M27'
obsplacename = '586' # a place name, an IAU/MPC code, or lat,lon in degrees
obsdatetime = '2019-09-15 23:00' # YYYY-MM-DD HH:MM
maxseparation = 5 # separation in degrees

base = Base(csvfilename)  #load database in an object
observateur = Observer(obsplacename, obsdatetime)  #create observer object
cible = Target(targetname)  #create target object
cible.observe(observateur)  #observe target

print(cible.txt())
print(observateur.txt())

if cible.alt<0:
    print('Target is below the horizon!')
    exit(0)

base.near(cible,maxseparation,observateur)  #search stars near target
print(base.txt())
