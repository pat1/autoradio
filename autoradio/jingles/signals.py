from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Jingle
import mutagen
import logging
import autoradio.settings

if not autoradio.settings.require_tags_in_enclosure:

    @receiver(post_save, sender=Jingle)
    def post_save__callback(sender, instance, created, **kwargs):
        if created:     # created is false and 'update_fields': None when file is changed
            try:
                audio = mutagen.File(instance.file.path)
                if audio is not None:
                    audio.tags['ARTIST'] = "JINGLE"
                    audio.tags['TITLE'] = instance.jingle
                    audio.save()
            except:
                logging.error("Jingle: error saving metadata Artist and Title")


            
