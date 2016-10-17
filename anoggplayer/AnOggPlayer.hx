import org.xiph.system.Bytes;

import flash.Vector;
import flash.external.ExternalInterface;
import flash.events.Event;
import flash.events.ProgressEvent;
import org.xiph.fogg.SyncState;
import org.xiph.fogg.StreamState;
import org.xiph.fogg.Page;
import org.xiph.fogg.Packet;

import org.xiph.fvorbis.Info;
import org.xiph.fvorbis.Comment;
import org.xiph.fvorbis.DspState;
import org.xiph.fvorbis.Block;

import org.xiph.foggy.Demuxer;
//import org.xiph.foggy.DemuxerStatus;

import org.xiph.system.AudioSink;

class PAudioSink extends AudioSink {
    /**
       A very quick&dirty wrapper around the AudioSink to somewhat
       make up for the lack of a proper demand-driven ogg demuxer a.t.m.
     */

    var cb_threshold : Int;
    var cb_pending : Bool;
    var cb : PAudioSink -> Void;

    public function new(chunk_size : Int, fill = true, trigger = 0) {
        super(chunk_size, fill, trigger);
        cb_threshold = 0;
        cb = null;
        cb_pending = false;

    }

    public function set_cb(threshold : Int, cb : PAudioSink -> Void) : Void {
        cb_threshold = threshold;
        this.cb = cb;
    }

    override function _data_cb(event : flash.events.SampleDataEvent) :Void {
        super._data_cb(event);

        if (cb_threshold > 0) {
            if (available < cb_threshold && !cb_pending) {
                cb_pending = true;
                haxe.Timer.delay(_delayed_cb, 1);
            }
        }
    }

    function _delayed_cb() : Void {
        this.cb_pending = false;
        this.cb(this);
    }

    override public function write(pcm : Array<Vector<Float>>,
                                   index : Vector<Int>, samples : Int) : Void {
        super.write(pcm, index, samples);

        if (cb_threshold > 0) {
            if (available < cb_threshold && !cb_pending) {
                cb_pending = true;
                haxe.Timer.delay(_delayed_cb, 1);
            }
        }
    }
}

class AnMp3Player {
    var mp3Sound:flash.media.Sound;
    var mp3Request:flash.net.URLRequest;
    var bIsPlaying: Bool;
    var nItfPlayMode: Int; //0=stop, 1=play, 2=pause
    var onProgress:flash.events.ProgressEvent -> Void;
    var onID3:flash.events.Event -> Void;
    var statusCB : String -> Void;
    var bufferCB : Int -> Void;
    var newSongCB: String -> Void;
    var onError: flash.events.IOErrorEvent -> Void;
    var volume: Int;
    var sch:flash.media.SoundChannel;
    var onSoundComplete:Event -> Void;
    var onProgressCB: Int -> Int -> Void;
    var bytesLoaded: Int;
    var bytesTotal: Int;
    var bytesPlayed: Int;
    var pausePos : Float;
    var playTimer: haxe.Timer;
    
    function DoProgress(event:ProgressEvent):Void {
    	bytesLoaded = cast(event.bytesLoaded,Int);
    	bytesTotal = cast(event.bytesTotal,Int);
    	doOnProgress(Math.ceil(bytesLoaded*100/bytesTotal),bytesPlayed);
    	if(mp3Sound.isBuffering)doBuffer(50)
        else {
      		if(!bIsPlaying){
      			if(nItfPlayMode==1)
      			{
      				doBuffer(100);
      				bIsPlaying=true;
      				doStatus("playing");
      			}
      		}	
        }
    }
    
    function doBuffer(value: Int) :Void {
            if(bufferCB != null) bufferCB(value);
    }
    
    function doOnProgress(loaded: Int, played: Int): Void {
    	if(onProgressCB != null) onProgressCB(loaded,played);
    }
    
    function doStatus(state: String) :Void {
    	trace("mp3:"+state);
            if(statusCB != null) statusCB(state);
    }
    
    function DoSoundComplete(e:Event):Void {
        bIsPlaying=false;
        trace("mp3 sound complete");
        doStatus("stopped");
        nItfPlayMode=0;
    }
    
