from django.db import models
from django.utils.translation import ugettext_lazy
import datetime
import calendar
from autoradio.autoradio_config import *

def giorno_giorno():
	giorni=[]
	for giorno in (calendar.day_name):
		giorno=giorno.decode('utf-8')
		giorni.append(( giorno, giorno))
	return giorni
#	yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True)
        def __unicode__(self):
            return self.name

class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True\
					   ,default='playlist',editable=False)

	active = models.BooleanField(ugettext_lazy("Activate Playlist"),default=True)
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed start time'))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "\
		+self.emission_starttime.isoformat()+" "\
		+self.emission_endtime.isoformat()


class Playlist(models.Model):
    playlist = models.CharField(ugettext_lazy('Playlist name'),max_length=200)
    file = models.FileField(ugettext_lazy('File'),upload_to='playlist')
    rec_date = models.DateTimeField(ugettext_lazy('Generation date'))
    active = models.BooleanField(ugettext_lazy("Active"),default=True)

 
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

    shuffle = models.BooleanField(ugettext_lazy("Shuffle Playlist on start"),default=True)
    length = models.FloatField(ugettext_lazy("Max time length (seconds)"),default=None,null=True,blank=True)
    emission_date = models.DateTimeField(ugettext_lazy('Programmed date'))

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

    shuffle = models.BooleanField(ugettext_lazy("Shuffle Playlist on start"),default=True)
    length = models.FloatField(ugettext_lazy("Max time length (seconds)"),default=None,null=True,blank=True)
    start_date = models.DateField(ugettext_lazy('Programmed start date'),null=True,blank=True)
    end_date = models.DateField(ugettext_lazy('Programmed end date'),null=True,blank=True)
    time = models.TimeField(ugettext_lazy('Programmed time'),null=True,blank=True)
    giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Programmed days'),null=True,blank=True)
    
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

