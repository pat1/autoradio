/* anOggPlayer JavaScript interface reference implementation */
/* copyright (c) anon-e-moose, mico.drive@gmail.com, 2009, all rights reserved */
/* this file is released under GNU LGPL v. 2.1 (or later if permissible under law) */

/* Global Vars */
var isIE;//set after first call to any interface function
var oggPlayer="haxe"; //set to name of flash control object. set automatically by this ref. interface.
var oggStatus=""; //status storage var, useful.

/* Events */
var doOggSongBegin=0;
var doOggState=0;
var doOggBuffer=0;
var doOggProgress=0;

/* Helper function */
function getFlashMovie(movieName) {
	isIE = navigator.appName.indexOf("Microsoft") != -1;
	return (isIE) ? window[movieName] : document[movieName];
}
/* Commands */
function oggPlayURL(str)//play an url ending with .ogg or .mp3
{
	getFlashMovie(oggPlayer).playURL(str);
}
function oggStop() //stop playing and discontinue loading as well
{
	getFlashMovie(oggPlayer).stopPlaying();
	//btnSetBufferState(0);
}
function oggSetVolume(val)//set linear volume to 0-100
{
	getFlashMovie(oggPlayer).setVolume(val);
}
function oggPause()//toggle pause playing but continue loading
{
	getFlashMovie(oggPlayer).pausePlay();
}
function oggSeek(val)//set seek position from 0 to 1 (floating point)
{
	getFlashMovie(oggPlayer).Seek(val);
}
/* Callbacks */
function onOggSongBegin(str)
{
	//called once when new stream arrives.
	//str is in the form 'tag="value";tag="value";' and contains the stream details.
	/*BAD example handling: str is not html-safe, possible exploit by inserting html tags in ogg stream header*/
	//var display = document.getElementById("hdr");
	//display.innerHTML=str;
	if(doOggSongBegin!=0)doOggSongBegin(str);
}
function onOggState(str)
{
	//called by player when state changes.
	//"loaded" when player initially loads and is ready. Don't do anything until loaded.
	//"buffering" when stream begins to load
	//"stopped" after stopPlay was called
	//"playing" after oggPlayURL was called, and buffering completed
	//"streamstop" after ogg stream/(or file if playing a file) ends
	//"error=$text" after some error happens.
	//Text may be "underflow", "ioerror","securerror", "badformat", "unsupported_format" or somesuch.
	oggStatus=str;
	/*example handling*/
	//if(str == "streamstop")btnSetBufferState(0);
	//var display = document.getElementById("stt");
	//display.innerHTML=str;
	if(doOggState!=0)doOggState(str);
}
function onOggBuffer(val)
{
	//called by player on buffering progress. val is 0 to 100.
	/*example handling*/
	//var display = document.getElementById("stt");
	//display.innerHTML=val;

	if(doOggBuffer!=0)doOggBuffer(val);
}
function onOggProgress(loaded,played)
{
	//called by player on progress
	//values for loaded and played are 0-100
	/*example handling*
	var prgBar=document.getElementById("loadprogress");
	var plyBar=document.getElementById("playposition");
	prgBar.style.width=loaded;
	plyBar.style.width=played;*/
	if(doOggProgress!=0)doOggProgress(loaded,played);
}