    function DoID3(event:Event):Void {
    	var statstring: String;
    	statstring = "Artist"+ "=\""+StringTools.replace(mp3Sound.id3.artist,"\"","\"\"")+"\";";
    	statstring+="Title"+"=\""+StringTools.replace(mp3Sound.id3.songName,"\"","\"\"")+"\";";
    	statstring+="Album"+"=\""+StringTools.replace(mp3Sound.id3.album,"\"","\"\"")+"\";";
    	statstring+="Genre"+"=\""+StringTools.replace(mp3Sound.id3.genre,"\"","\"\"")+"\";";
    	if(newSongCB != null) newSongCB(statstring);
    }
    
    function DoError(event:flash.events.IOErrorEvent):Void {
    	doStatus("error=ioerror");
    	bIsPlaying=false;
    	nItfPlayMode=0;
    }
    function DoPlayTimer(): Void{
        if(bIsPlaying)
        {
           if (sch !=null)bytesPlayed=Math.ceil(sch.position*100/ mp3Sound.length+1);
           doOnProgress(Math.ceil(bytesLoaded*100/bytesTotal),bytesPlayed);
        }
    }

    
    public function setNewSongCB(newCB : String -> Void): Void {
            newSongCB = newCB;
    }
    //-----------------
    public function setBufferCB(newCB : Int -> Void): Void {
        bufferCB = newCB;
    }
     
    public function setProgressCB(newCB: Int -> Int -> Void): Void{
    	onProgressCB = newCB;
    }
    
    public function setStatusCB(newCB : String -> Void): Void {
        statusCB = newCB;
    }
    
    
    public function new() {
    	onProgress=DoProgress;
    	onID3=DoID3;
    	onError=DoError;
    	onSoundComplete=DoSoundComplete;
    	sch = null;
    	bytesPlayed=0;
    	playTimer = new haxe.Timer(500);
    	playTimer.run = DoPlayTimer;
    	nItfPlayMode = 0;
    	pausePos=0;
    }
    public function setVolume(vol:Int):Void {
    	var strans:flash.media.SoundTransform;
    	volume=vol;
    	if(sch != null) {
    		strans = sch.soundTransform;
		strans.volume = (volume+0.0001)/100;
    	   	sch.soundTransform = strans;
    	}
    
    }
    public function playMP3 ( murl:String):Void {
        trace("playMP3: "+murl);
        nItfPlayMode = 1;//play!
        bIsPlaying = false;
        mp3Request = new flash.net.URLRequest(murl);
        mp3Sound = new flash.media.Sound();
        mp3Sound.load(mp3Request);
        mp3Sound.addEventListener(flash.events.ProgressEvent.PROGRESS, onProgress);
        mp3Sound.addEventListener(Event.ID3, onID3);
        mp3Sound.addEventListener(flash.events.IOErrorEvent.IO_ERROR, onError);
        sch = mp3Sound.play(0,0);
        sch.addEventListener(Event.SOUND_COMPLETE,onSoundComplete);
        doStatus("buffering");
        setVolume(volume);
        pausePos=0;
    }
    
    public function stopMP3() :Void {
    	//trace(".mp3 stopping");
    	//doStatus("stopped");
    	bIsPlaying=false;
    	nItfPlayMode = 0;
    	if(sch!= null)sch.stop();
    	pausePos=0;
    	try
    	{
    		mp3Sound.close();
    	}catch (e:flash.errors.IOError){
    		
    	}
    	trace(" mp3 stopped");
    }
    
    public function pauseMP3():Void{
    	if(pausePos==0){//do pause
    		if(sch!=null)
    		{
    			pausePos=sch.position;
    			sch.stop();
    			nItfPlayMode=2;
    		}
    	}else{
    		sch=mp3Sound.play(pausePos);
    		setVolume(volume);
    		pausePos=0;
    		nItfPlayMode=1;
    		sch.addEventListener(Event.SOUND_COMPLETE,onSoundComplete);
    	}
    }
    public function seekMp3(seekPos:Float):Int{
    	var target_pos:Int =Math.ceil(mp3Sound.length*seekPos);
    	target_pos=Math.ceil(Math.max(target_pos,1000));//from 1 sec
    	var needResume:Bool =(pausePos==0);
    	if(pausePos==0)pauseMP3();
    	pausePos=target_pos;
    	if(needResume)pauseMP3();
    	return 1;
    }
    public function isPlaying(): Bool {
    	return bIsPlaying;
    }
    public function getPlayMode():Int
    {
    	return(nItfPlayMode);
    }
 
}

