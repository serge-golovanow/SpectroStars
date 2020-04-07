
import pickle
import hashlib
import os, math
from datetime import datetime
import pytz
from pytz import timezone
from timezonefinder import TimezoneFinder 
from astropy.time import Time
import re
from astropy import units as u
from astropy.coordinates import  SkyCoord, EarthLocation, AltAz, Angle
from astroquery.mpc import MPC

import configparser
cfg = configparser.ConfigParser()
cfg.read('config.ini')
cachedir = cfg.get('spectrostars','cachedir',fallback=None)
googleapikey = cfg.get('spectrostars','googleapikey',fallback=None)

class Observer:
    def __init__(self,obsplace,localtime):
        obs = None
        md5 = hashlib.md5()
    
        if (obsplace.lower() == "ohp"): obsplace="511" #spécial OHP
    
        md5.update(obsplace.encode('utf-8'))
        md5place = 'place-'+md5.hexdigest()

        if cachedir is not None and os.path.isfile(cachedir+md5place):   #si possible, chargement depuis un pickle
            try:
                obs = pickle.load(open(cachedir+md5place, 'rb'))
            except:
                pass
    
        if (obs is None and re.match(r'^[A-Za-z0-9][0-9]{2}$',obsplace)):
            try:
                mpc = MPC.get_observatory_location(obsplace.upper())
                lon = float(mpc[0].to_string(decimal=True))
                if lon>180: lon = -(360-lon) #convert 0->360 to -180->180
                lat = math.atan((mpc[2]/mpc[1]/0.99330546)) /math.pi * 180
                obsplace = str(lat)+", "+str(lon)
            except:
                obs = None   

        if (obs is None):
            try:
                obs = EarthLocation.of_address(address=obsplace,get_height=(googleapikey!=None),google_api_key=googleapikey)
            except:
                obs = None 

        if (obs is None and re.match(r'^[0-9\.]+, ?[0-9\.]+',obsplace)):    #from coordinates
            try:
                latlon = Angle(obsplace.split(','),u.deg)
                altitude = 250 # can be hard-coded here until I do something else...
                obs = EarthLocation.from_geodetic(latlon[1],latlon[0],altitude)
            except:
                obs = None

        if (cachedir is not None and obs is not None and not os.path.isfile(cachedir+md5place)):   #saving in a pickle
            try:
                pickle.dump(obs, open(cachedir+md5place, 'wb'))
            except:
                pass
        
        self.place =  obs
        if obs is None: 
            return None  

        tzf = TimezoneFinder()
        try:
            tz = pytz.timezone(tzf.timezone_at(lng=float(obs.lon.to_string(decimal=True)), lat=float(obs.lat.to_string(decimal=True))))
        except:
            tz = None
        self.tz = tz

        obsdatetime = datetime.strptime(localtime, '%Y-%m-%d %H:%M')#.astimezone(timezone(tz))
        obsdatetime = tz.localize(obsdatetime)
        obsdatetime = obsdatetime.astimezone(pytz.utc)  
        obsdatetime = Time(obsdatetime.strftime('%Y-%m-%d %H:%M'))

        self.time = obsdatetime

        self.frame = AltAz(obstime=obsdatetime,location=obs)

    def html(self):
        return (
            '<a target="_blank" href="https://www.openstreetmap.org/#map=15/' + self.place.lat.to_string(decimal=True) + '/' + self.place.lon.to_string(decimal=True) + '">Observer:</a> '
            + 'lat=<abbr title="' + self.place.lat.to_string(decimal=True) + '">' + self.place.lat.to_string(precision=0) + '</abbr>, '
            + 'lon=<abbr title="' + self.place.lon.to_string(decimal=True) + '">' + self.place.lon.to_string(precision=0) + '</abbr>, '
            + 'alt=' + str(round(float(self.place.height/u.m))) + 'm, '
            + '<abbr title="TimeZone">tz</abbr>=' + str(self.tz) + ', '
            + str(self.time).replace(':00.000','') + ' UTC'
        )

    def txt(self):
        return (
            'Observer: lat=' + self.place.lat.to_string(precision=0)
            + ', lon=' + self.place.lon.to_string(precision=0)
            + ', alt=' + str(round(float(self.place.height/u.m))) + 'm'
            + ', tz=' + str(self.tz)
            + ', ' + str(self.time).replace(':00.000','') + ' UTC'        
        )