/* Reference visual interface */
var playerDiv="";
function initEvents()
{
	doOggState=onStateChanged;
	doOggProgress=oggSetProgress;
}
function injectPlayerObject(parentObj)//do this only once per page!
{
	var playerWidth=400;
	var playerHeight=400;
	var injectedHTML="<object classid=\"clsid:d27cdb6e-ae6d-11cf-96b8-444553540000\" ";
    injectedHTML+="codebase=\"http:\/\/download.macromedia.com\/pub\/shockwave\/cabs\/flash\/swflash.cab#version=6,0,0,0\" ";
    injectedHTML+="width=\""+playerWidth+"\" height=\""+playerHeight+"\" id=\""+oggPlayer+"\" align=\"middle\" ";
    //injectedHTML+="style=\"position:absolute;left:0;top:0\"> ";//make css style from it
	injectedHTML+="data=\"AnOgg.swf\" type=\"application\/x-shockwave-flash\" ";
	injectedHTML+="class='player_obj'>";
	injectedHTML+="<param name=\"movie\" value=\"AnOgg.swf\"\/>";
	injectedHTML+="<param name=\"allowScriptAccess\" value=\"always\"\/>";
	injectedHTML+="<param name=\"wmmode\" value=\"opaque\" \/>";
	injectedHTML+="<param name=\"quality\" value=\"low\" \/>";
	injectedHTML+="<param name=\"scale\" value=\"noscale\" \/>";
	injectedHTML+="<param name=\"salign\" value=\"lt\" \/>";
	injectedHTML+="<param name=\"bgcolor\" value=\"#ffffff\"\/>"
	injectedHTML+="<embed src=\"AnOgg.swf\" bgcolor=\"#ffffff\" width=\""+playerWidth+"\" ";
    injectedHTML+="height=\""+playerHeight+"\" class=\"player_obj\" name=\"haxe\" wmmode=\"opaque\" quality=\"low\" ";
    injectedHTML+="align=\"middle\" allowScriptAccess=\"always\" ";
    injectedHTML+="type=\"application\/x-shockwave-flash\" ";
    injectedHTML+="pluginspage=\"http:\/\/www.macromedia.com\/go\/getflashplayer\" \/> <\/object>";
	playerDiv=document.createElement('div');
	playerDiv.style.position="absolute";
	playerDiv.style.top=0;
	//playerDiv.id="playerDiv";
	playerDiv.style.left=0;
	playerDiv.style.zIndex=1120;//higher, higher!
	parentObj.appendChild(playerDiv);
    playerDiv.innerHTML=injectedHTML;

}
var ActivePlayer="";
var UrlsOfPlayers = new Array();
var oggPlayList=new Array();
var ActiveURL="";

function injectPlayerInterface(parentObj,IntfID,playURL)
{
	var injectedHTML="<div class='player_controls' id='controls"+IntfID+"'>";
	injectedHTML+="<table cellpadding=\"0\" cellspacing=\"0\" class='player_tbl player_inside' >";
	injectedHTML+="<tr class='player_row' id='plcntr"+IntfID+"'>	<td id='lside"+IntfID+"' width=\"5px\"><\/td>";
	injectedHTML+="<td id='cside' width=\"100px\"> <table cellpadding=\"0\" cellspacing=\"0\" class='player_tbl'>";
	injectedHTML+="<tr class='pl_1px c3'><td class='pl_1px'><\/td><\/tr>";
	injectedHTML+="<tr class='pl_1px'><td class='pl_1px'><\/td><\/tr><tr class='pl_btnrow'><td class='pl_btnrow'>";
	injectedHTML+="<table cellpadding=\"0\" cellspacing=\"0\" class='player_tbl'><tr class='pl_btn'>";
	injectedHTML+="<td id='play"+IntfID+"'><\/td><td class='pl_sep'><\/td><td id='list"+IntfID+"'><\/td><td class='pl_sep'><\/td><td id='stop"+IntfID+"'><\/td>";
	injectedHTML+="<td class='vol_sep'><\/td><td id='volume"+IntfID+"'><\/td><td class='vol_sep'><\/td><\/tr><\/table>";
	injectedHTML+="<\/td><\/tr>";
	injectedHTML+="<tr class='pl_pr_env'><td class='pl_pr_env'><table cellpadding=\"0\" cellspacing=\"0\" class='pl_pr_tab' ";
	injectedHTML+="onmousedown='onProgDown(event,\""+IntfID+"\")'>";
	injectedHTML+="<tr class='pl_pr_progress'><td class='pl_pr_pl tprb' id='pr-pl"+IntfID+"'><\/td><td class='pl_pr_ld tprb' id='pr-ld"+IntfID+"'><\/td>";
	injectedHTML+="<td class='pl_pr_em' id='pr-em"+IntfID+"'><\/td><\/tr><\/table>";
	injectedHTML+="<\/td><\/tr>";
	injectedHTML+="<tr class='pl_1px'><td class='pl_1px'><\/td><\/tr><tr class='pl_1px c3'><td class='pl_1px'><\/td><\/tr>";
	injectedHTML+="<\/table><\/td><td id='rside"+IntfID+"' width=\"5px\"><\/td><\/tr>	<\/table><\/div>";
	/*var cntrlDiv=document.createElement('div');
	cntrlDiv.id="div"+IntfID;
	parentObj.appendChild(cntrlDiv);
    cntrlDiv.innerHTML=injectedHTML;*/
    parentObj.innerHTML=injectedHTML;
	var playerBlock=document.getElementById("plcntr"+IntfID);
	var sideHeight=playerBlock.clientHeight;
	drawSide(true,sideHeight,"lside"+IntfID);
	drawSide(false,sideHeight,"rside"+IntfID);
	//buttons
	drawButton(PlayBtn,"play"+IntfID,"doPlay(\""+IntfID+"\",\""+playURL+"\")");
	drawButton(ListBtn,"list"+IntfID,"doEnlist(\""+IntfID+"\")");
	drawButton(StopBtn,"stop"+IntfID,"doStop(\""+IntfID+"\")");
	drawVolume(vVolume,"volume"+IntfID,IntfID);
	//associate
	UrlsOfPlayers[IntfID]=playURL;
}

