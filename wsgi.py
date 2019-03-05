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


Forbid access to spectrostars.py to protect your Google API key ; with a .htaccess file :
 RewriteRule spectrostars\.py$ - [F,L,NC]

v19-03-04
'''

from cgi import parse_qs, escape
from datetime import datetime
from spectrostars import process

def application(environ, start_response):
    query = parse_qs(environ['QUERY_STRING']) #query parameters
    outputlines = None #array with all lines to output

    if 'separation' in query: maxseparation = int(query.get('separation')[0])
    else: maxseparation = 10 # default separation
    if maxseparation<5: maxseparation=5 # min separation
    if maxseparation>20: maxseparation=20 # max separation
    if 'date' in query: date = escape(query.get('date')[0])
    else: date = datetime.strftime('%Y-%m-%d') #today ;  now() ?
    if 'time' in query: time = escape(query.get('time')[0])
    else: time = '22:00' #local time
    obsdatetime = date+' '+time
    if 'place' in query: place = escape(query.get('place')[0])
    else: place = 'Lyon, France' #Home, sweet home !
    if 'target' in query: target = escape(query.get('target')[0])
    else: outputlines = ['no target ?!!'] #no default target

    #Call to spectrostars.process !
    try:
        if (outputlines is None): outputlines = process(targetname=target,maxseparation=maxseparation,obsplace=place,obsdatetime=obsdatetime)
    except:
        outputlines = None

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