/* ANOnymous-delivered Ogg Player for ANOma.fm :3 */
class AnOggPlayer {
    var ul : flash.net.URLStream;
    var asink : PAudioSink;
    var url : String;
    var volume : Int;
    var mp3player:AnMp3Player;
    var bytesTotal : Int;
    var bytesLoaded : Int;
    var bytesPlayed: Int;
    var playBuffer:flash.utils.ByteArray;
    var whatPlayer:Int;//0 for ogg, 1 for mp3;
    var isPaused:Bool;
    // FIXME: find a better way to initialize those static bits?
    static function init_statics() : Void {
        org.xiph.fogg.Buffer._s_init();
        org.xiph.fvorbis.FuncFloor._s_init();
        org.xiph.fvorbis.FuncMapping._s_init();
        org.xiph.fvorbis.FuncTime._s_init();
        org.xiph.fvorbis.FuncResidue._s_init();
    }

    var _packets : Int;
    var vi : Info;
    var vc : Comment;
    var vd : DspState;
    var vb : Block;
    var dmx : Demuxer;

    var _pcm : Array<Array<Vector<Float>>>;
    var _index : Vector<Int>;

    var read_pending : Bool;
    var read_started : Bool;
    var read_buff_pending: Bool;
    var buff_write_pos:Int;
    var play_buffered:Bool;//use buffer, don't set to true for streaming?
    var streamDetected:Bool;//do NOT use buffer.
    
    function _proc_packet_head(p : Packet, sn : Int) : DemuxerStatus {
        vi.init();
        vc.init();
        if (vi.synthesis_headerin(vc, p) < 0) {
            // not vorbis - clean up and ignore
            vc.clear();
            vi.clear();
        } else {
            // vorbis - detach this cb and attach the main decoding cb
            // to the specific serialno
            //dmx.remove_packet_cb(-1);
            dmx.set_packet_cb(sn, _proc_packet);
        }
	_packets = 0;
        _packets++;
        return dmx_ok;
    }

    function _proc_packet(p : Packet, sn : Int) : DemuxerStatus {
        var samples : Int;

        switch(_packets) {
        case 0:
            /*
            vi.init();
            vc.init();
            if (vi.synthesis_headerin(vc, p) < 0) {
                return dmx_ok;
            } else {
                dmx.set_packet_cb(sn, _proc_packet);
                dmx.remove_packet_cb(-1);
            }
            */
        case 1:
            vi.synthesis_headerin(vc, p);

        case 2:
            vi.synthesis_headerin(vc, p);

            {
                var ptr : Array<Bytes> = vc.user_comments;
                var j : Int = 0;
                var comments : String;
                var comment: Array<String>;
                //trace("");
                comments="";
                while (j < ptr.length) {
                    if (ptr[j] == null) {
                        break;
                    };
                    comment = System.fromBytes(ptr[j], 0, ptr[j].length - 1).split("=");
                    comments = comments+comment[0];
		    comments = comments +"=\""+StringTools.htmlEscape(StringTools.replace(comment[1],"\"","\"\""))+"\";";
                    trace(System.fromBytes(ptr[j], 0, ptr[j].length - 1));
                    j++;
                };
                _doNewSong(comments);
		
                trace("Bitstream is " + vi.channels + " channel, " +
                      vi.rate + "Hz");
                trace(("Encoded by: " +
                       System.fromBytes(vc.vendor, 0, vc.vendor.length - 1)) +
                      "\n");
            }

            vd.synthesis_init(vi);
            vb.init(vd);

            _pcm = [null];
            _index = new Vector(vi.channels, true);

        default:
            if (vb.synthesis(p) == 0) {
                vd.synthesis_blockin(vb);
            }

            while ((samples = vd.synthesis_pcmout(_pcm, _index)) > 0) {
                asink.write(_pcm[0], _index, samples);
                vd.synthesis_read(samples);
            }
        }

        _packets++;

        return dmx_ok;
    }

