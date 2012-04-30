from django.db import models
from django.utils.translation import ugettext_lazy
import datetime
import calendar
from autoradio.autoradio_config import *


from  django import VERSION as djversion

if ((djversion[0] == 1 and djversion[1] >= 3) or 
    djversion[0] > 1):

    from django.db import models
    from django.db.models import signals

    class DeletingFileField(models.FileField):
        """
        FileField subclass that deletes the refernced file when the model object
        itself is deleted.
        
        WARNING: Be careful using this class - it can cause data loss! This class
        makes at attempt to see if the file's referenced elsewhere, but it can get
        it wrong in any number of cases.
       """
        def contribute_to_class(self, cls, name):
            super(DeletingFileField, self).contribute_to_class(cls, name)
            signals.post_delete.connect(self.delete_file, sender=cls)
        
        def delete_file(self, instance, sender, **kwargs):
            file = getattr(instance, self.attname)
            # If no other object of this type references the file,
            # and it's not the default value for future objects,
            # delete it from the backend.
            
            if file and file.name != self.default and \
                    not sender._default_manager.filter(**{self.name: file.name}):
                file.delete(save=False)
            elif file:
                # Otherwise, just close the file, so it doesn't tie up resources.
                file.close()
        
else:
    DeletingFileField=models.FileField

def giorno_giorno():
	giorni=[]
	for giorno in (calendar.day_name):
		giorno=giorno.decode('utf-8')
		giorni.append(( giorno, giorno))
	return giorni
#	yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True,\
                                    help_text=ugettext_lazy("weekday name"))
        def __unicode__(self):
            return self.name

class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True\
					   ,default='playlist',editable=False)

	active = models.BooleanField(ugettext_lazy("Activate Playlist"),default=True,\
                                         help_text=ugettext_lazy("activate/deactivate the intere playlist class"))
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'),null=True,blank=True,\
                                                  help_text=ugettext_lazy("The start time from wich the playlist will be active"))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed start time'),null=True,blank=True,\
                                            help_text=ugettext_lazy("The end time the playlist will be active"))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "\
		+self.emission_starttime.isoformat()+" "\
		+self.emission_endtime.isoformat()


class Playlist(models.Model):
    playlist = models.CharField(ugettext_lazy('Playlist name'),max_length=200)
    file = DeletingFileField(ugettext_lazy('File'),upload_to='playlist',max_length=255,\
                                 help_text=ugettext_lazy("The playlist file to upload, format should be extm3u, m3u, pls"))
    rec_date = models.DateTimeField(ugettext_lazy('Generation date'),\
                                                      help_text=ugettext_lazy("When the playlist was done (for reference only)"))
    active = models.BooleanField(ugettext_lazy("Active"),default=True,\
                                     help_text=ugettext_lazy("Activate the playlist for emission"))

 
    def was_recorded_today(self):
        return self.rec_date.date() == datetime.date.today()
    
    was_recorded_today.short_description = ugettext_lazy('Generated today?')

    def __unicode__(self):
        #return self.playlist+" "+self.rec_date.isoformat()+" "+self.active.__str__()
        return self.playlist

class Schedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    playlist = models.ForeignKey(Playlist, verbose_name=\
					ugettext_lazy('refer to playlist:'))

    shuffle = models.BooleanField(ugettext_lazy("Shuffle Playlist on start"),default=True,\
                                      help_text=ugettext_lazy("Every time the playlist will be scheduled it's order will be randomly changed"))
    length = models.FloatField(ugettext_lazy("Max time length (seconds)"),default=None,null=True,blank=True,\
                                   help_text=ugettext_lazy("If this time is set the playlist will be truncated"))
    emission_date = models.DateTimeField(ugettext_lazy('Programmed date'),\
                                             help_text=ugettext_lazy("This is the date and time when the playlist will be on air"))

# da reinserire !
#    start_date = models.DateField('Data inizio programmazione',null=True,blank=True)
#    end_date = models.DateField('Data fine programmazione',null=True,blank=True)
#    time = models.TimeField('Ora programmazione',null=True,blank=True)
#    giorni = models.ManyToManyField(Giorno,verbose_name='Giorni programmati',null=True,blank=True)
    
    emission_done = models.DateTimeField(ugettext_lazy('Emission done')\
			        ,null=True,editable=False )

#    def emitted(self):
#	    return self.emission_done != None 
#    emitted.short_description = 'Trasmesso'

    def was_scheduled_today(self):
        return self.emission_date.date() == datetime.date.today()
    
    was_scheduled_today.short_description = ugettext_lazy('Programmed for today?')

    def file(self):
        return self.playlist.playlist
    file.short_description = ugettext_lazy('Linked Playlist')

    def __unicode__(self):
        return unicode(self.playlist)

class PeriodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    playlist = models.ForeignKey(Playlist,verbose_name=\
					ugettext_lazy('refer to playlist:'))

    shuffle = models.BooleanField(ugettext_lazy("Shuffle Playlist on start"),default=True,\
                                      help_text=ugettext_lazy("Every time the playlist will be scheduled it's order will be randomly changed"))
    length = models.FloatField(ugettext_lazy("Max time length (seconds)"),default=None,null=True,blank=True,\
                                   help_text=ugettext_lazy("If this time is set the playlist will be truncated"))
    start_date = models.DateField(ugettext_lazy('Programmed start date'),null=True,blank=True,\
                                      help_text=ugettext_lazy("The playlist will be scheduled starting from this date"))
    end_date = models.DateField(ugettext_lazy('Programmed end date'),null=True,blank=True,\
                                      help_text=ugettext_lazy("The playlist will be scheduled ending this date"))
    time = models.TimeField(ugettext_lazy('Programmed time'),null=True,blank=True,\
                                             help_text=ugettext_lazy("This is the time when the playlist will be on air"))
    giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Programmed days'),null=True,blank=True,\
                                        help_text=ugettext_lazy("The playlist will be scheduled those weekdays"))
    emission_done = models.DateTimeField(ugettext_lazy('Emission done')\
			        ,null=True,editable=False )

#    def emitted(self):
#	    return self.emission_done != None 
#    emitted.short_description = 'Trasmesso'

    def file(self):
        return self.playlist.playlist
    file.short_description = ugettext_lazy('Linked Playlist')

    def __unicode__(self):
        return unicode(self.playlist)

