from django.shortcuts import render_to_response
import autoradio.settings


def playercmd(request, media):
    """
    player commander

    Template:  ``player/player.html``
    Context: play a media file

    """

    return render_to_response('player/player.html', {'media': media, 'site_media_url': autoradio.settings.SITE_MEDIA_URL })

def playernohtml5cmd(request, media):
    """
    player commander for no html5

    Template:  ``player/playernohtml5.html``
    Context: play a media file

    """

    return render_to_response('player/playernohtml5.html', {'media': media, 'site_media_url': autoradio.settings.SITE_MEDIA_URL })