    function _read_data() : Void {
        var to_read : Int = ul.bytesAvailable;
        //var chunk : Int = 8192;
        var chunk : Int = 16384;//test?
        //trace("read_data: " + ul.bytesAvailable+" to read: "+to_read);
        read_pending = false;

        if (to_read == 0)
            return;

        if (to_read < chunk && !read_pending) {
            read_pending = true;
            haxe.Timer.delay(_read_data, 50);
            return;
        }

        to_read = ul.bytesAvailable;
        if (to_read > chunk) {
            to_read = chunk;
        }
	
        /*this was here, now we read to buffer, not to demuxer
        dmx.read(ul, to_read);
        bytesPlayed+=to_read;
        _doProgress(Math.ceil(bytesLoaded*100/(bytesTotal+2)),Math.ceil(bytesPlayed*100/(bytesTotal+2)));
        */
        to_read=ul.bytesAvailable;
        ul.readBytes(playBuffer,buff_write_pos,/*chunk*/to_read);
        buff_write_pos+=to_read;
       // bytesPlayed+=to_read;
    }
    
    function _read_buffer():Void{
     	var to_read : Int = playBuffer.bytesAvailable;
    	//var chunk : Int = 8192;
    	var chunk : Int = 16384;//test?
    	var did_read:Int=0;
    	//trace("read_data: " + ul.bytesAvailable+" to read: "+to_read);
    	read_buff_pending = false;

    	if (to_read == 0)
		return;

    	if (to_read < chunk && !read_buff_pending) {
		read_buff_pending = true;
		haxe.Timer.delay(_read_buffer, 50);
		return;
    	}
	/*else if(to_read<chunk && !play_buffered){
		return;
	}
	*/
    	to_read = playBuffer.bytesAvailable;
    	if (to_read > chunk) {
		to_read = chunk;
    	}

    	did_read=dmx.read(playBuffer, to_read);
    	if(did_read==to_read)
    	{
    		bytesPlayed+=to_read;
    		if((!play_buffered)||(streamDetected))
    		{//kill off buffer
    			
    			/*
    			buff_write_pos=playBuffer.bytesAvailable;
    			System.bytescopy(playBuffer,playBuffer.position,playBuffer, 0, playBuffer.bytesAvailable);
    			playBuffer.position=0;*/
    			var tmp:flash.utils.ByteArray = new flash.utils.ByteArray();
    			playBuffer.readBytes(tmp);
    			playBuffer=tmp;
    			buff_write_pos=playBuffer.length;
    			
    		}
		_doProgress(Math.ceil(bytesLoaded*100/(bytesTotal+2)),Math.ceil(bytesPlayed*100/(bytesTotal+2)));    
    	}
    }
    
    function _seek_ogg(seek_pos:Float):Int {
    	var target_pos,target_step:Int;
    	target_pos=Math.ceil(bytesTotal*seek_pos);
    	target_step=Math.ceil(Math.max(Math.ceil(target_pos/16384),3));
    	target_pos=target_step*16384;
    	if(playBuffer.length > cast(target_pos,UInt)){
    		bytesPlayed=target_pos;
    		playBuffer.position=target_pos;
    		return 1;
    	}
    	else
    	{
    		return 0;
    	}
    }
    
