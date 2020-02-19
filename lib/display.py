import math,re
from lib.otypes import otypes

picklesdb = ['o5v', 'o8iii', 'o9v', 'a0i', 'a0iii', 'a0iv', 'a0v', 'a2i', 'a2v', 'a3iii', 'a3v', 'a47iv', 'a5iii', 'a5v', 'a7iii', 'a7v', 'b0i', 'b0v', 'b12iii', 'b1i', 'b1v', 'b2ii', 'b2iv', 'b3i', 'b3iii', 'b3v', 'b57v', 'b5i', 'b5ii', 'b5iii', 'b6iv', 'b8i', 'b8v', 'b9iii', 'b9v']


class Value:
    def __init__(self,val):
        self.val=val   
    def html(self):
        return '<td>'+str(self.val)+'</td>'
    def txt(self):
        return str(self.val)

class Name(Value):
    def html(self,CDSName,SAO):
        title = ''
        if (CDSName!=self.val): title = CDSName.strip() + '&#10'
        if (SAO!=''): title = title+'SAO ' + SAO
        return '<td><abbr title="'+title+'"><a target="_blank" href="http://simbad.u-strasbg.fr/simbad/sim-basic?Ident='+self.val+'">'+self.val+'</a></abbr></td>'

class Separation(Value):
    def __init__(self,val):
        self.val=(round(val,3))    
    def txt(self):
        return str(round(self.val,1))+'°'
    def html(self):
        if round(self.val,1) >= 15: alert='class="alert" title="Very huge separation"'
        elif round(self.val,1) >= 10: alert='class="warn" title="Huge separation"'
        else: return '<td sorttable_customkey="'+str(self.val)+'">'+str(round(self.val,1))+'°</td>'
        return '<td sorttable_customkey="'+str(self.val)+'"><abbr '+alert+'>'+str(round(self.val,1))+'°</abbr></td>'

class VMag(Value):
    def __init__(self,val):
        self.val=round(float(val),2)

class RADec():
    def __init__(self,sky):
        coords = sky.to_string(style='hmsdms',precision=0)
        self.RA = coords.split(' ')[0]
        self.dec = coords.split(' ')[1]   
    def txt(self):
        return self.RA+' '+self.dec
    def html(self):
        return '<td>'+self.RA+'</td><td>'+self.dec+'</td>'

class Alt(Value):
    def txt(self):
        return str(int(self.val))+'°'
    def html(self,airmass,az):
        if self.val < 0: return '<td><abbr class="alert" title="The star must be above the horizon !&#10Height='+str(round(self.val,2))+'°&#10Azimuth : '+str(round(az))+'°">'+str(round(self.val))+'°</abbr></td>'
        elif self.val < 15: alert='class="alert" '
        elif self.val < 30: alert='class="warn" '
        else: alert=''
        return '<td><abbr '+alert+'title="Height='+str(round(self.val,2))+'° ; Airmass='+str(round(airmass,3))+'&#10Azimuth : '+str(round(az))+'°">'+str(round(self.val))+'°</abbr></td>'

class Delta(Value):
    def __init__(self,val):
        self.val=(round(val,3))
    def txt(self):
        return str(round(self.val,1))+'°'
    def html(self):
        if math.fabs(round(self.val,1)) >= 10: alert='class="alert" title="Very huge height difference"'
        elif math.fabs(round(self.val,1)) >= 5: alert='class="warn" title="Huge height difference"'
        else: return '<td sorttable_customkey="'+str(math.fabs(self.val))+'">'+str(round(self.val,1))+'°</td>'
        return '<td sorttable_customkey="'+str(math.fabs(self.val))+'"><abbr '+alert+'>'+str(round(self.val,1))+'°</abbr></td>'

class BV(Value):
    pass

class EBV(Value):
    pass

class OType(Value):
    def html(self):
        if (self.val == 'Star'): return '<td>Star</td>'
        if (self.val == 'Be*'): return '<td><abbr class="warn" title="Be Star (should not be used as reference star)">Be*</abbr></td>'
        return '<td><abbr title="'+otypes[self.val]+'">'+self.val+'</abbr></td>'

class SPType(Value):
    def __init__(self,val):
        self.val=val.replace(' ','')    
    def html(self):
        sptype = re.search(r'[OBA]\d+[IV]+s?[a-z]*',self.val.replace(' ',''))
        if sptype: sptype=sptype.group()
        else: return '<td>'+self.val+'</td>'

        if sptype.lower() in picklesdb: return '<td><abbr class="good" title="The spectral type '+sptype.upper()+' is in the Pickles Library of Stellar Spectra">'+self.val+'</abbr></td>'
        else: return '<td>'+self.val+'</td>'            

class Miles(Value):
    def html(self):
        if (self.val != ''): return '<td><abbr class="good" title="This star is in the Miles database">'+str(self.val)+'</abbr></td>'
        else: return '<td></td>'
    def txt(self):
        if (self.val != ''): return str(self.val)
        else: return ''

