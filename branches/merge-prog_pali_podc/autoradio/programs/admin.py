from django.contrib import admin
from models import Configure, Program, Schedule



class ScheduleInline(admin.StackedInline):
#class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra=2
    max_num=10

class ConfigureAdmin(admin.ModelAdmin):

    list_display = ('sezione','active',\
                        'emission_starttime'\
                        ,'emission_endtime')

admin.site.register(Configure, ConfigureAdmin)

class ProgramAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('program','file')}),
        ('Date information', {'fields': ('rec_date','active','palimpsest')}),
        )
    list_display = ('program', 'rec_date', 'was_recorded_today','active','palimpsest')
    #list_filter = ['end_date']
    list_filter = ['rec_date']
    search_fields = ['program','file']
    date_hierarchy = 'rec_date'

    inlines = [
        ScheduleInline,
        ]


admin.site.register(Program, ProgramAdmin)

class ScheduleAdmin(admin.ModelAdmin):

    list_display = ('file', 'emission_date','emission_done'\
                        ,'was_scheduled_today')
    list_filter = ['emission_date','emission_done']
    search_fields = ['program','emission_date']
    date_hierarchy = 'emission_date'

admin.site.register(Schedule, ScheduleAdmin)