    function try_ogg() : Void {
        dmx = new Demuxer();

        vi = new Info();
        vc = new Comment();
        vd = new DspState();
        vb = new Block(vd);

        _packets = 0;

        dmx.set_packet_cb(-1, _proc_packet_head);

        //asink = new PAudioSink(8192, true, 132300);
        asink = new PAudioSink(8192, true, 132300);//params: data chunk for Sound.onSampleData, doFill with zeroes, trigger play after...
        asink.setBufferCB(_doBuffer);
        asink.setStatusCB(_doState);
        asink.setVolume(volume);
        asink.set_cb(88200, _on_data_needed);
    }
 //----------------------------------------------------------------   
    function _playURL ( murl:String ): Void {
    	trace("playURL: "+murl);
    	playBuffer=new flash.utils.ByteArray();
    	streamDetected=false;
    	oldBytesTotal=0;//nothing loaded
    	buff_write_pos=0;
    	url=murl;
    	bytesPlayed =0;
    	isPaused=false;
    	if(StringTools.endsWith(url,"ogg")||StringTools.endsWith(url,"OGG")||StringTools.endsWith(url,"Ogg")) {
    		_doState("buffering");
    		ul.load(new flash.net.URLRequest(url));
    		whatPlayer=0;//ogg
    	}
    	else if(StringTools.endsWith(url,"mp3")||StringTools.endsWith(url,"MP3")||StringTools.endsWith(url,"Mp3")) {
    		_playMP3(murl);
    	}
    	else
    	{
    		_doState("error=unsupported_format");
    	}
    }
    function _playMP3 (murl:String):Void {
    	trace("playing mp3");
    	whatPlayer=1;//mp3
    	mp3player = new AnMp3Player();
    	mp3player.setNewSongCB(_doNewSong);
    	mp3player.setStatusCB(_doState);
    	mp3player.setBufferCB(_doBuffer);
    	mp3player.setProgressCB(_doProgress);
    	mp3player.playMP3(murl);
    }
 //---------------------------------------------------   
    function _stopPlay() : Void {
    	trace("stopPlay!");
    	isPaused=false;
    	try {
    		if(mp3player!=null){
		    		trace("stopping mp3");
		    		mp3player.stopMP3();
		    		
    		}
    		if(asink!=null) {
    			asink.stop();
    			ul.close();
    			playBuffer=null;
    		}
    	} catch( msg : String ) {
		    trace("Error occurred: " + msg);
	}
    	whatPlayer=-1;
    	_doState("stopped");
    }
//----------------------------------------------------    
    function _pausePlay() : Void {
    	trace(whatPlayer);
    	if(whatPlayer==0)
    	{
    		//ogg pause routine
    		if(!isPaused){
    			asink.stop();
    			isPaused=true;
    			_doState("paused");
    		}
    		else{
    			asink.play();
    			isPaused=false;
    			_doState("playing");
    		}
    	}
    	else if(whatPlayer==1)
    	{
    		//mp3 pause routine
    		if(mp3player.getPlayMode()==2)
    		{//unpause
    			mp3player.pauseMP3();
    			_doState("playing");
    		}
    		else
    		{//pause
    			mp3player.pauseMP3();
    			_doState("paused");
    		}
    	}
    }
    //----------------------------------------------------
    function _seekPlay(pos:Float): Void {
    	if(whatPlayer==0)
    	{
    		asink.stop();
    		if(_seek_ogg(pos)>0){
    			asink.resetBuffer();
    			_read_buffer();
    			_read_buffer();
    			_read_buffer();
    		}
    		asink.play();
    	}
    	else
    	{
    		mp3player.seekMp3(pos);
    	}
    	
    }
 //----------------------------------------------------   
    function _setVolume(vol: Int) : Void {
    	volume = vol;
    	if(asink!=null) asink.setVolume(vol);
    	if(mp3player!=null)mp3player.setVolume(vol);
    }
    
    function _doState(state: String) : Void {
    	if(state=="stopped")whatPlayer = -1;
    	flash.external.ExternalInterface.call("onOggState",state);
    }
    
    function _doBuffer(fill : Int) : Void {
    	flash.external.ExternalInterface.call("onOggBuffer",fill);
    }
    
    function _doNewSong(headers:String) : Void {
    	flash.external.ExternalInterface.call("onOggSongBegin",headers);
    }
   
   function _doProgress(loaded:Int,played:Int):Void {
   	if(streamDetected)
   	{
   		loaded=100;
   		if((whatPlayer==0)&&(asink!=null))
   		{
   			played=Math.ceil(asink.available*100/(132300*3));
   		}
   	}
   	flash.external.ExternalInterface.call("onOggProgress",loaded,played);
   }
   
    function start_request() : Void {
        trace("Starting downloading: " + url);
        
        ul = new flash.net.URLStream();

        ul.addEventListener(flash.events.Event.OPEN, _on_open	);
        ul.addEventListener(flash.events.ProgressEvent.PROGRESS, _on_progress);
        ul.addEventListener(flash.events.Event.COMPLETE, _on_complete);
        ul.addEventListener(flash.events.IOErrorEvent.IO_ERROR, _on_error);
        ul.addEventListener(flash.events.SecurityErrorEvent.SECURITY_ERROR,
                            _on_security);
	_doState("loaded");
        //ul.load(new flash.net.URLRequest(url));
    }

    function _on_open(e : flash.events.Event) : Void {
        read_pending = false;
        read_started = false;
        try_ogg();
    }
    var oldBytesTotal:Int;
    var adjustCount:Int; 
    var _bootstrap_pending:Bool;
    
