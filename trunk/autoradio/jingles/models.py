from django.db import models
from django.utils.translation import ugettext_lazy
import calendar
from autoradio.autoradio_config import *

def giorno_giorno():
	for giorno in calendar.day_name:
		yield giorno, giorno
#	yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True)
        def __unicode__(self):
            return self.name

        class Admin:
		search_fields = ['name']


class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True,default='jingle',editable=False)
	active = models.BooleanField(ugettext_lazy("Activate Jingle"),default=True)
        emission_freq = models.TimeField(ugettext_lazy('Frequency'))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "+self.emission_freq.isoformat()

        class Admin:
		list_display = ('sezione','active','emission_freq',)


class Jingle(models.Model):
	
	jingle = models.CharField(ugettext_lazy("Jingle name"),max_length=80,unique=True)
	file = models.FileField(ugettext_lazy('File'),upload_to='jingles')
	rec_date = models.DateTimeField(ugettext_lazy('Recording date'))
	active = models.BooleanField(ugettext_lazy("Active"),default=True)

	start_date = models.DateField(ugettext_lazy('Emission starting date'),null=True,blank=True)
	end_date = models.DateField(ugettext_lazy('Emission end date'),null=True,blank=True)

	start_time = models.TimeField(ugettext_lazy('Emission start time'),null=True,blank=True)
	end_time = models.TimeField(ugettext_lazy('Emission end time'),null=True,blank=True)

	giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Scheduled days'),null=True,blank=True)

	priorita = models.IntegerField(ugettext_lazy("Priority"),default=50)

	emission_done = models.DateTimeField(ugettext_lazy('emission done'),null=True,editable=False )

	
	def was_recorded_today(self):
		return self.rec_date.date() == datetime.date.today()
    
	was_recorded_today.short_description = ugettext_lazy('Recorded today?')

	def __unicode__(self):
		return self.jingle

	class Admin:
		fields = (
			(None, {'fields': ('jingle','file','rec_date','active')}),
			('Emission information', {'fields': ('start_date','end_date','start_time','end_time','giorni','priorita')}),
			)
		list_display = ('jingle','file','rec_date','emission_done')
		list_filter = ['start_date','end_date','start_time','end_time','giorni']
		date_hierarchy = 'rec_date'
		search_fields = ['jingle']

	#class Meta:
	#	unique_together = ("prologo", "epilogo","fasce")

