
/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

* SpectroStars : find reference stars for spectroscopy
* https://github.com/serge-golovanow/SpectroStars
* Copyright (c) 2019, Serge Golovanow
* 
* Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
* The Software is provided “as is”, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the Software.
* 
* Here is the JavaScript part.
* 
* Required libraries :
*  jQuery          MIT license     (c) JS Foundation and other contributors        https://jquery.org/license
*  JS-Storage      MIT license     Copyright (c) 2016 Julien Maurel                https://github.com/julien-maurel/js-storage
* 
* As lot VanillaJS as possible ; jQuery will be used only for AJAX
* 
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */

//  WSGI endpoint URL
WSGIURL = 'wsgi';

// Nothing else to do

var storage; //JS Storage

Number.prototype.pad = function(size) { //.padstart(2,'0') won't work with internet explorer
    var s = String(this);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
}        

function now() { // set time to the current one
    var d = new Date();
    var tnow = d.getHours().pad(2) +":"+ d.getMinutes().pad(2);
    document.getElementById('time').value = tnow;
}//////////////////////////////////////////////////////////////////////////

function geoloc() { //HTML5 geolocation from navigator
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position){
            try {
                document.getElementById('place').value = position.coords.latitude.toFixed(3)+", "+position.coords.longitude.toFixed(3);
            } catch(ex) { console.warn('GeoLocation error : '+ex); }
        });
    } else {
        console.warn('Navigator GeoLocation is not available');
    }
    return false;
}//////////////////////////////////////////////////////////////////////////

function validform() { //if form is valid, call WSGI
    var erreurs = [];
    var elplace = document.getElementById('place');
    var eldate = document.getElementById('date');
    var eltime = document.getElementById('time');
    var eltarget = document.getElementById('target');
    var elsepa = document.getElementById('separation');
    var elinfo = document.getElementById('forminfo');

    if (elplace.value == "") erreurs.push('observing place');
    if (eldate.value == "") eldate.valueAsDate = new Date();
    if (eltime.value == "") eltime.value = "22:00"
    if (eltarget.value == "") erreurs.push('observing target');
    if (elsepa.value == "") elsepa.value = "10"
    if (elsepa.value <5 ) elsepa.value = "5"
    if (elsepa.value >20) elsepa.value = "20"
    
    if (erreurs.length) { elinfo.innerHTML = "Error : please specify "+erreurs.join(' and ')+' !'; return false; }
    else elinfo.innerHTML = "";

    // Processing ; jQuery used from here
    $("#submit").html('Processing... please wait').prop("disabled", true);
    $('input').prop("disabled", true);
    $('html').addClass('wait');
    $.ajax({ 
        method: "GET",  url: WSGIURL,
        data: { place: elplace.value, target: eltarget.value, date: eldate.value, time: eltime.value, separation:elsepa.value },
        success : function(msg, statut){ // when process is correctly done
            $('html').removeClass('wait');
            $("#result").html(msg);
            try {
                sorttable.makeSortable(document.getElementById("stars"));
                var myTH = document.getElementsByTagName("th")[7];
                sorttable.innerSortFunction.apply(myTH, []);
            } catch(e) { }
            $("#submit").html('Process').prop("disabled", false);   
            $('input').prop("disabled", false);
            try { // write target name in URL anchor
                window.location.hash = document.getElementById('target').value;
            } catch(ex) { console.warn("Erreur du hash : "+ex); } // en cas d'erreur on enchaine    
            try { // save place
                storage.set('place',document.getElementById('place').value);
            } catch(ex) { console.warn("Erreur JS storage : "+ex); } 
        },
        error : function(resultat, statut, error){ // if wsgi crashed
            $('html').removeClass('wait');
            $('input').prop("disabled", false);
            $("#result").html( 'Error : '+error+', please try again' );
            $("#submit").html('Process').prop("disabled", false);
            
        },
        complete : function(resultat, statut){

        }
    }); //end $.ajax({

    return false;     
}/////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function(event) { // jQuery(document).ready(function($){
    var place = undefined;
    try { // load place from JS storage
        storage=Storages.localStorage; 
        place = storage.get('place');
    } catch(error) { 
        storage=false; 
        console.warn("Au chargement de JS-Storage : "+error);
    }             
    var htmldate = document.getElementById('date');
    document.getElementById('geoloc').addEventListener("click", geoloc, true);
    htmldate.valueAsDate = new Date(); //today
    if (htmldate.value == "") { htmldate.value = (htmldate.valueAsDate.getFullYear()+'-'+(htmldate.valueAsDate.getMonth()+1)+'-'+htmldate.valueAsDate.getDate()); }
    document.getElementById('time').value = '22:00'; //tonight
    document.getElementById('separation').value=10;
    if (place !== undefined && place !== null) document.getElementById('place').value = place; 
    document.getElementById('target').value = window.location.hash.substr(1).replace('%20',' ');
    document.getElementById('now').addEventListener("click", now, true);

});/////////////////////////////////////////////////////////////////////////