    function _on_progress(e : flash.events.ProgressEvent) : Void {
        //trace("on_progress: " + ul.bytesAvailable);
        bytesLoaded = cast(e.bytesLoaded,Int);
        if(oldBytesTotal==0){
        	_bootstrap_pending=false;
        	read_started=false;
        	oldBytesTotal=bytesTotal;
        	if(adjustCount>3)adjustCount=0;
        	if(!streamDetected)trace("adjust "+adjustCount+": size "+bytesTotal);
        }
        bytesTotal = cast(e.bytesTotal,Int);
        if((bytesTotal==0)&&(!streamDetected))
        {
        	adjustCount++;
        	if(adjustCount>3)
        	{
        		trace("Microsoft idea of streaming detected :3");
        		streamDetected=true;
        	}
        }
        if(oldBytesTotal!=bytesTotal)
        {
        	oldBytesTotal=bytesTotal;
        	if(!streamDetected)
        	{
        		adjustCount++;
        		trace("adjust "+adjustCount+": size "+bytesTotal);
        		if(adjustCount>10)
        		{
        			trace("streaming Ogg detected");
        			streamDetected=true;
        			adjustCount=0;
        		}
        	}
        }
        _doProgress(Math.ceil(bytesLoaded*100/(bytesTotal+2)),Math.ceil(bytesPlayed*100/(bytesTotal+2)));
        if (ul.bytesAvailable > 16284){
            _read_data();
            if (!read_started ) {
               //to fix immediate preload on ogg on IE 6
                if(!_bootstrap_pending)_bootstrap_read();
            }
        }
    }
    //this functions hand-feeds audiosink new data until it starts playing on it's own
    function _bootstrap_read():Void
    {
    	_bootstrap_pending=false;
    	_read_buffer();//this function feeds the actual data
    	if((!asink.triggered)&&(!_bootstrap_pending))
    	{
    		_bootstrap_pending=true;
    		haxe.Timer.delay(_bootstrap_read, 50);
    		return;
    	}
    	
    }
    function _on_complete(e : flash.events.Event) : Void {
        //trace("Found ? pages with " + _packets + " packets.");
        trace("\n\n=====   Loading '" + url + "'done. Enjoy!   =====\n");
    }

    function _on_error(e : flash.events.IOErrorEvent) : Void {
        trace("error occured: " + e);
        _doState("error=ioerror");
    }

    function _on_security(e : flash.events.SecurityErrorEvent) : Void {
        trace("security error: " + e);
        _doState("error=securerror");
    }

    function _on_data_needed(s : PAudioSink) : Void {
         //trace("on_data: " + ul.bytesAvailable);
        read_started = true;
        //_read_data();
      	_read_buffer();
    }


    static function check_version() : Bool {
        if (flash.Lib.current.loaderInfo.parameters.noversioncheck != null)
            return true;

        var vs : String = flash.system.Capabilities.version;
        var vns : String = vs.split(" ")[1];
        var vn : Array<String> = vns.split(",");

        if (vn.length < 1 || Std.parseInt(vn[0]) < 10)
            return false;

        if (vn.length < 2 || Std.parseInt(vn[1]) > 0)
            return true;

        if (vn.length < 3 || Std.parseInt(vn[2]) > 0)
            return true;

        if (vn.length < 4 || Std.parseInt(vn[3]) >= 525)
            return true;

        return false;
    }

    private function new(url : String) {
        this.url = url;
        whatPlayer=-1;
        play_buffered=true;
    }

    public static function main() : Void {
        if (check_version()) {
            init_statics();
	    
            var fvs : Dynamic<String> = flash.Lib.current.loaderInfo.parameters;
            var url = fvs.playUrl == null ? "http://comodino.org:8001/null.ogg" : fvs.playUrl;

            var foe = new AnOggPlayer(url);
            foe.volume=100;
            flash.system.Security.allowDomain("*");
            flash.external.ExternalInterface.addCallback("playURL",foe._playURL);
            flash.external.ExternalInterface.addCallback("stopPlaying",foe._stopPlay);
            flash.external.ExternalInterface.addCallback("setVolume",foe._setVolume);
            flash.external.ExternalInterface.addCallback("pausePlay",foe._pausePlay);
            flash.external.ExternalInterface.addCallback("Seek",foe._seekPlay);
            //foe._playURL("called from self");
            foe.start_request();
        } else {
            trace("You need a newer Flash Player.");
            trace("Your version: " + flash.system.Capabilities.version);
            trace("The minimum required version: 10.0.0.525");
            flash.external.ExternalInterface.call("onOggState","error=need_flash_10.0.0.525_or_better");
        }
    }
}
