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

##################  CONFIGURATION  ###############################################################

#If the script is started without command-line parameters or not from a WSGI script, these parameters will be used :
observingtarget = '3C232'    #Target name, will be searched in SIMBAD
observingplace = 'L14'   #Observing place : name, lat,lon (in degrees, like "45.57,5.58") or IAU/MPC code
targetmaxseparation = 10  #Maximum separation from target to reference stars
maxebv = None  #Maximum Eb-v (0.1), or None
observingdate = None #YYYY-MM-DD, or None for today
observingtime = None #'HH:MM", or None for 22h (all local time)

#Cache directory, with ending  /, or None
cachedir = None

#CSV file with stars database, full (absolute) path would be better
csvfilename = 'base.csv'

#Google Api Key or None ( https://developers.google.com/maps/documentation/geocoding/get-api-key )
#If None, OSM will be used, without place altitude : https://nominatim.openstreetmap.org/
#IF you're using AstroPy version <3.1, you'll get trouble... Soon, if False, no geolocation : lat,Lon will be required
googleapikey = None

#Parallel processing of stars database ?  True or False
parallelize = True

#default values set right after modules imports
##################################################################################################

import time
import math 
import csv
import hashlib
import os
import pickle
import re
from datetime import datetime

from astropy.time import Time
from astropy import units as u
from astropy.coordinates import  SkyCoord, EarthLocation, AltAz, Angle
#from astropy.config import set_temp_cache, set_temp_config
from astroquery.mpc import MPC
if parallelize: from joblib import Parallel, delayed
import pytz
from pytz import timezone
from timezonefinder import TimezoneFinder 
tzf = TimezoneFinder()

#Timestamp in millisecond, for debuging     mark=msts()     print(''+str(msts()-mark)+'ms)
msts = lambda: int(round(time.time() * 1000))

#default values :
if observingdate is None: observingdate = datetime.now().strftime("%Y-%m-%d") #today
if observingtime is None: observingtime = '22:00'
observingdatetime = observingdate+' '+observingtime    
if targetmaxseparation>30: targetmaxseparation=30

### FUNCTIONS :

def azToDirection(az): #azimut to direction
    az = float(az)
    if (az >=360): az -= 360
    if (az <0): az += 360
    if (az >= 0 and az < 22.5) or (az >= 337.5 and az < 360): lettre='N'
    elif az >= 22.5 and az < 67.5:  lettre='NE'
    elif az >= 67.5 and az < 112.5:  lettre='E'
    elif az >= 112.5 and az < 157.5:  lettre='SE'
    elif az >= 157.5 and az < 202.5:  lettre='S'
    elif az >= 202.5 and az < 247.5:  lettre='SW'
    elif az >= 247.5 and az < 292.5:  lettre='W'
    elif az >= 292.5 and az < 337.5:  lettre='NW'
    return lettre

def starload(star,target,maxseparation,altaz): #Compute an OrderedDict : separation, alt, az
    try:
        if (float(star['EB-V'])<0): star['EB-V'] = '0'
        if (maxebv is not None and float(star['EB-V']) > maxebv): return None #maximum Eb-v
        star['Sky'] = SkyCoord(star['RA_dec'], star['de_dec'], unit='deg')
        if (not Angle(star['de_dec']+'d').is_within_bounds((target['Dec'].deg-maxseparation)*u.deg,(target['Dec'].deg+maxseparation)*u.deg)): return None
        star['Separation'] = target['Sky'].separation(star['Sky']).deg
        if star['Separation']>maxseparation: return None
        altaz = star['Sky'].transform_to(altaz)
        star['Alt'] = float(altaz.alt.to_string(decimal=True))
        if (star['Alt']<=-10): return None
        star['Delta'] = star['Alt'] - target['Alt']
        star['secz'] = float(altaz.secz)
    except:
        return None

    return star

