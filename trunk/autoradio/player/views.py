from django.shortcuts import render_to_response
import autoradio.settings


def playercmd(request, media):
    """
    player commander

    Template:  ``player/player.html``
    Context: play a media file

    """

    return render_to_response('player/player.html', {'media': media, 'media_url': autoradio.settings.MEDIA_URL })