function playerLoadConfirm()
{
	//alert("test");
	playerDiv.style.top="-400px";
	//playerDiv.style.display="none";
}
var nextSched=false;
function setModeStopped(stoptype)
{
	oggSetProgress(0,0);
	drawButton(PlayBtn,"play"+ActivePlayer,"doPlay(\""+ActivePlayer+"\",\""+ActiveURL+"\")");
	if((!nextSched) &&(oggPlayList.length>0)&&((stoptype=="streamstop")||(stoptype=="stopped"))){
		nextSched=true;
		setTimeout("doPlayNext()",50);
	}
	var display = document.getElementById("stt");
	display.innerHTML=display.innerHTML+":"+stoptype;
}

function doPlayNext()
{
	if((oggStatus!="playing")&&(oggStatus!="paused")){
		var display = document.getElementById("stt");
		display.innerHTML=display.innerHTML+":[playnext]:"+oggPlayList.length;
		var PlayerID=oggPlayList.shift();
		display.innerHTML=display.innerHTML+":"+PlayerID;
		var PlayURL=UrlsOfPlayers[PlayerID];
		setTimeout("doPlayNextTmr(\""+PlayerID+"\")",500);
	}
}

function doPlayNextTmr(PlayerID)
{
	var display = document.getElementById("stt");
	display.innerHTML=display.innerHTML+":[doTmr]:"+nextSched;
	nextSched=false;
	doPlay(PlayerID,UrlsOfPlayers[PlayerID]);
}

var oggError="ok";
function onStateChanged(state)
{
	if(state=="loaded")playerLoadConfirm();
	else if(state=="streamstop")setModeStopped("streamstop");
	else if(state=="stopped")setModeStopped("stopped");
	else if(state.indexOf("error",0)>-1)
	{
		var errmsg=state.split("=",3);
		oggError=errmsg[1];
		if((errmsg[1]=="underflow")||(errmsg[1]=="ioerror"))setModeStopped("stopped");
		else setModeStopped("error");
	}
}

