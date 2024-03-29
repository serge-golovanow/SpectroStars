'''
SpectroStars : Find reference stars for spectroscopy
https://github.com/serge-golovanow/SpectroStars
Copyright © 2019, Serge Golovanow

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.

WSGI endpoint for SpectroStars

Apache (mod-wsgi-py3) VirtualHost configuration example :
    WSGIDaemonProcess spectrostars user=www-data group=www-data home=/var/www/spectrostars
    WSGIProcessGroup spectrostars
    WSGIScriptAlias /spectrostars/wsgi /var/www/spectrostars/wsgi.py

v2022-01-14
'''

import os
cwd = os.getcwd()
os.environ.update({ 'HOME':cwd })

from cgi import parse_qs, escape
from datetime import datetime
 
from lib.functions import *
from lib.target import Target
from lib.observer import Observer
from lib.base import Base 

#https://www.usno.navy.mil/ : USNO websites [...] are undergoing modernization efforts. The expected completion of the work and return of service is estimated as 30 April 2020.
from astropy.utils import iers
iers.conf.auto_download = False

#avoid "No known catalog could be found" and other warnings
import warnings
warnings.filterwarnings(action="ignore")

import configparser
cfg = configparser.ConfigParser()
cfg.read('config.ini')
csvfilename = cfg.get('spectrostars','csvfilename')

def application(environ, start_response):
    query = parse_qs(environ['QUERY_STRING']) #query parameters
    outputlines = None #array with all lines to output

    if 'output' in query : outputmode = escape(query.get('output')[0])
    else: outputmode = 'html'
    if 'separation' in query: maxseparation = int(query.get('separation')[0])
    else: maxseparation = 10 # default separation
    if maxseparation<5: maxseparation=5 # min separation
    if maxseparation>20: maxseparation=20 # max separation
    if 'date' in query: date = escape(query.get('date')[0])
    else: date = datetime.today().strftime('%Y-%m-%d')
    if 'time' in query: time = escape(query.get('time')[0])
    else: time = '22:00' #local time
    obsdatetime = date+' '+time
    if 'place' in query: obsplacename = escape(query.get('place')[0])
    else: obsplacename = 'Lyon, France' #Home, sweet home !
    if 'target' in query: targetname = escape(query.get('target')[0])
    else: outputlines = ['no target ?!!'] #no default target

    if (outputlines is None):         
        base = Base(csvfilename)  #load database in an object
        observateur = Observer(obsplacename, obsdatetime)  #create observer object
        cible = Target(targetname)  #create target object
        cible = Target(targetname)  #create target object
        if observateur.place is None:
            outputlines = ["Can't find observer's place !"]
        elif cible.sky is None:
            outputlines = ["Can't find target !"]
        else:
            cible.observe(observateur)  #observe target
            base.near(cible,maxseparation,observateur)

            if outputmode == 'html':
                if cible.alt>0: outputlines = [cible.html()+'<br>',observateur.html()+'<br>',base.html()]
                else: outputlines = [cible.html()+'<br>',observateur.html()+'<br>','Target is below the horizon !']
            elif outputmode == 'xml':
                if cible.alt>0: outputlines = [cible.xml(),observateur.xml(),base.xml()]
                else: outputlines = [cible.xml(),observateur.xml(),'<!-- Target is below the horizon ! -->','<stars results="0"></stars>']
            else:
                if cible.alt>0: outputlines = [cible.txt(),observateur.txt(),base.txt()]
                else: outputlines = [cible.txt(),observateur.txt(),'Target is below the horizon !']                

    if (outputlines is not None): status = '200 OK' #HTTP success
    else: 
        status = '520 Unknown Error'
        outputlines = ['An error occured...']

    #Encode output string
    output = bytes('\n'.join(outputlines), 'utf-8')

    response_headers = [('Content-type', 'text/plain; charset=utf-8'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
