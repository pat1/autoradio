from django.db import models
from django.utils.translation import gettext_lazy
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
       	#giorno=giorno.decode('utf-8')
       	giorni.append(( giorno, giorno))
       return giorni
#       yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True,\
               help_text=gettext_lazy("weekday name"))

        def __str__(self):
            return self.name

        class Admin(object):
       	     search_fields = ['name']


class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True,default='jingle',editable=False)
        active = models.BooleanField(gettext_lazy("Activate Jingle"),default=True,
                  help_text=gettext_lazy("activate/deactivate the intere jingle class"))
        emission_freq = models.TimeField(gettext_lazy('Frequency'))


        def __str__(self):
            return self.sezione+" "+self.active.__str__()+" "+self.emission_freq.isoformat()

        class Admin(object):
       	    list_display = ('sezione','active','emission_freq',)


class Jingle(models.Model):
       
       jingle = models.CharField(gettext_lazy("Jingle name"),max_length=80,unique=True)
       file = DeletingFileField(gettext_lazy('File'),upload_to='jingles',max_length=255,\
                 help_text=gettext_lazy("The jingle file to upload"))
       rec_date = models.DateTimeField(gettext_lazy('Recording date'),\
                 help_text=gettext_lazy("When the jingle was done (for reference only)"))
       active = models.BooleanField(gettext_lazy("Active"),default=True,\
                 help_text=gettext_lazy("Activate the jingle for emission"))
       start_date = models.DateField(gettext_lazy('Emission starting date'),null=True,blank=True,\
                 help_text=gettext_lazy("The jingle will be scheduled starting from this date"))
       end_date = models.DateField(gettext_lazy('Emission end date'),null=True,blank=True,\
                 help_text=gettext_lazy("The jingle will be scheduled ending this date"))
       start_time = models.TimeField(gettext_lazy('Emission start time'),null=True,blank=True,\
                 help_text=gettext_lazy("The jingle will be scheduled starting from this date"))
       end_time = models.TimeField(gettext_lazy('Emission end time'),null=True,blank=True,\
                 help_text=gettext_lazy("The jingle will be scheduled ending this date"))
       giorni = models.ManyToManyField(Giorno,verbose_name=gettext_lazy('Scheduled days'),blank=True,\
                 help_text=gettext_lazy("The jingle will be scheduled those weekdays"))
       priorita = models.IntegerField(gettext_lazy("Priority"),default=50,\
                 help_text=gettext_lazy("When there are more jingle that wait for emission from the same time, the emission will be ordered by this numer"))
       emission_done = models.DateTimeField(gettext_lazy('emission done'),null=True,editable=False )

       
       def was_recorded_today(self):
       	return self.rec_date.date() == datetime.date.today()
    
       was_recorded_today.short_description = gettext_lazy('Recorded today?')

       def __str__(self):
       	return self.jingle

#       class Admin(object):
#
#        fields = (
#       		(None, {'fields': ('jingle','file','rec_date','active')}),
#       		('Emission information', {'fields': ('start_date','end_date','start_time','end_time','giorni','priorita')}),
#       		)
#       	list_display = ('jingle','file','rec_date','emission_done')
#       	list_filter = ['start_date','end_date','start_time','end_time','giorni']
#       	date_hierarchy = 'rec_date'
#       	search_fields = ['jingle']

       #class Meta:
       #	unique_together = ("prologo", "epilogo","fasce")

