from models import Giorno, Configure, Playlist, Schedule, PeriodicSchedule
from django.contrib import admin


class ScheduleInline(admin.StackedInline):
#class ScheduleInline(admin.TabularInline):

    model = Schedule
    extra=2


class PeriodicScheduleInline(admin.TabularInline):
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
        (None, {'fields': ('playlist','file')}),
        ('Date information', {'fields': ('rec_date','active',)}),
        )
    list_display = ('playlist','rec_date','was_recorded_today','active')
    search_fields = ['playlist','file']
    date_hierarchy = 'rec_date'
    list_filter = ['rec_date','active']
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

admin.site.register(Schedule, ScheduleAdmin)



class PeriodicScheduleAdmin(admin.ModelAdmin):
    list_display = ('file', 'shuffle','length','start_date','end_date','time'\
				,'emission_done')
    list_filter = ['start_date','end_date','time','giorni','emission_done']
    search_fields = ['playlist','giorni']
    date_hierarchy = 'start_date'


admin.site.register(PeriodicSchedule, PeriodicScheduleAdmin)
