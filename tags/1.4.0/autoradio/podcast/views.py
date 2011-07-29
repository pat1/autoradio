from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.http import HttpResponseRedirect
from autoradio.podcast.models import Episode, Show, Enclosure
import autoradio.settings


def episode_detail(request, show_slug, episode_slug):
    """
    Episode detail

    Template:  ``podcast/episode_detail.html``
    Context:
        object_detail
            Detail of episode.
    """
    return object_detail(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=show_slug),
        slug=episode_slug,
        slug_field='slug',
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=show_slug).filter(episode__slug__exact=episode_slug).order_by('-episode__date'),'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/episode_detail.html')


def episode_list(request, slug):
    """
    Episode list

    Template:  ``podcast/episode_list.html``
    Context:
        object_list
            List of episodes.
    """
#    return object_list(
#        request,
#        queryset=Episode.objects.published().filter(show__slug__exact=slug),
#        extra_context={'media_url':autoradio.settings.MEDIA_URL},
#        template_name='podcast/episode_list.html')

# from: http://code.google.com/p/django-podcast/issues/detail?id=12

    try:
        show = Show.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(reverse('podcast_shows'))

    context = {'show':show, 'media_url':autoradio.settings.MEDIA_URL}
    return object_list(
        request,
        queryset=Episode.objects.published().filter(show__slug__exact=slug),
        template_name='podcast/episode_list.html',
        extra_context = context)


def episode_sitemap(request, slug):
    """
    Episode sitemap

    Template:  ``podcast/episode_sitemap.html``
    Context:
        object_list
            List of episodes.
    """
    return object_list(
        request,
        mimetype='application/xml',
        queryset=Episode.objects.published().filter(show__slug__exact=slug).order_by('-date'),
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/episode_sitemap.html')


def show_list(request):
    """
    Episode list

    Template:  ``podcast/show_list.html``
    Context:
        object_list
            List of shows.
    """
    return object_list(
        request,
        queryset=Show.objects.all().order_by('title'),
        extra_context={'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/show_list.html')


def show_list_feed(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/show_feed.html')


def show_list_media(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_media.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/show_feed_media.html')


def show_list_atom(request, slug):
    """
    Episode feed by show

    Template:  ``podcast/show_feed_atom.html``
    Context:
        object_list
            List of episodes by show.
    """
    return object_list(
        request,
        mimetype='application/rss+xml',
        queryset=Episode.objects.filter(show__slug__exact=slug).order_by('-date')[0:21],
        extra_context={
            'enclosure_list': Enclosure.objects.filter(episode__show__slug__exact=slug).order_by('-episode__date'),'media_url':autoradio.settings.MEDIA_URL},
        template_name='podcast/show_feed_atom.html')
