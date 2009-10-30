from django.db import models
from django.utils.translation import ugettext_lazy
import datetime
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

class Configure(models.Model):
        sezione = models.CharField(max_length=50,unique=True\
					   ,default='palimpsest',editable=False)
        radiostation = models.CharField(max_length=50,unique=True\
					   ,default='Radio',editable=True)
        channel = models.CharField(max_length=50,unique=True\
					   ,default='103',editable=True)

	active = models.BooleanField(ugettext_lazy("Activate palimpsest"),default=True)
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed start time'))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "\
		+self.emission_starttime.isoformat()+" "\
		+self.emission_endtime.isoformat()




class ProgramType(models.Model):

    code = models.CharField(ugettext_lazy("Code"),max_length=4,default=None,null=False,blank=False,unique=True)
    type = models.CharField(ugettext_lazy("Type"),max_length=200,default=None,null=False,blank=False)
    subtype = models.CharField(ugettext_lazy("SubType"),max_length=254,default=None,null=False,blank=False)
    description = models.TextField(ugettext_lazy("Description"),default=None,null=True,blank=True)

    def __unicode__(self):
        return self.type+"/"+self.subtype


class Program(models.Model):
    program = models.CharField(ugettext_lazy('Program name'),max_length=200)
    active = models.BooleanField(ugettext_lazy("Active"),default=True)
    length = models.FloatField(ugettext_lazy("Time length (seconds)"),default=None,null=True,blank=True)
    type = models.ForeignKey(ProgramType, verbose_name=	ugettext_lazy('Program Type'))
 
    def __unicode__(self):
        return self.program



class Schedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    program = models.ForeignKey(Program, verbose_name=\
					ugettext_lazy('refer to program:'))

    emission_date = models.DateTimeField(ugettext_lazy('Programmed date'))

    def was_scheduled_today(self):
        return self.emission_date.date() == datetime.date.today()
    
    was_scheduled_today.short_description = ugettext_lazy('Programmed for today?')

    def __unicode__(self):
        return unicode(self.program)

class PeriodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    program = models.ForeignKey(Program,verbose_name=\
					ugettext_lazy('refer to program:'))

    start_date = models.DateField(ugettext_lazy('Programmed start time'),null=True,blank=True)
    end_date = models.DateField(ugettext_lazy('Programmed end time'),null=True,blank=True)
    time = models.TimeField(ugettext_lazy('Programmed time'),null=True,blank=True)
    giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Programmed days'),null=True,blank=True)
    

    def __unicode__(self):
        return unicode(self.program)