def baseload(target,maxseparation,altaz): #Read CSV database to put it in an OrderedDict
    starbase = []
    with open(csvfilename, newline='\n') as csvfile:
        csvbase = csv.DictReader(csvfile, delimiter=',')

        if parallelize:	#Joblib.Parallel : parallelise main loop        loky multiprocessing threading
            starbase = Parallel(n_jobs=-1,backend="multiprocessing",verbose=0)(delayed(starload)(star,target,maxseparation,altaz) for star in csvbase)
        else:
            starbase = [starload(star,target,maxseparation,altaz) for star in csvbase] #old way

    return starbase

def getplace(obsplace): #returns an EarthLocation, based on place's name, lat/lon, IAU/MPC code
    obs = None
    md5 = hashlib.md5()

    md5.update(obsplace.encode('utf-8'))
    md5place = 'place-'+md5.hexdigest()

    if cachedir is not None and os.path.isfile(cachedir+md5place):   #si possible, chargement depuis un pickle
        try:
            obs = pickle.load(open(cachedir+md5place, 'rb'))
        except:
            pass

    if (obs is None and re.match(r'[A-Za-z0-9][0-9]{2}',obsplace)):
        try:
            mpc = MPC.get_observatory_location(obsplace.upper())
            lon = float(mpc[0].to_string(decimal=True))
            if lon>180: lon = -(360-lon) #convert 0-360 to -180-180
            lat = math.atan((mpc[2]/mpc[1]/0.99330546)) /math.pi * 180
            obsplace = str(lat)+", "+str(lon)
        except:
            obs = None   
            
    if (obs is None):
        try:
            obs = EarthLocation.of_address(address=obsplace,get_height=(googleapikey!=None),google_api_key=googleapikey) #lat=45*u.deg, lon=4.5*u.deg, height=390*u.m)
        except:
            obs = None 

    if (cachedir is not None and obs is not None and not os.path.isfile(cachedir+md5place)):   #saving in a pickle
        pickle.dump(obs, open(cachedir+md5place, 'wb'))

    return obs

def gettarget(targetname,altaz): #Get target coordinates from name with SIMBAD, compute alt/az
    target = None

    md5 = hashlib.md5()
    md5.update(targetname.encode('utf-8'))
    md5target = 'target-'+md5.hexdigest()
    if cachedir is not None and os.path.isfile(cachedir+md5target):   #si possible, chargement depuis un pickle
        try:
            target = pickle.load(open(cachedir+md5target, 'rb'))
        except:
            target = None

    if (target is None) :
        target = {}
        target['Name'] = targetname
        try :
            target['Sky'] = SkyCoord.from_name(targetname)
        except:
            return None
        if target['Sky'] is None: return None # ['Could not find target by reference : '+target['Name']]

        target['RA'] = Angle(float(target['Sky'].to_string(style='decimal').split(' ')[0]),u.degree)
        target['Dec'] = Angle(float(target['Sky'].to_string(style='decimal').split(' ')[1]),u.degree)
        target['Const'] = target['Sky'].get_constellation()
        #print ('Constellation en '+str(msts()-mark)+'ms')

    if (cachedir is not None and not os.path.isfile(cachedir+md5target)):
        pickle.dump(target, open(cachedir+md5target, 'wb'))

    #mark = msts()
    target['AltAz'] = target['Sky'].transform_to(altaz) #tres long à la première execution
    #print ('Target AltAz en '+str(msts()-mark)+'ms')

    target['Alt'] = float(target['AltAz'].alt.to_string(decimal=True))
    target['Az'] = float(target['AltAz'].az.to_string(decimal=True))
    target['secz'] = float(target['AltAz'].secz)

    return target

def stardisplay(num,star): # display a star
    name = star["Name"]
    separation = str(round(star['Separation'],1))+"°"
    coords = star['Sky'].to_string(style='hmsdms',precision=0)
    alt = str(round(star['Alt'])).zfill(2)+'°'
    deltaalt = str(round(star['Delta'],1))+"°"
    Vmag = star['V']
    BV = star['B-V']
    if BV=='': BV = '    '
    EBV = star['EB-V']
    if EBV is '': EBV = '\t'
    sptype = star['Sp']
    if (star['Alt']>=1): 
        decimales = 2
        if (star['secz']>=100): decimales = 1
        airmass = str(round(star['secz'],decimales))
    else: airmass = '  '
    miles = star['Miles']
    starline = str(num).zfill(2)+'  '+name+'\t'+separation+"\t"+Vmag+'\t'+coords+'\t'+alt+', Δh='+deltaalt+'\t'+BV+'\t'+EBV+'\t'+sptype+'\t '+airmass+'\t'+miles

    return starline

