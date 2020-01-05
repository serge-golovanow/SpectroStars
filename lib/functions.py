from astropy import units as u
from astropy.coordinates import  SkyCoord, AltAz, Angle

def azToDirection(az): #azimut to direction
    az = float(az)
    if (az >=360): az -= 360
    if (az <0): az += 360
    if (az >= 0 and az < 22.5) or (az >= 337.5 and az < 360): lettre='North'
    elif az >= 22.5 and az < 67.5:  lettre='North-East'
    elif az >= 67.5 and az < 112.5:  lettre='East'
    elif az >= 112.5 and az < 157.5:  lettre='South-East'
    elif az >= 157.5 and az < 202.5:  lettre='South'
    elif az >= 202.5 and az < 247.5:  lettre='South-West'
    elif az >= 247.5 and az < 292.5:  lettre='West'
    elif az >= 292.5 and az < 337.5:  lettre='North-West'
    return lettre

def SpTypeInPickles(insptype):
    #sptype = insptype.lower()
    sptype = re.search(r'[OBA]\d+[IV]+s?[a-z]*',insptype.replace(' ',''))
    if sptype: sptype=sptype.group()
    else: return insptype
    picklesdb = ['o5v', 'o8iii', 'o9v', 'a0i', 'a0iii', 'a0iv', 'a0v', 'a2i', 'a2v', 'a3iii', 'a3v', 'a47iv', 'a5iii', 'a5v', 'a7iii', 'a7v', 'b0i', 'b0v', 'b12iii', 'b1i', 'b1v', 'b2ii', 'b2iv', 'b3i', 'b3iii', 'b3v', 'b57v', 'b5i', 'b5ii', 'b5iii', 'b6iv', 'b8i', 'b8v', 'b9iii', 'b9v']
    if sptype.lower() in picklesdb: return '<abbr class="good" title="The spectral type '+sptype.upper()+' is in the Pickles Library of Stellar Spectra">'+insptype+'</abbr>'
    else: return insptype

def starload(star,target,maxseparation,altaz): #Compute an OrderedDict : separation, alt, az
    #try:
    maxebv = 5
    star['Name'] = star['Name'].strip()
    if (star['EB-V'] is None or float(star['EB-V'])<0): star['EB-V'] = '0'
    if (maxebv is not None and float(star['EB-V']) > maxebv): return None #maximum Eb-v
    star['Sky'] = SkyCoord(star['RA_dec'], star['de_dec'], unit='deg')
    if (not Angle(star['de_dec']+'d').is_within_bounds((target.sky.dec.deg -maxseparation)*u.deg,(target.sky.dec.deg+maxseparation)*u.deg)): return None
    star['Separation'] = target.sky.separation(star['Sky']).deg
    if star['Separation']>maxseparation: return None
    altaz = star['Sky'].transform_to(altaz)
    star['Alt'] = float(altaz.alt.to_string(decimal=True))
    star['Az']  = float(altaz.az.to_string(decimal=True))
    if (star['Alt']<=-10): return None
    star['Delta'] = star['Alt'] - target.alt
    star['secz'] = float(altaz.secz)
    if len(star['B-V'])>5: star['B-V'] = str(round(float(star['B-V']),3))
    #except:
        #return None
    return star
