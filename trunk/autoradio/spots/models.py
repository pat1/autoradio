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

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True,
                                help_text=ugettext_lazy("weekday name"))
        def __unicode__(self):
            return self.name

        class Admin:
		search_fields = ['name']

## class Giorno(models.Model):


## 	#DAY_CHOICES = (
## 	#        ('1', 'Lunedi'),
## 	#        ('2', 'Martedi'),
## 	#        ('3', 'Mercoledi'),
## 	#        ('4', 'Giovedi'),
## 	#        ('5', 'Venerdi'),
## 	#        ('6', 'Sabato'),
## 	#        ('7', 'Domenica'),
## 	#	)
	

## 	DAY_CHOICES = (
## 	        ( 'Lunedi','Lunedi'),
## 	        ( 'Martedi','Martedi'),
## 	        ( 'Mercoledi','Mercoledi'),
## 	        ( 'Giovedi','Giovedi'),
## 	        ( 'Venerdi','Venerdi'),
## 	        ( 'Sabato','Sabato'),
## 	        ( 'Domenica','Domenica'),
## 		)
	
##         name = models.CharField(max_length=20,choices=DAY_CHOICES,unique=True)

## 	#name = models.CharField(max_length=20)
	
##         def __unicode__(self):
##             return self.name

##         class Admin:
## 		search_fields = ['name']


class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True,default='spot',editable=False)
	active = models.BooleanField(ugettext_lazy("Activate Spot"),default=True,\
                 help_text=ugettext_lazy("activate/deactivate the intere spot class"))
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'),null=True,blank=True,\
                 help_text=ugettext_lazy("The start time from wich the spot will be active"))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed end time'),null=True,blank=True,\
                 help_text=ugettext_lazy("The end time the spot will be active"))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "+self.emission_starttime.isoformat()\
		+" "+self.emission_endtime.isoformat()

        class Admin:
		list_display = ('sezione','active','emission_starttime','emission_endtime')


class Fascia(models.Model):
        name = models.CharField(max_length=50,unique=True,\
                       help_text=ugettext_lazy("The name of commercial break"))
        emission_time = models.TimeField(unique=True,\
                       help_text=ugettext_lazy("This is the date and time when the commercial break will be on air"))
	active = models.BooleanField(ugettext_lazy("Active"),default=True,\
                       help_text=ugettext_lazy("Activate the commercial break for emission"))
	emission_done = models.DateTimeField(ugettext_lazy('Emission done'),null=True,editable=False )


	def spots(self):
#		print   self.spot_set.filter(prologo__exact=True).order_by('priorita').append(\
#			self.spot_set.exclude(prologo__exact=True).exclude(epilogo__exact=True).order_by('priorita')).append(\
#			self.spot_set.filter(epilogo__exact=True).order_by('priorita'))

		return self.spot_set.all().order_by('prologo').order_by('priorita').order_by('epilogo')

#		filter(prologo__exact=True)
#		return di
#		di={}
#		di["bb"]="ciccia"
#		di["cc"]="cacca"
#		return di
#		sps=""
#		for sp in di.iterkeys():
#			sps=sps+di[sp]
#		return sps
#		    .append(\
#			self.spot_set.exclude(prologo__exact=True).exclude(epilogo__exact=True).order_by('priorita')).append(\
#			self.spot_set.filter(epilogo__exact=True).order_by('priorita'))

        def __unicode__(self):
            return self.name+" "+self.emission_time.isoformat()

        class Admin:
		search_fields = ['name','emission_time','emission_done','active','spots']
		list_display = ('name','emission_time','emission_done','active','spots')


class Spot(models.Model):
	
	spot = models.CharField(ugettext_lazy("Spot Name"),max_length=80,unique=True,\
                       help_text=ugettext_lazy("The name of the spot"))
	file = DeletingFileField(ugettext_lazy('File'),upload_to='spots',max_length=255,\
                       help_text=ugettext_lazy("The spot file to upload"))
	rec_date = models.DateTimeField(ugettext_lazy('Record date'),\
                       help_text=ugettext_lazy("When the spot was done (for reference only)"))
	active = models.BooleanField(ugettext_lazy("Active"),default=True,\
                       help_text=ugettext_lazy("Activate the spot for emission"))
	start_date = models.DateTimeField(ugettext_lazy('Programmed starting date'),null=True,blank=True,\
                       help_text=ugettext_lazy("The spot will be scheduled starting from this date"))
	end_date = models.DateTimeField(ugettext_lazy('Programmed ending date'),null=True,blank=True,\
                       help_text=ugettext_lazy("The spot will be scheduled ending this date"))

	# giorni = models.PositiveIntegerField( choices=DAY_CHOICES)
#	giorni = models.ForeignKey(Giorno,verbose_name='Giorni programmati',editable=False)
	giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Programmed days'),null=True,blank=True,\
                       help_text=ugettext_lazy("The spot will be scheduled those weekdays"))
	fasce = models.ManyToManyField(Fascia,null=True,blank=True,\
                       help_text=ugettext_lazy("The spot will be included in those commercial break"))

	priorita = models.IntegerField(ugettext_lazy("Priority"),default=50,\
                       help_text=ugettext_lazy("The order of the spots in commercial breaks will be ordered by this numer"))
	prologo =  models.BooleanField(ugettext_lazy("Prologue"),default=False,\
                       help_text=ugettext_lazy("This spot will be the firt in commercial breaks to introduce the others"))
	epilogo =  models.BooleanField(ugettext_lazy("Epilogue"),default=False,\
                       help_text=ugettext_lazy("This spot will be the last in commercial breaks to leave-taking"))
	
	def was_recorded_today(self):
		return self.rec_date.date() == datetime.date.today()
    
	was_recorded_today.short_description = ugettext_lazy('Recorded today?')

	def __unicode__(self):
		return self.spot

	class Admin:
		fields = (
			(None, {'fields': ('spot','file','rec_date')}),
			('Emission information', {'fields': \
			  ('start_date','end_date','giorni','fasce','priorita','prologo','epilogo')}),
			)
		#	    list_display = ('spot', 'rec_date', 'was_recorded_today','giorni','fasce','priorita')
		list_filter = ['start_date','end_date','fasce','giorni',"prologo","epilogo"]
		date_hierarchy = 'rec_date'
		search_fields = ['spot','giorni','fascie']
		list_display = ('spot','file','rec_date','priorita')


	#class Meta:
	#	unique_together = ("prologo", "epilogo","fasce")
		
