from jingles.models import Giorno, Configure, Jingle
from django.contrib import admin


class GiornoAdmin(admin.ModelAdmin):
	search_fields = ['name']

admin.site.register(Giorno, GiornoAdmin)


class ConfigureAdmin(admin.ModelAdmin):
		list_display = ('sezione','active','emission_freq',)

admin.site.register(Configure, ConfigureAdmin)


class JingleAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('jingle','file','rec_date','active')}),
		('Emission information', {'fields': ('start_date','end_date','start_time','end_time','giorni','priorita')}),
		)
	list_display = ('jingle','file','rec_date','emission_done','active')
	list_filter = ['active','start_date','end_date','start_time','end_time','rec_date','giorni']
	date_hierarchy = 'rec_date'
	search_fields = ['jingle','file']

admin.site.register(Jingle, JingleAdmin)

