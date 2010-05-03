from django.contrib import admin
from models import Giorno, Configure, ProgramType, Show, Schedule, \
    PeriodicSchedule,AperiodicSchedule,Episode,Enclosure,ScheduleDone


class EnclosureInline(admin.StackedInline):
    model = Enclosure
    extra=1
    max_num=10
    fieldsets = (
        (None, {
                'fields': ('title', 'file',)
                }),
        ('Podcast options', {
                'classes': ('collapse',),
                'fields': ('mime', 'medium','expression','frame','bitrate',\
                               'sample','channel','algo','hash','player','embed','width','height')
                }),
        )



class ScheduleInline(admin.StackedInline):
#class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra=2
    max_num=10

class PeriodicScheduleInline(admin.TabularInline):
    model = PeriodicSchedule
    extra=2

class AperiodicScheduleInline(admin.TabularInline):
    model = AperiodicSchedule
    extra=2

class EpisodeInline(admin.TabularInline):
    model = Episode
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



class ShowAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('title','length','type','production')}),
        )
    list_display = ('title',)
    #list_filter = ['end_date',]
    search_fields = ['title',]

    inlines = [
        PeriodicScheduleInline,AperiodicScheduleInline,EpisodeInline
        ]


admin.site.register(Show, ShowAdmin)


class EpisodeAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('show','title','rec_date')}),
        )
    list_display = ('title',)
    #list_filter = ['end_date',]
    search_fields = ['title',]

    inlines = [
        ScheduleInline,EnclosureInline
        ]

admin.site.register(Episode, EpisodeAdmin)




class ScheduleAdmin(admin.ModelAdmin):

    list_display = ('episode', 'emission_date'\
                        ,'was_scheduled_today')
    list_filter = ['emission_date']
    search_fields = ['episode','emission_date']
    date_hierarchy = 'emission_date'

admin.site.register(Schedule, ScheduleAdmin)


class PeriodicScheduleAdmin(admin.ModelAdmin):
    list_display = ('start_date','end_date','time')
    list_filter = ['start_date','end_date','time','giorni']
    search_fields = ['playlist','giorni']
    date_hierarchy = 'start_date'

admin.site.register(PeriodicSchedule, PeriodicScheduleAdmin)

class AperiodicScheduleAdmin(admin.ModelAdmin):
    list_display = ('emission_date','show')
    search_fields = ['show']
    date_hierarchy = 'emission_date'

admin.site.register(AperiodicSchedule, AperiodicScheduleAdmin)

class ScheduleDoneAdmin(admin.ModelAdmin):
    list_display = ('emission_done','schedule','enclosure')
    search_fields = ['enclosure']
    date_hierarchy = 'emission_done'

admin.site.register(ScheduleDone, ScheduleDoneAdmin)


class EnclosureAdmin(admin.ModelAdmin):

    list_display = ('title',)
    list_filter = ['medium','mime','bitrate']
    search_fields = ['title','file']

    fieldsets = (
        (None, {
                'fields': ('title', 'file',)
                }),
        ('Podcast options', {
                'classes': ('collapse',),
                'fields': ('mime', 'medium','expression','frame','bitrate',\
                               'sample','channel','algo','hash','player','embed','width','height')
                }),
        )


admin.site.register(Enclosure, EnclosureAdmin)
