import math
from astroquery.simbad import Simbad
from astroquery.mpc import MPC
from astropy import units as u
from astropy.coordinates import  SkyCoord, EarthLocation, AltAz, Angle
from lib.otypes import otypes
from lib.functions import azToDirection


class Target:

    def __init__(self,name):
        self.name = name
        try:
            mySimbad = Simbad()
            mySimbad.add_votable_fields('otype')            
            CDS = mySimbad.query_object(self.name)
        except:
            CDS = None

        if CDS is not None: #objet trouvé dans SIMBAD, avec les infos qui vont bien
            self.ra = Angle(CDS['RA'][0],u.hourangle)
            #print(str(self.ra))
            self.dec = Angle(CDS['DEC'][0],u.deg)
            self.mainid = str(CDS['MAIN_ID'][0])#.decode("utf-8"))
            self.otype =  str(CDS['OTYPE'][0])#.decode("utf-8"))
            self.sky = SkyCoord(self.ra,self.dec, unit=(u.hourangle, u.deg))
            self.const = self.sky.get_constellation()
            return  #fini !

        if CDS is None:
            try:
                CDS = SkyCoord.from_name(self.name,parse=True)
            except:
                try:
                    CDS = SkyCoord(self.name)
                except:
                    pass

        if CDS is None: 
            self.sky = None
            return None #on ne peut plus rien faire d'autre

        self.sky = CDS
        self.mainid = 'Unknown'
        self.otype = 'Unknown'
        self.ra = Angle(float(CDS.to_string(style='decimal').split(' ')[0]),u.degree)
        self.dec = Angle(float(CDS.to_string(style='decimal').split(' ')[1]),u.degree)
        self.const = CDS.get_constellation()       

    def observe(self,observer):
        self.altaz = self.sky.transform_to(observer.frame) #observer = place & date
        self.alt = float(self.altaz.alt.to_string(decimal=True))
        self.az = float(self.altaz.az.to_string(decimal=True))
        self.secz = float(self.altaz.secz)

    def html(self):
        text = (
            '<a target="_blank" href="http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+self.name+'">Target: '+self.mainid+'</a> ('
            + self.sky.to_string(style='hmsdms',precision=0) + ', '
            + otypes[self.otype]
            + ' in ' + self.const + '), '
            + 'altitude=' + str(round(self.alt,1)) + '°, '
            + 'azimuth=<abbr title="'+azToDirection(self.az)+'">' + str(int(self.az)) + '°</abbr>'
        )
        if self.alt>0: text = text + ', <abbr title="secant(z)">airmass</abbr>=' + str(round(self.secz,3))
        return text

    def txt(self):
        return (
            'Target: '+self.mainid
            + ' (' + self.sky.to_string(style='hmsdms',precision=0) + ', '
            + otypes[self.otype]
            + ' in ' + self.const + '), '
            + 'altitude=' + str(round(self.alt,1)) + '°, '
            + 'azimuth=' + str(int(self.az)) + '°, '
            + 'airmass=' + str(round(self.secz,3))
        )

    def xml(self):
        coords = self.sky.to_string()
        hmsdmscoords = self.sky.to_string(style='hmsdms',precision=0)
        return (
            '<target>'
            + ' <name>' + self.mainid + '</name>'
            + ' <ra hms="' + hmsdmscoords.split()[0] + '">' + coords.split()[0] + '</ra>'
            + ' <dec dms="' + hmsdmscoords.split()[1] + '">' + coords.split()[1] + '</dec>'
            + ' <otype fulltype="' + otypes[self.otype] + '">' + self.otype + '</otype>'
            + ' <const>' + self.const + '</const>'
            + ' <alt>' + str(self.alt) + '</alt>'
            + ' <azimuth direction="' + azToDirection(self.az) + '">' + str(self.az) + '</azimuth>'
            + '</target>'
        )