function oggSetProgress(loaded,played)
{
	var loadedBar=document.getElementById("pr-ld"+ActivePlayer);
	var playedBar=document.getElementById("pr-pl"+ActivePlayer);
	var emptyBar=document.getElementById("pr-em"+ActivePlayer);
	if(played >= loaded)
	{
		loadedBar.style.width="0%";
		emptyBar.style.width=(100-loaded)+"%";
		playedBar.style.width=loaded+"%"
	}
	else
	{
		loadedBar.style.width=(loaded-played)+"%";
		emptyBar.style.width=(100-loaded)+"%";
		playedBar.style.width=played+"%"
	}
}



//play/stop command
var vVolume=60;
function doEnlist(PlayerID)
{
	oggPlayList.push(PlayerID);
}

function doPlay(PlayerID,playURL)
{
	if ((oggStatus=="stopped") || (oggStatus=="loaded") || (oggStatus=="streamstop"))
	{
		ActivePlayer=PlayerID;
		oggPlayURL(playURL);
		oggSetVolume(vVolume);
		drawVolume(vVolume,"volume"+PlayerID,PlayerID);
		drawButton(PauseBtn,"play"+PlayerID,"doPlay(\""+PlayerID+"\",\""+playURL+"\")");
		ActiveURL=playURL;
	}
	else if((oggStatus=="playing")||(oggStatus=="paused"))
	{
		if(ActivePlayer!=PlayerID)
		{
			oggStop();
			//put this on timer?
			ActivePlayer=PlayerID;
			oggPlayURL(playURL);
			oggSetVolume(vVolume);
			drawVolume(vVolume,"volume"+PlayerID,PlayerID);
			drawButton(PauseBtn,"play"+PlayerID,"doPlay(\""+PlayerID+"\",\""+playURL+"\")");
			ActiveURL=playURL;
		}
		else//pause
		{
			if(oggStatus=="playing")drawButton(PlayBtn,"play"+PlayerID,"doPlay(\""+PlayerID+"\",\""+playURL+"\")");
			else drawButton(PauseBtn,"play"+PlayerID,"doPlay(\""+PlayerID+"\",\""+playURL+"\")");
			oggPause();
		}
	}
}

function doStop(PlayerID)
{
	if(PlayerID==ActivePlayer)
	{
		//oggSetProgress(0,0);
		oggStop();
	}
}

var PlayBtn =[[2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2],
                        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                        [2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,2],
                        [2,0,1,1,1,1,0,0,0,0,0,0,0,0,0,2],

                        [2,0,1,1,1,1,1,1,0,0,0,0,0,0,0,2],
                        [2,0,1,1, 1,1,1,1, 1,1,0,0 ,0,0,0,2],
                        [2,0,1,1, 1,1,1,1 ,1,1,1,1, 0,0,0,2],
                        [2,0,1,1, 1,1,1,1 ,1,1,1,1, 1,1,0,2],

                        [2,0,1,1, 1,1,1,1 ,1,1,1,1, 0,0,0,2],
                        [2,0,1,1, 1,1,1,1, 1,1,0,0 ,0,0,0,2],
                        [2,0,1,1,1,1,1,1,0,0,0,0,0,0,0,2],
                        [2,0,1,1,1,1,0,0,0,0,0,0,0,0,0,2],

                        [2,0,1,1,0,0,0,0,0,0,0,0,0,0,0,2],
                        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
                        [2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2]];
var PauseBtn =[[2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,0,0,0,1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],

                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],

                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],

                        [2,0,0,0, 1,1,1,0, 0,1,1,1 ,0,0,0,2],
                        [2,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,2],
                        [2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2]];
var StopBtn =[[2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],

                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],

                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],
                        [2,0,0,1,1,1,1,1, 1,1,1,1 ,1,0,0,2],

                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2]];

