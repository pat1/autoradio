
#    audio/basic: mulaw audio at 8 kHz, 1 channel; Defined in RFC 2046
#    audio/L24: 24bit Linear PCM audio at 8-48kHz, 1-N channels; Defined in RFC 3190
#    audio/mp4: MP4 audio
#    audio/mpeg: MP3 or other MPEG audio; Defined in RFC 3003
#    audio/ogg: Ogg Vorbis, Speex, Flac and other audio; Defined in RFC 5334
#    audio/vorbis: Vorbis encoded audio; Defined in RFC 5215
#    audio/x-ms-wma: Windows Media Audio; Documented in MS kb288102[9]
#    audio/x-ms-wax: Windows Media Audio Redirector; Documented in MS kb288102[9]
#    audio/vnd.rn-realaudio: RealAudio; Documented in RealPlayer Help[10]
#    audio/vnd.wave: WAV audio; Defined in RFC 2361
#    audio/webm: WebM open media format


mymime_audio=("application/ogg","audio/mpeg", "audio/mp4", "audio/x-flac", "audio/x-wav") 
mymime_ogg=("application/ogg",)

webmime_audio = ("audio/mpeg","audio/mp3","audio/flac","video/ogg","audio/ogg","audio/oga", \
                     "audio/basic","audio/L24","audio/mp4","audio/vorbis","audio/x-ms-wma2",\
                     "audio/x-ms-wax","audio/vnd.rn-realaudio","audio/vnd.wave","audio/webm",\
                     "application/ogg","audio/wav")

websuffix_audio = (".mp3",".wav",".ogg",".oga",".flac",".Mp3",".Wav",".Ogg",".Oga",".Flac",".MP3",".WAV",".OGG",".OGA",".FLAC" )

webmime_ogg = ("video/ogg","audio/oga","audio/ogg","audio/oga","audio/vorbis","application/ogg")
websuffix_ogg = (".ogg",".oga",".Ogg",".Oga",".OGG")
