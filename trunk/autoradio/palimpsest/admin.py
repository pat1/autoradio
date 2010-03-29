from models import Giorno, Configure, ProgramType, Program, Schedule, PeriodicSchedule
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

    list_display = ('sezione','radiostation','channel','active',\
                        'emission_starttime'\
                        ,'emission_endtime')

admin.site.register(Configure, ConfigureAdmin)

class ProgramTypeAdmin(admin.ModelAdmin):

    list_display = ('code','type','subtype','description')

admin.site.register(ProgramType, ProgramTypeAdmin)


class ProgramAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('program','length','type','production')}),
        )
    list_display = ('program','active')
    search_fields = ['program',]
    list_filter = ['active']
    inlines = [
        ScheduleInline,PeriodicScheduleInline,
        ]


admin.site.register(Program, ProgramAdmin)


class ScheduleAdmin(admin.ModelAdmin):
        list_display = ('emission_date'\
				,'was_scheduled_today')
        list_filter = ['emission_date']
        search_fields = ['program','emission_date']
        date_hierarchy = 'emission_date'

admin.site.register(Schedule, ScheduleAdmin)



class PeriodicScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','time')
    list_filter = ['start_date','end_date','time','giorni']
    search_fields = ['playlist','giorni']
    date_hierarchy = 'start_date'


admin.site.register(PeriodicSchedule, PeriodicScheduleAdmin)