def gettime(tz,obsdatetime): #Returns a Time() object, UTC converted from localtime and timezone
    obsdatetime = datetime.strptime(obsdatetime, '%Y-%m-%d %H:%M')#.astimezone(timezone(tz))
    obsdatetime = tz.localize(obsdatetime)
    obsdatetime = obsdatetime.astimezone(pytz.utc)  
    obsdatetime = Time(obsdatetime.strftime('%Y-%m-%d %H:%M'))
    return obsdatetime

def process(targetname,maxseparation,obsplace,obsdatetime): #main routine
    displayed=[]
    if (maxseparation>30): maxseparation=30

    #Getting an EarthPlace from place's name :
    obs = getplace(obsplace)
    if (obs is None): return ['Could not find observing place '+obsplace]

    #Getting timezone for this place :
    try:
        tz = pytz.timezone(tzf.timezone_at(lng=float(obs.lon.to_string(decimal=True)), lat=float(obs.lat.to_string(decimal=True))))
    except:
        tz = None
    if (tz is None): return ['Could not find timezone']
    
    #Getting a Time, set to UTC from localtime
    try:
        obsdatetime = gettime(tz,obsdatetime)
    except:
        return ['Error while creating obsdatetime']

    #Getting an AltAz, at the observer's EarthPlace, at observer's time converted to UTC :
    try:
        altaz = AltAz(obstime=obsdatetime,location=obs)
    except:
        return ['Error while creating AltAz object']

    #Getting the target from name, processing its alt/az position
    target = gettarget(targetname,altaz)
    if (target is None): return ['Could not find target in SIMBAD']

    #Setting output, global informations :
    displayed.append('Target   : '+target['Name']+' ('+str(target['Sky'].to_string(style='hmsdms',precision=0))+', '+target['Const']+'), altitude='+str(round(target['Alt'],1))+'°, azimuth='+str(round(target['Az']))+'° ('+azToDirection(target['Az'])+'), airmass (secz)='+str(round(target['secz'],3)))
    displayed.append('Observer : lat='+obs.lat.to_string(precision=0)+', lon='+obs.lon.to_string(precision=0)+', alt='+str(round(float(obs.height/u.m)))+'m, tz='+str(tz)+', '+str(obsdatetime).replace('.000','')+' UTC')

    #Stopping here if target is below the horizon
    if (target['Alt']<0):
        displayed.append('\nTarget is below the horizon !')
        return displayed

    #Geting stars database, with separation and altaz computed :
    base = baseload(target=target,maxseparation=maxseparation,altaz=altaz)
    if (base == []): return ['Error while loading database from csv or processing it']

    #Setting final stars array
    final = []  #will contain only nearest stars
    for num, star in enumerate(base):
        if star is not None and star['Separation'] <= maxseparation and float(star['EB-V']) < 10.1 : final.append(star)

    #sorting stars by Δh :
    final = sorted(final, key=lambda item: math.fabs(item['Delta']))

    #setting table header :
    displayed.append('\n##  Star:\tSep:\tVMag:\tRA:\t  Dec:\t\tHeight:\t\tB-V:\tEb-v:\tSpType:\t secz:\tMiles:')

    #setting line for each displayed star
    line=1
    for star in final :
        displayed.append(stardisplay(line,star))
        line += 1

    #finished !
    return displayed


### MAIN PROCESS CALL :

# if it's an interactive run, let's call the main process :
if __name__ == "__main__":
    print("\n".join(process(observingtarget,targetmaxseparation,observingplace,observingdatetime)))
