# SpectroStars
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE.txt)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-red.svg)](https://www.python.org/)
[![Powered by Astropy](http://img.shields.io/badge/Powered%20by-AstroPy-orange.svg)](https://www.astropy.org)

**Find reference stars for astronomical spectroscopy : https://spectro-starfinder.net/**

_Work in progress... Discussions on [spectro-aras forum](http://www.spectro-aras.com/forum/viewtopic.php?f=8&t=2252)._

Based on an idea and the stars database from [François Teyssier](http://www.spectro-aras.com/forum/viewtopic.php?f=8&t=1227). Able to find target's coordinates on [SIMBAD](https://simbad.u-strasbg.fr/simbad/), observer's place from [IAU/MPC observatory code](https://minorplanetcenter.net/iau/lists/ObsCodesF.html) or place name, it also manages timezone and daylight saving. Main processing loop on stars database is [parallelized](https://joblib.readthedocs.io/en/latest/parallel.html).


Searching for stars nearer than 5° of M27, from [586](https://minorplanetcenter.net/iau/lists/ObsCodesF.html) (Pic du Midi), september 15th, 23:00 local time : https://spectro-starfinder.net/#M27

    Target: M  27 (19h59m36s +22d43m16s, Planetary Nebula in Vulpecula), altitude=68.3°, azimuth=204°, airmass=1.076
    Observer: lat=42d56m13s, lon=0d08m27s, alt=2843m, tz=Europe/Paris, 2019-09-15 21:00 UTC
    ..  Star:       Sep:    VMag:   RA:       Dec:          Height:         B-V:    Eb-v:   SpType: Miles:
    01  HD 187811   2.0°    4.89    19h51m04s +22d36m36s    67°, Δh=-0.8°   -0.143  0.10    B2,5Ve
    02  HD 190993   1.9°    5.06    20h06m53s +23d36m52s    69°, Δh=1.4°    -0.16   0.04    B3V
    03  HD 189944   2.1°    5.87    20h01m45s +24d48m02s    70°, Δh=2.1°    -0.133  0.05    B4V
    04  HD 185859   4.9°    6.54    19h40m58s +20d28m38s    64°, Δh=-3.7°           0.63    B0.5Iae s0732
    05  HD 192685   4.6°    4.76    20h15m16s +25d35m31s    72°, Δh=3.8°    -0.167  0.03    B3V
    06  HD 187362   4.4°    5.0     19h48m59s +19d08m31s    64°, Δh=-4.2°   0.1     0.02    A3V
    07  HD 192044   4.7°    5.9     20h12m01s +26d28m44s    72°, Δh=4.4°    -0.106  0.02    B7Ve

Required python packages : [configparser](https://pypi.org/project/configparser/) [timezonefinder](https://pypi.org/project/timezonefinder/) [pytz](https://pypi.org/project/pytz/) [numpy](https://pypi.org/project/numpy/) [astropy](https://pypi.org/project/astropy/) [astroquery](https://pypi.org/project/astroquery/) [joblib](https://pypi.org/project/joblib/). AstroPy version >= 3.1 is required. Caution, [numba](https://pypi.org/project/numba/) badly interferes.

File|Language|Description
----|--------|-----------
spectrostars.py|Python|Main script
config.ini|INI|Configuration
base.csv|CSV|Stars database
lib/base.py|Python|Stars database
lib/display.py|Python|Formater for HTML or text display
lib/functions.py|Python|Various functions
lib/observer.py|Python|Observer
lib/otypes.py|Python|Object classification in SIMBAD
lib/target.py|Python|Target
makehtml.py|Python|Create offline HTML list of stars
wsgi.py|Python|Optional WSGI backend
index.html|HTML, CSS|Optional web page
jslib.js|JavaScript|jQuery and JS-Storage for the web page
jscode.js|JavaScript|JavaScript code for the web page
