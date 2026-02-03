from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enclosure
import mutagen
import logging
import autoradio.settings
import subprocess
import os, shutil, tempfile

if not autoradio.settings.require_tags_in_enclosure:

    @receiver(post_save, sender=Enclosure)
    def post_save__callback(sender, instance, created, **kwargs):
        if created:    # created is false and 'update_fields': None when file is changed
            try:
                audio = mutagen.File(instance.file.path)
                if audio is not None:
                    audio.tags['ARTIST'] = "SHOW: "+instance.episode.show.title
                    audio.tags['TITLE'] = instance.episode.title+" / "+instance.title
                    audio.save()
            except:
                logging.error("Enclosure: error saving metadata Artist and Title")

            try:
                filename, extension = os.path.splitext(instance.file.path)
                with tempfile.TemporaryDirectory() as tmp:
                    tmppath = os.path.join(tmp, 'soxoutput'+extension)

                    # sox with output on tmp file
                    subprocess.check_call(["/usr/bin/sox","--norm"
                                       ,instance.file.path, tmppath
                                       ,"compand", "0.005,3","6:-100,-50,-60,-30,-9","-3","-90","0.2"])

                    # atomic file substitution
                    try:
                        os.replace(tmppath,instance.file.path)
                    except OSError as e:
                        if e.errno == 18:  # EXDEV - cross-device link
                            # Fall back to copy + delete
                            shutil.copy2(tmppath,instance.file.path)
                            os.unlink(tmppath)
                        else:
                            raise

                    #subprocess.check_call(["/usr/bin/mv","-f",tmppath,instance.file.path])
                    #os.rename(tmppath,instance.file.path)
            except:
                logging.error("Enclosure: error applying sox normalization and compander effect")
            try:
                subprocess.check_call(["/usr/bin/rsgain","custom","-l","-30","-c","a","-s","i",instance.file.path])
            except:
                logging.error("Enclosure: error applying rplaygain")
            