var ListBtn =[[2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,0,1,1, 1,1,1,1 ,1,1,1,1 ,1,1,0,2],
                        [2,0,1,0, 0,0,0,0 ,0,0,0,0 ,0,1,0,2],

                        [2,0,1,0, 1,1,0,0 ,1,1,1,1 ,0,1,0,2],
                        [2,0,1,0, 0,0,0,0 ,0,0,0,0 ,0,1,0,2],
                        [2,0,1,0, 1,1,1,1 ,1,0,0,0 ,0,1,0,2],
                        [2,0,1,0, 0,0,0,0 ,0,0,0,0 ,0,1,0,2],

                        [2,0,1,0, 1,1,1,1 ,0,0,1,1 ,0,1,0,2],
                        [2,0,1,0, 0,0,0,0 ,0,0,0,0 ,0,1,0,2],
                        [2,0,1,0, 1,1,1,1, 1,1,1,1 ,0,1,0,2],
                        [2,0,1,0, 0,0,0,0 ,0,0,0,0 ,0,1,0,2],

                        [2,0,1,1, 1,1,1,1 ,1,1,1,1 ,1,1,0,2],
                        [2,0,0,0, 0,0,0,0 ,0,0,0,0 ,0,0,0,2],
                        [2,2,2,2, 2,2,2,2, 2,2,2,2, 2,2,2,2]];

function drawButton(whatButton,whereButton,whatOnClick)
{
	var i,j;
	var contents="<table width=\"16px\" cellpadding=\"0\" cellspacing=\"0\" class='tbtn' onclick='"+whatOnClick+"'>";
	for(i=0;i<15;i++){
		contents+="<tr>";
		for(j=0;j<16;j++){
			contents+="<td class='c"+whatButton[i][j]+"'><\/td>";
			//else contents+="<td class='c1'><\/td>";
		}
		contents+="<\/tr>";
	}
	contents+="<\/table>";
	var mydiv=document.getElementById(whereButton);
	mydiv.innerHTML=contents;
}

var SideRound =[[9,9,9,9,9],
                          [9,9,9,3,3],
                          [9,9,3,0,0],
                          [9,3,0,0,0],

                          [9,3,0,0,0],
                          [3,0,0,0,0],

                          [9,3,0,0,0],

                          [9,3,0,0,0],
                          [9,9,3,0,0],
                          [9,9,9,3,3],
                          [9,9,9,9,9]];
var SideRect =[[3,3,3,3,3],
                          [3,0,0,0,0],
                          [3,0,0,0,0],
                          [3,0,0,0,0],

                          [3,0,0,0,0],
                          [3,0,0,0,0],

                          [3,0,0,0,0],

                          [3,0,0,0,0],
                          [3,0,0,0,0],
                          [3,0,0,0,0],
                          [3,3,3,3,3]];
var Side=SideRound;

function drawSide(isLeft,totalHeight,drawWhere,colorCode)
{
	var i,j;
	var contents="<table width=\"5px\" cellpadding=\"0\" cellspacing=\"0\" class='tbtn'>";
	if(!colorCode)colorCode="c";
	for(i=0;i<5;i++){
		contents+="<tr>";
		for(j=0;j<5;j++){
			if(isLeft)
			{
				contents+="<td class='"+colorCode+Side[i][j]+"'><\/td>";
			}
			else
			{
				contents+="<td class='"+colorCode+Side[i][4-j]+"'><\/td>";
			}
		}
		contents+="<\/tr>";
	}
	for(i=0;i<totalHeight-10;i++){
		contents+="<tr>";
		for(j=0;j<5;j++){
			if(isLeft)
			{
				contents+="<td class='"+colorCode+Side[5][j]+"'><\/td>";
			}
			else
			{
				contents+="<td class='"+colorCode+Side[5][4-j]+"'><\/td>";
			}
		}
		contents+="<\/tr>";
	}
	for(i=0;i<5;i++){
			contents+="<tr>";
			for(j=0;j<5;j++){
				if(isLeft)
				{
					contents+="<td class='"+colorCode+Side[6+i][j]+"'><\/td>";
				}
				else
				{
					contents+="<td class='"+colorCode+Side[6+i][4-j]+"'><\/td>";
				}
			}
			contents+="<\/tr>";
	}
	contents+="<\/table>";
	var mydiv=document.getElementById(drawWhere);
	mydiv.innerHTML=contents;
}

