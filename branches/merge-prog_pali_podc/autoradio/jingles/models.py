from django.db import models
from django.utils.translation import ugettext_lazy
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
	file = DeletingFileField(ugettext_lazy('File'),upload_to='jingles',max_length=255)
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

