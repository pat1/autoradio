
from autoradio.palimpsest.models import Program as PalimpsestProgram
from django.db import models
from django.utils.translation import ugettext_lazy

import datetime

class Configure(models.Model):
	sezione = models.CharField(max_length=50,unique=True\
					   ,default='program',editable=False)
	active = models.BooleanField(ugettext_lazy("Active programs"),default=True)
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed end time'))


        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "\
		+self.emission_starttime.isoformat()+" "\
		+self.emission_endtime.isoformat()


class Program(models.Model):
	program = models.CharField(ugettext_lazy('Program name'),max_length=200)
	file = models.FileField('file',upload_to='programs')
	rec_date = models.DateTimeField(ugettext_lazy('Recording date'))
	active = models.BooleanField(ugettext_lazy("Active"),default=True)
	palimpsest = models.ForeignKey(PalimpsestProgram,related_name="PalimpsestProgram")
	
	def was_recorded_today(self):
		return self.rec_date.date() == datetime.date.today()

	was_recorded_today.short_description = ugettext_lazy('Recorded today?')

	def __unicode__(self):
		#return self.program+" "+self.rec_date.isoformat()+" "+self.active.__str__()
		return self.program

class Schedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

	program = models.ForeignKey(Program, \
		  verbose_name=ugettext_lazy('Linked program:'))

	emission_date = models.DateTimeField(ugettext_lazy('programmed date'))
	emission_done = models.DateTimeField(ugettext_lazy('emission done')\
						     ,null=True,editable=False )

	#    def emitted(self):
	#	    return self.emission_done != None 
	#    emitted.short_description = 'Trasmesso'

	def was_scheduled_today(self):
		return self.emission_date.date() == datetime.date.today()
    
	was_scheduled_today.short_description = ugettext_lazy('Scheduled for today?')

	def file(self):
		return self.program.program
	file.short_description = ugettext_lazy('Linked program:')

	def __unicode__(self):
	        return unicode(self.program)