function setVolume(percent,PlayerID)
{

	if(!PlayerID)PlayerID=ActivePlayer;
	if(PlayerID!=ActivePlayer)return;
	vVolume=percent;
	oggSetVolume(percent);
	drawVolume(percent,"volume"+PlayerID,PlayerID);
}

function drawVolume(fillPercent,whereVolume,PlayerID)
{
	var i,j,c;
	var contents="<table width=30px cellpadding=0 cellspacing=0 class='tbtn' id='volctrl"+PlayerID+
		"' onmousedown='onVolDown(event,\""+PlayerID+"\")' onmouseup='onVolUp(event,\""+PlayerID+
		"\")' onmousemove='onVolMove(event,\""+PlayerID+"\")' onmouseout='onVolLeave(event,\""+PlayerID+"\")'>";
	for(i=0;i<15;i++){
		contents+="<tr>";
		for(j=0;j<30;j++){
			if((j==29)||(i==14)||(i+Math.ceil(j/2)==14))
			{
				c=7;
			}
			else
			{
				if(i+(j/2)>14)c=6;
				else c=0;
			}
			if((j>fillPercent/3.3)&&(c==6))	c=5;
			contents+="<td class='c"+c+"'><\/td>";
		}
		contents+="<\/tr>";
	}
	contents+="<\/table>";
	var mydiv;
	if(whereVolume)mydiv=document.getElementById(whereVolume);
	else mydiv=document.getElementById("volume"+PlayerID);
	mydiv.innerHTML=contents;

}

function getAbsX(element)
{
	var iReturnValue = 0;
	while( element != null ) {
		iReturnValue += element.offsetLeft;
		element = element.offsetParent;
	}
	return iReturnValue;
}
var volDown;

function getEvtSource(event)
{
	if(event.srcElement)return event.srcElement;
	else return event.target;
}

function getEvtCoords(event)
{
	var posx = 0;
	var posy = 0;
	if (event.pageX || event.pageY) 	{
		posx = event.pageX;
		posy = event.pageY;
	}
	else if (event.clientX || event.clientY) 	{
		posx = event.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
		posy = event.clientY + document.body.scrollTop + document.documentElement.scrollTop;
	}
	var retval=[];
	retval.x=posx;
	retval.y=posy;
	return retval;
}

function onVolDown(event,PlayerID)
{
	if (event.preventDefault){
		event.preventDefault();
	}
	else
	{
		event.returnValue=false;
	}
	setVolume((getEvtCoords(event).x-getAbsX(getEvtSource(event).offsetParent))*3.3,PlayerID);
	volDown=true;
}


function onVolMove(event,PlayerID)
{
	if (event.preventDefault)event.preventDefault();//dont drag image
	else event.returnValue=false;
	if(volDown)
	{
		setVolume((getEvtCoords(event).x-getAbsX(getEvtSource(event).offsetParent))*3.3,PlayerID);
	}
	return false;
}
function onVolUp(event,PlayerID)
{
	if (event.preventDefault)event.preventDefault();//dont popup
	else event.returnValue=false;
	if(volDown)
	{
		volDown=false;
	}
}
function onVolLeave(event,PlayerID)
{
	if(volDown)
	{
			//volDown=false;
	}
}

function onProgDown(event,PlayerID)
{
	if (event.preventDefault){
		event.preventDefault();
	}
	else
	{
		event.returnValue=false;
	}
	var SeekPos=(getEvtCoords(event).x-getAbsX(getEvtSource(event).offsetParent));
	var SeekPossible=(getEvtSource(event).id=="pr-pl"+PlayerID)||(getEvtSource(event).id=="pr-ld"+PlayerID);
	if(SeekPossible &&(PlayerID==ActivePlayer))oggSeek(SeekPos/100);
}
