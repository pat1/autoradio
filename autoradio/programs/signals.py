from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enclosure
import mutagen
import logging

@receiver(post_save, sender=Enclosure)
def post_save__callback(sender, instance, created, **kwargs):
    if created:
        try:
            audio = mutagen.File(instance.file.path)
            if audio:
                audio.tags['ARTIST'] = instance.episode.show.title
                audio.tags['TITLE'] = instance.episode.title+" / "+instance.title
                audio.save()
        except:
            logging.error("Enclosure: error saving metadata Artist and Title")


            
