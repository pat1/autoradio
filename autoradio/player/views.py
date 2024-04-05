from django.shortcuts import render
import autoradio.settings


def playercmd(request, media):
    """
    player commander

    Template:  ``player/player.html``
    Context: play a media file

    """

    return render(request,'player/player.html', {'media': media})

def playernohtml5cmd(request, media):
    """
    player commander for no html5

    Template:  ``player/playernohtml5.html``
    Context: play a media file

    """

    return render(request,'player/playernohtml5.html', {'media': media})
