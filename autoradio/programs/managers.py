from django.db.models import Manager
import datetime


class EpisodeManager(Manager):
    """Returns public posts that are not in the future."""
    def __init__(self, *args, **kwargs):
        super(EpisodeManager, self).__init__(*args, **kwargs)

    def published(self):
        return self.get_queryset().filter(status__exact=2, date__lte=datetime.datetime.now())
