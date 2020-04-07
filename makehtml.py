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
import bs4 # BeautifulSoup

#https://www.usno.navy.mil/ : USNO websites [...] are undergoing modernization efforts. The expected completion of the work and return of service is estimated as 30 April 2020.
from astropy.utils import iers
iers.conf.auto_download = False

#avoid "No known catalog could be found" warning
import warnings
warnings.filterwarnings(action="ignore")

import configparser
cfg = configparser.ConfigParser()
cfg.read('config.ini')

csvfilename = cfg.get('spectrostars','csvfilename')
targetname = cfg.get('spectrostars','targetname')
obsplacename = cfg.get('spectrostars','obsplacename')
obsdatetime = cfg.get('spectrostars','obsdatetime')
maxseparation = cfg.getint('spectrostars','maxseparation')

outputfilename = 'stars-'+''.join(e for e in targetname if e.isalnum())+'.html'

base = Base(csvfilename)  #load database in an object
observateur = Observer(obsplacename, obsdatetime)  #create observer object
cible = Target(targetname)  #create target object

if observateur.place is None:
    print("Can't find observer's place !")
    exit(1)
if cible.sky is None:
    print('Target can\'t be found !')
    exit(2)
cible.observe(observateur)  #observe target

print(cible.txt())
print(observateur.txt())

