HAXE = haxe
HX_FILES = 				\
	org/xiph/fogg/Buffer.hx		\
	org/xiph/fogg/SyncState.hx	\
	org/xiph/fogg/Packet.hx		\
	org/xiph/fogg/StreamState.hx	\
	org/xiph/fogg/Page.hx		\
	org/xiph/foggy/Demuxer.hx	\
	org/xiph/system/Bytes.hx	\
	org/xiph/system/AudioSink.hx	\
	org/xiph/fvorbis/Block.hx	\
	org/xiph/fvorbis/CodeBook.hx	\
	org/xiph/fvorbis/Comment.hx	\
	org/xiph/fvorbis/Drft.hx	\
	org/xiph/fvorbis/DspState.hx	\
	org/xiph/fvorbis/EncodeAuxNearestMatch.hx	\
	org/xiph/fvorbis/EncodeAuxThreshMatch.hx	\
	org/xiph/fvorbis/Floor0.hx	\
	org/xiph/fvorbis/Floor1.hx	\
	org/xiph/fvorbis/FuncFloor.hx	\
	org/xiph/fvorbis/FuncMapping.hx	\
	org/xiph/fvorbis/FuncResidue.hx	\
	org/xiph/fvorbis/FuncTime.hx	\
	org/xiph/fvorbis/Info.hx	\
	org/xiph/fvorbis/InfoMode.hx	\
	org/xiph/fvorbis/Lookup.hx	\
	org/xiph/fvorbis/Lpc.hx		\
	org/xiph/fvorbis/Lsp.hx		\
	org/xiph/fvorbis/Mapping0.hx	\
	org/xiph/fvorbis/Mdct.hx	\
	org/xiph/fvorbis/PsyInfo.hx	\
	org/xiph/fvorbis/Residue0.hx	\
	org/xiph/fvorbis/Residue1.hx	\
	org/xiph/fvorbis/Residue2.hx	\
	org/xiph/fvorbis/StaticCodeBook.hx	\
	org/xiph/fvorbis/Time0.hx	\
	System.hx			\
	ArrayTools.hx			\
	VectorTools.hx

AnOgg.swf: build.hxml AnOggPlayer.hx $(HX_FILES)
	$(HAXE) -cp . -swf-version 10 -swf-header 200:200:30:000000 build.hxml

clean:
	rm -f AnOgg.swf

