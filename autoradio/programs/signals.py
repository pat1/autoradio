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

        companderdone=False
        try:
            audio = mutagen.File(instance.file.path)
            if audio is not None:
                logging.info(f"Enclosure: {instance.file.path} apply tags")
                audio.tags['ARTIST'] = "SHOW: "+instance.episode.show.title
                audio.tags['TITLE'] = instance.episode.title+" / "+instance.title
                companderdone=audio.tags.get('COMPANDER',["not done",])[0] =="done"
                audio.save()
        except:
            logging.error(f"Enclosure: {instance.file.path} error saving metadata Artist and Title")

        # compander is not reversible so I check if is already done by tag

        if (created and not companderdone):    # created is false and 'update_fields': None when file is changed
            logging.info(f"Enclosure: {instance.file.path} apply compander")
            try:
                filename, extension = os.path.splitext(instance.file.path)
                with tempfile.TemporaryDirectory() as tmp:
                    tmppath = os.path.join(tmp, 'soxoutput'+extension)

                    # sox with output on tmp file
                    subprocess.check_call(["/usr/bin/sox"
                                       ,instance.file.path, tmppath
                                       ,"norm","0"
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
                logging.error(f"Enclosure: {instance.file.path} applying sox normalization and compander effect")
                
            try:
                logging.info(f"Enclosure: {instance.file.path} apply rsgain")
                subprocess.check_call(["/usr/bin/rsgain","custom","-s","i",instance.file.path])
            except:
                logging.error(f"Enclosure: {instance.file.path}  error applying replaygain (rsgain)")
            
            try:
                audio = mutagen.File(instance.file.path)
                if audio is not None:
                    logging.info(f"Enclosure: {instance.file.path} apply tag COMPANDER")
                    audio.tags['COMPANDER'] = "done"
                    audio.save()
            except:
                logging.error(f"Enclosure: {instance.file.path} error saving metadata COMPANDER done")
