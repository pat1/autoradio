from models import Giorno, Configure, Fascia, Spot
from django.contrib import admin


class GiornoAdmin(admin.ModelAdmin):
	search_fields = ['name']


admin.site.register(Giorno, GiornoAdmin)

class ConfigureAdmin(admin.ModelAdmin):
	list_display = ('sezione','active','emission_starttime','emission_endtime')

admin.site.register(Configure, ConfigureAdmin)

class FasciaAdmin(admin.ModelAdmin):
	search_fields = ['name','spots']
	list_display = ('name','emission_time','emission_done','active','spots')

admin.site.register(Fascia, FasciaAdmin)


class SpotAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('spot','file','rec_date')}),
		('Emission information', {'fields': \
		  ('start_date','end_date','giorni','fasce','priorita','prologo','epilogo')}),
		)
	#	    list_display = ('spot', 'rec_date', 'was_recorded_today','giorni','fasce','priorita')
	list_filter = ['start_date','end_date','rec_date','fasce','giorni',"prologo","epilogo"]

	# rec_date sarebbe standard, ma per eliminare cose vecchie meglio usare end_date
	#date_hierarchy = 'rec_date'
	date_hierarchy = 'end_date'

	search_fields = ['spot','giorni__name','fasce__name',]
	list_display = ('spot','file','rec_date','priorita')

admin.site.register(Spot, SpotAdmin)

