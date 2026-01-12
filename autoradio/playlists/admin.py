from .models import Giorno, Configure, Playlist, Schedule, PeriodicSchedule
from django.contrib import admin


class ScheduleInline(admin.StackedInline):
#class ScheduleInline(admin.TabularInline):

    model = Schedule
    extra=2


class PeriodicScheduleInline(admin.StackedInline):
    model = PeriodicSchedule
    extra=2


class GiornoAdmin(admin.ModelAdmin):
	search_fields = ['name']


admin.site.register(Giorno, GiornoAdmin)

class ConfigureAdmin(admin.ModelAdmin):

    list_display = ('sezione','active',\
                        'emission_starttime'\
                        ,'emission_endtime')

admin.site.register(Configure, ConfigureAdmin)


class PlaylistAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('active','playlist','file')}),
        ('Date information', {'fields': ('rec_date',)}),
        )
    list_display = ('active','playlist','rec_date','was_recorded_today')
    search_fields = ['playlist','file']
    date_hierarchy = 'rec_date'
    list_filter = ['active','rec_date']
    list_editable = ('active',)
    list_display_links = ('playlist',)
    inlines = [
        ScheduleInline,PeriodicScheduleInline,
        ]


admin.site.register(Playlist, PlaylistAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('file', 'shuffle','length','emission_date','emission_done'\
				,'was_scheduled_today')
    list_filter = ['emission_date','emission_done']
    search_fields = ['playlist','emission_date']
    date_hierarchy = 'emission_date'
    list_editable = ('shuffle','length')

admin.site.register(Schedule, ScheduleAdmin)



class PeriodicScheduleAdmin(admin.ModelAdmin):
    list_display = ('file', 'shuffle','length','start_date','end_date','time'\
				,'emission_done')
    list_filter = ['start_date','end_date','time','giorni','emission_done']
    search_fields = ['playlist','giorni__name']
    date_hierarchy = 'start_date'
    list_editable = ('shuffle','length')


admin.site.register(PeriodicSchedule, PeriodicScheduleAdmin)
