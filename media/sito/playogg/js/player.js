// execute on load

    var flashvars = {};
    var params = {};
    var attributes = {
    allowScriptAccess: "always",
    swLiveConnect:"true"
    };

    var haveflash=false;
    function callbackFn(e) 
    {
      if (e.success){
      //alert("you have flash");
      haveflash=true;
    };
      createPlayer(media,"html5player","flashplayer","javaplayer");
    }
    
    // try to update flash becouse after I am hidden !
    function cancelFunction() {
     alert("Flash Express Install was cancelled");
    }
    var upflash = function() {

      var att = { data:media_url+"/sito/playogg/swfobject/expressInstall.swf", width:"310", height:"137" };
      var par = {};
      var id = "updateflash";
      swfobject.showExpressInstall(att, par, id, cancelFunction);
    }

    if ( ! (swfobject.hasFlashPlayerVersion("10.0.0"))) {
	swfobject.addDomLoadEvent(upflash);
    }

    swfobject.embedSWF(media_url+"/sito/playogg/flash/AnOgg.swf", "flashplayer",  "0", "0", "10.0.0", media_url+"/sito/playogg/swfobject/expressInstall.swf",flashvars,params,attributes,callbackFn);



//----------------------------------------------------
//                 Flash
//
/* Helper function */
function getFlashMovie(movieName)
{

    if (window.document[movieName]) 
	{
	    return window.document[movieName];
	}
    if (navigator.appName.indexOf("Microsoft Internet")==-1)
	{
	    if (document.embeds && document.embeds[movieName])
		return document.embeds[movieName]; 
	}
    else // if (navigator.appName.indexOf("Microsoft Internet")!=-1)
	{
	    return document.getElementById(movieName);
	} 
}

/* Commands */
function oggPlayURL(oggPlayer,str)//play an url ending with .ogg or .mp3
{
	getFlashMovie(oggPlayer).playURL(str);
}
function oggStop(oggPlayer) //stop playing and discontinue loading as well
{
	getFlashMovie(oggPlayer).stopPlaying();
	//btnSetBufferState(0);
}
function oggSetVolume(oggPlayer,val)//set linear volume to 0-100
{
	getFlashMovie(oggPlayer).setVolume(val);
}
function oggPause(oggPlayer)//toggle pause playing but continue loading
{
	getFlashMovie(oggPlayer).pausePlay();
}
function oggSeek(oggPlayer,val)//set seek position from 0 to 1 (floating point)
{
	getFlashMovie(oggPlayer).Seek(val);
}


// general function

function  createPlayer(playURL,html5id,flashid,javaid){

    var id=testobjects(html5id,flashid,javaid);

    if(document.getElementById && document.createElement)
	{

	    //alert(id);

	    if ( id == "plugin"){

		// Creiamo il nuovo elemento Anchor

		immagine = document.createElement("A");
		immagine.innerHTML="<img src='player.png'>";
		immagine.setAttribute("id",id);
		immagine.setAttribute("type","audio/ogg");
		immagine.setAttribute("href",playURL);
		//		immagine.setAttribute("href","player.m3u");
		//              application/xspf+xml

		// inseriamola quindi nel nostro tag <player>
		document.getElementById("player").appendChild(immagine);

	    }
	    else{
		// Creiamo il nuovo elemento IMG e
		// impostiamo l'attributo src, che recupera l'immagine
		immagine = document.createElement("IMG");
		immagine.setAttribute("src",imgURL+"player.png");
		immagine.setAttribute("id",id);
		immagine.setAttribute("alt","Play OGG");
		//immagine.setAttribute("onclick","buttonPlayStop(event,'"+playURL+"','"+html5id+"','"+flashid+"','"+javaid+"')");

		// inseriamola quindi nel nostro tag <player>
		document.getElementById("player").appendChild(immagine);

		$("#"+id).click(function (event) { 
			buttonPlayStop(event,playURL,html5id,flashid,javaid);
		    });
	    
	    }
	}
}

function  setPlayerButton(PlayerID,PlayStop,imgBaseURL)
{
    document.getElementById(PlayerID).src=imgURL+"media-"+PlayStop+".png";
}

var html5playogg=null;

function testobjects(html5id,flashid,javaid){
    var player=null;

    try {
	
	html5playogg=document.createElement('audio').canPlayType('audio/ogg; codecs=vorbis');

	document.getElementById(html5id).pause();
	if (html5playogg != "probably")
	    { 
		//swfobject.embedSWF("flash/AnOgg.swf", "redoflplayer",  "310", "137", "10.0.0", "swfobject/expressInstall.swf",flashvars,params,attributes,callbackFn);
	    //alert(flashid);
		alert("Your browser have some problems with html5 tag ! update it or try firefox");
		//raise_random_error();
	}
	player="html5";
    }
    catch(err){

	/*   non va questo
	try {
	    oggPlayURL("null.ogg");
	    player="flash";
	}
	*/

	if (haveflash){
	    player="flash";
	    return player;
	}
	
	try {
	    document.getElementById(javaid).doStop();
	    player="java";
	}
	catch(err){
	    player="plugin";
	}
    }

    return player;
}


function buttonPlayStop(event,playURL,html5id,flashid,javaid){
    // IE doesn't pass event into the parameter
    if ( !event )
	{
	    event = window.event;
	}

    // IE doesn't have the property "target".
    // Use "srcElement" instead.
    // Not 100% the same, but works in most simple cases
    var target = event.target ? event.target : event.srcElement;

    PlayerID=target.getAttribute("id")
	
	switch (PlayerID) {
	case "html5":
	html5buttonPlayStop(PlayerID,html5id,playURL);
	break;
	
	case "flash": 
	flashbuttonPlayStop(PlayerID,flashid,playURL);
	break;
	
	case "java": 
	javabuttonPlayStop(PlayerID,javaid,playURL);
	break;

	default:
	alert("evento non gestito; contatta il webmaster");
	}
}

function html5buttonPlayStop(PlayerID,html5id,playURL)
{
    var myAudio = document.getElementById(html5id);
    if (myAudio.paused){
       	myAudio.setAttribute('src', playURL);
	myAudio.play();
	setPlayerButton(PlayerID,"stop");
    }else{
	myAudio.pause();
	setPlayerButton(PlayerID,"play");
    }
}

     var flStatus = false;

function flashbuttonPlayStop(PlayerID,flashid,playURL)
{
    if (flStatus){
	oggStop(flashid);
	flStatus = false;
	setPlayerButton(PlayerID,"play");
    }
    else{
	oggPlayURL(flashid,playURL);
	flStatus = true;
	setPlayerButton(PlayerID,"stop");
    } 
}


/* doPlay(): Start playback
   doPause(): Pause playback
   doStop(): Stop playback 
   doSeek(double pos)   seek to a new position, must be between 0.0 and 1.0.
   getPlayPosition(): returns current position in seconds   */

var javaStatus = false;

function javabuttonPlayStop(PlayerID,javaid,playURL)
{
    var javaAudio = document.getElementById(javaid);

    if (javaStatus){
	javaAudio.doStop();
	javaStatus = false;
	setPlayerButton(PlayerID,"play");
    } 
    else{
	javaAudio.doPlay();
	javaStatus = true;
	setPlayerButton(PlayerID,"stop");
    }
}