sorttable = """<script type="text/javascript"> 
/*  SortTable   version 2   7th April 2007
  Stuart Langridge, http://www.kryogenix.org/code/browser/sorttable/ */
var stIsIE=!1;if(sorttable={init:function(){arguments.callee.done||(arguments.callee.done=!0,_timer&&clearInterval(_timer),document.createElement&&document.getElementsByTagName&&(sorttable.DATE_RE=/^(\d\d?)[\/\.-](\d\d?)[\/\.-]((\d\d)?\d\d)$/,forEach(document.getElementsByTagName("table"),function(t){-1!=t.className.search(/\bsortable\b/)&&sorttable.makeSortable(t)})))},makeSortable:function(t){if(0==t.getElementsByTagName("thead").length&&(the=document.createElement("thead"),the.appendChild(t.rows[0]),t.insertBefore(the,t.firstChild)),null==t.tHead&&(t.tHead=t.getElementsByTagName("thead")[0]),1==t.tHead.rows.length){sortbottomrows=[];for(var e=0;e<t.rows.length;e++)-1!=t.rows[e].className.search(/\bsortbottom\b/)&&(sortbottomrows[sortbottomrows.length]=t.rows[e]);if(sortbottomrows){null==t.tFoot&&(tfo=document.createElement("tfoot"),t.appendChild(tfo));for(e=0;e<sortbottomrows.length;e++)tfo.appendChild(sortbottomrows[e]);delete sortbottomrows}headrow=t.tHead.rows[0].cells;for(e=0;e<headrow.length;e++)headrow[e].className.match(/\bsorttable_nosort\b/)||(mtch=headrow[e].className.match(/\bsorttable_([a-z0-9]+)\b/),mtch&&(override=mtch[1]),mtch&&"function"==typeof sorttable["sort_"+override]?headrow[e].sorttable_sortfunction=sorttable["sort_"+override]:headrow[e].sorttable_sortfunction=sorttable.guessType(t,e),headrow[e].sorttable_columnindex=e,headrow[e].sorttable_tbody=t.tBodies[0],dean_addEvent(headrow[e],"click",sorttable.innerSortFunction=function(t){if(-1!=this.className.search(/\bsorttable_sorted\b/))return sorttable.reverse(this.sorttable_tbody),this.className=this.className.replace("sorttable_sorted","sorttable_sorted_reverse"),this.removeChild(document.getElementById("sorttable_sortfwdind")),sortrevind=document.createElement("span"),sortrevind.id="sorttable_sortrevind",sortrevind.innerHTML=stIsIE?'&nbsp<font face="webdings">5</font>':"&nbsp;&#x25B4;",void this.appendChild(sortrevind);if(-1!=this.className.search(/\bsorttable_sorted_reverse\b/))return sorttable.reverse(this.sorttable_tbody),this.className=this.className.replace("sorttable_sorted_reverse","sorttable_sorted"),this.removeChild(document.getElementById("sorttable_sortrevind")),sortfwdind=document.createElement("span"),sortfwdind.id="sorttable_sortfwdind",sortfwdind.innerHTML=stIsIE?'&nbsp<font face="webdings">6</font>':"&nbsp;&#x25BE;",void this.appendChild(sortfwdind);theadrow=this.parentNode,forEach(theadrow.childNodes,function(t){1==t.nodeType&&(t.className=t.className.replace("sorttable_sorted_reverse",""),t.className=t.className.replace("sorttable_sorted",""))}),sortfwdind=document.getElementById("sorttable_sortfwdind"),sortfwdind&&sortfwdind.parentNode.removeChild(sortfwdind),sortrevind=document.getElementById("sorttable_sortrevind"),sortrevind&&sortrevind.parentNode.removeChild(sortrevind),this.className+=" sorttable_sorted",sortfwdind=document.createElement("span"),sortfwdind.id="sorttable_sortfwdind",sortfwdind.innerHTML=stIsIE?'&nbsp<font face="webdings">6</font>':"&nbsp;&#x25BE;",this.appendChild(sortfwdind),row_array=[],col=this.sorttable_columnindex,rows=this.sorttable_tbody.rows;for(var e=0;e<rows.length;e++)row_array[row_array.length]=[sorttable.getInnerText(rows[e].cells[col]),rows[e]];row_array.sort(this.sorttable_sortfunction),tb=this.sorttable_tbody;for(e=0;e<row_array.length;e++)tb.appendChild(row_array[e][1]);delete row_array}))}},guessType:function(t,e){sortfn=sorttable.sort_alpha;for(var r=0;r<t.tBodies[0].rows.length;r++)if(text=sorttable.getInnerText(t.tBodies[0].rows[r].cells[e]),""!=text){if(text.match(/^-?[£$¤]?[\d,.]+%?$/))return sorttable.sort_numeric;if(possdate=text.match(sorttable.DATE_RE),possdate){if(first=parseInt(possdate[1]),second=parseInt(possdate[2]),12<first)return sorttable.sort_ddmm;if(12<second)return sorttable.sort_mmdd;sortfn=sorttable.sort_ddmm}}return sortfn},getInnerText:function(t){if(!t)return"";if(hasInputs="function"==typeof t.getElementsByTagName&&t.getElementsByTagName("input").length,null!=t.getAttribute("sorttable_customkey"))return t.getAttribute("sorttable_customkey");if(void 0!==t.textContent&&!hasInputs)return t.textContent.replace(/^\s+|\s+$/g,"");if(void 0!==t.innerText&&!hasInputs)return t.innerText.replace(/^\s+|\s+$/g,"");if(void 0!==t.text&&!hasInputs)return t.text.replace(/^\s+|\s+$/g,"");switch(t.nodeType){case 3:if("input"==t.nodeName.toLowerCase())return t.value.replace(/^\s+|\s+$/g,"");case 4:return t.nodeValue.replace(/^\s+|\s+$/g,"");case 1:case 11:for(var e="",r=0;r<t.childNodes.length;r++)e+=sorttable.getInnerText(t.childNodes[r]);return e.replace(/^\s+|\s+$/g,"");default:return""}},reverse:function(t){newrows=[];for(var e=0;e<t.rows.length;e++)newrows[newrows.length]=t.rows[e];for(e=newrows.length-1;0<=e;e--)t.appendChild(newrows[e]);delete newrows},sort_numeric:function(t,e){return aa=parseFloat(t[0].replace(/[^0-9.-]/g,"")),isNaN(aa)&&(aa=0),bb=parseFloat(e[0].replace(/[^0-9.-]/g,"")),isNaN(bb)&&(bb=0),aa-bb},sort_alpha:function(t,e){return t[0]==e[0]?0:t[0]<e[0]?-1:1},sort_ddmm:function(t,e){return mtch=t[0].match(sorttable.DATE_RE),y=mtch[3],m=mtch[2],d=mtch[1],1==m.length&&(m="0"+m),1==d.length&&(d="0"+d),dt1=y+m+d,mtch=e[0].match(sorttable.DATE_RE),y=mtch[3],m=mtch[2],d=mtch[1],1==m.length&&(m="0"+m),1==d.length&&(d="0"+d),dt2=y+m+d,dt1==dt2?0:dt1<dt2?-1:1},sort_mmdd:function(t,e){return mtch=t[0].match(sorttable.DATE_RE),y=mtch[3],d=mtch[2],m=mtch[1],1==m.length&&(m="0"+m),1==d.length&&(d="0"+d),dt1=y+m+d,mtch=e[0].match(sorttable.DATE_RE),y=mtch[3],d=mtch[2],m=mtch[1],1==m.length&&(m="0"+m),1==d.length&&(d="0"+d),dt2=y+m+d,dt1==dt2?0:dt1<dt2?-1:1},shaker_sort:function(t,e){for(var r=0,o=t.length-1,n=!0;n;){n=!1;for(var s=r;s<o;++s)if(0<e(t[s],t[s+1])){var a=t[s];t[s]=t[s+1],t[s+1]=a,n=!0}if(o--,!n)break;for(s=o;r<s;--s)if(e(t[s],t[s-1])<0){a=t[s];t[s]=t[s-1],t[s-1]=a,n=!0}r++}}},document.addEventListener&&document.addEventListener("DOMContentLoaded",sorttable.init,!1),/WebKit/i.test(navigator.userAgent))var _timer=setInterval(function(){/loaded|complete/.test(document.readyState)&&sorttable.init()},10);function dean_addEvent(t,e,r){if(t.addEventListener)t.addEventListener(e,r,!1);else{r.$$guid||(r.$$guid=dean_addEvent.guid++),t.events||(t.events={});var o=t.events[e];o||(o=t.events[e]={},t["on"+e]&&(o[0]=t["on"+e])),o[r.$$guid]=r,t["on"+e]=handleEvent}}function removeEvent(t,e,r){t.removeEventListener?t.removeEventListener(e,r,!1):t.events&&t.events[e]&&delete t.events[e][r.$$guid]}function handleEvent(t){var e=!0;t=t||fixEvent(((this.ownerDocument||this.document||this).parentWindow||window).event);var r=this.events[t.type];for(var o in r)this.$$handleEvent=r[o],!1===this.$$handleEvent(t)&&(e=!1);return e}function fixEvent(t){return t.preventDefault=fixEvent.preventDefault,t.stopPropagation=fixEvent.stopPropagation,t}window.onload=sorttable.init,dean_addEvent.guid=1,fixEvent.preventDefault=function(){this.returnValue=!1},fixEvent.stopPropagation=function(){this.cancelBubble=!0},Array.forEach||(Array.forEach=function(t,e,r){for(var o=0;o<t.length;o++)e.call(r,t[o],o,t)}),Function.prototype.forEach=function(t,e,r){for(var o in t)void 0===this.prototype[o]&&e.call(r,t[o],o,t)},String.forEach=function(r,o,n){Array.forEach(r.split(""),function(t,e){o.call(n,t,e,r)})};var forEach=function(t,e,r){if(t){var o=Object;if(t instanceof Function)o=Function;else{if(t.forEach instanceof Function)return void t.forEach(e,r);"string"==typeof t?o=String:"number"==typeof t.length&&(o=Array)}o.forEach(t,e,r)}};
</script>

"""

output = cible.html() + '<br>' + observateur.html()+'<br>\n'

if cible.alt<0:
    print('Target is below the horizon!')
    exit(0)

base.near(cible,maxseparation,observateur)  #search stars near target
output += base.html()


with open("index.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt)

output = bs4.BeautifulSoup('<div>'+output+'</div>')
sorttable = bs4.BeautifulSoup(sorttable)

for scripts in soup.find_all("script"): scripts.extract() #remove current <script> tags
for links in soup.find_all("link"): links.extract() #remove  <link> tags
soup.find('title').string = targetname
soup.find('head').append(sorttable.script)
soup.find("form").clear()
result = soup.find(id="result")
result.clear()
result.append(output.html.body.div)

print('Writing output to '+outputfilename)
with open(outputfilename, "w") as outf:
    outf.write(str(soup))

#print(output)