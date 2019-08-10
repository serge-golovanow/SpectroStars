# SpectroStars
[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE.txt)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-red.svg)](https://www.python.org/)
[![Powered by Astropy](http://img.shields.io/badge/Powered%20by-AstroPy-orange.svg)](https://www.astropy.org)

**Find reference stars for astronomical spectroscopy : https://spectro-starfinder.net/**

Based on an idea and the stars database from [François Teyssier](http://www.spectro-aras.com/forum/viewtopic.php?f=8&t=1227). Able to find target's coordinates on [SIMBAD](https://simbad.u-strasbg.fr/simbad/), observer's place from [IAU/MPC observatory code](https://minorplanetcenter.net/iau/lists/ObsCodesF.html) or place name, it also manages timezone and daylight saving. Main processing loop on stars database is [parallelized](https://joblib.readthedocs.io/en/latest/parallel.html).


Searching for stars nearer than 10° of M27, from [L14](https://minorplanetcenter.net/iau/lists/ObsCodesF.html) (Vaulx-en-Velin Planetarium), september 9th, 23:00 local time : https://spectro-starfinder.net/#M27

	Target   : m27 (19h59m36s +22d43m16s, Vulpecula), altitude=65.8°, azimuth=202° (S), airmass (secz)=1.097
    Observer : lat=45d46m38s, lon=4d55m22s, alt=172m, tz=Europe/Paris, 2019-09-10 21:00:00 UTC
    
    ..  Star:       Sep:    VMag:   RA:       Dec:          Height:         B-V:    Eb-v:   SpType:  secz:  Miles:
    01  HD 196724   9.1°    4.82    20h38m31s +21d12m04s    65°, Δh=-0.3°   -0.02   0       A0V      1.1
    02  HD338529    7.1°    9.37    19h32m58s +26d23m26s    67°, Δh=1.0°            0.01    B5       1.09   s0725
    03  HD 190993   1.9°    5.064   20h06m53s +23d36m52s    67°, Δh=1.3°    -0.16   0.04    B3V      1.09
    04  HD 189944   2.1°    5.872   20h01m45s +24d48m02s    68°, Δh=2.1°    -0.133  0.05    B4V      1.08
    05  HD 183914   8.4°    5.088   19h30m45s +27d57m55s    68°, Δh=2.1°    -0.061  0.05    B8Ve     1.08
    06  HD 192685   4.6°    4.759   20h15m16s +25d35m31s    69°, Δh=3.6°    -0.167  0.03    B3V      1.07
    07  HD 187362   4.4°    5       19h48m59s +19d08m31s    62°, Δh=-4.2°   0.1     0.02    A3V      1.14
    08  HD 192044   4.7°    5.903   20h12m01s +26d28m44s    70°, Δh=4.4°    -0.106  0.02    B7Ve     1.06
    09  HD189849    5.1°    4.663   20h01m59s +27d45m13s    71°, Δh=5.0°            0.03    A4III    1.06   s0748
    10  HD 196504   9.3°    5.589   20h37m05s +26d27m43s    71°, Δh=5.0°    -0.05   0.02    B9V      1.06
    11  HD 182919   8.2°    5.594   19h26m13s +20d05m52s    61°, Δh=-5.3°   0.002   0.01    A0V      1.15
    12  HD 192425   8.3°    4.947   20h14m17s +15d11m51s    59°, Δh=-6.7°   0.066   0.02    A2V      1.17
    13  HD 189395   8.3°    5.506   19h58m38s +30d59m01s    73°, Δh=7.7°    -0.059  0.01    B9Vn     1.04
    14  HD 185936   9.9°    5.988   19h41m06s +13d48m56s    56°, Δh=-9.8°   -0.081  0.08    B5V      1.21

Required python packages : [timezonefinder](https://pypi.org/project/timezonefinder/) [pytz](https://pypi.org/project/pytz/) [numpy](https://pypi.org/project/numpy/) [astropy](https://pypi.org/project/astropy/) [astroquery](https://pypi.org/project/astroquery/) [joblib](https://pypi.org/project/joblib/). AstroPy version >= 3.1 is required. Caution, [numba](https://pypi.org/project/numba/) badly interferes.

File|Language|Description
----|--------|-----------
spectrostars.py|Python|Main script
base.csv|CSV|Stars database
otypes.py|Python|Object classification in SIMBAD
wsgi.py|Python|Optional WSGI backend
index.html|HTML, CSS|Optional web page
jslib.js|JavaScript|jQuery and JS-Storage for the web page
jscode.js|JavaScript|JavaScript code for the web page

_**Work in progress... Discussions on [spectro-aras forum](http://www.spectro-aras.com/forum/viewtopic.php?f=8&t=2252).**_
