from django.contrib import admin
from models import Giorno, Configure, ProgramType, Show, Schedule, \
    PeriodicSchedule,AperiodicSchedule,Episode,Enclosure,ScheduleDone
from autoradio.programs.models import ParentCategory, ChildCategory, MediaCategory


class CategoryInline(admin.StackedInline):
    model = ChildCategory
    extra = 3

class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CategoryInline,]

class ChildCategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name')

class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(ParentCategory, ParentCategoryAdmin)
admin.site.register(ChildCategory, ChildCategoryAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)

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

class EpisodeInline(admin.StackedInline):
    model = Episode
    extra=1

    # not supported
    #inline=(ScheduleInline,EnclosureInline,)

    fieldsets = (
        (None, {
            'fields': ('show', 'author', 'title_type', 'title', 'slug', 'description_type', 'description')
        }),
        ('podcast options', {
            'classes': ('collapse',),
            'fields': ('captions', 'category', 'domain', 'frequency', 'priority', 'status')
        }),
        ('iTunes options', {
            'classes': ('collapse',),
            'fields': ('subtitle', 'summary', ('minutes', 'seconds'), 'keywords', ('explicit', 'block'))
        }),
        ('Media RSS options', {
            'classes': ('collapse',),
            'fields': ('role', 'media_category', ('standard', 'rating'), 'image', 'text', ('deny', 'restriction'))
        }),
        ('Dublin Core options', {
            'classes': ('collapse',),
            'fields': (('start', 'end'), 'scheme', 'name')
        }),
        ('Google Media options', {
            'classes': ('collapse',),
            'fields': ('preview', ('preview_start_mins', 'preview_start_secs'), ('preview_end_mins', 'preview_end_secs'), 'host')
        }),
    )

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

    prepopulated_fields = {'slug': ("title",)}

    fieldsets = (
        (None, {'fields': ('title','slug','length','type','production',\
                               'organization','link','description','author')}),

        ('Podcast options', {
                'classes': ('collapse',),
                'fields': ('language','copyright','copyright_url',\
                               'webmaster','category_show',\
                               'domain','ttl','image','feedburner')}),
        ('iTunes options', {
                'classes': ('collapse',),
                'fields': ('subtitle','summary','category','explicit',\
                               'block','redirect','keywords','itunes')})
        )


    list_display = ('title',)
    #list_filter = ['end_date',]
    search_fields = ['title',]

#    is better without EpisodeInline and start from Episode 
#    inlines = [
#        EpisodeInline,PeriodicScheduleInline,AperiodicScheduleInline
#        ]

    inlines = [
        PeriodicScheduleInline,AperiodicScheduleInline
        ]


admin.site.register(Show, ShowAdmin)





class EpisodeAdmin(admin.ModelAdmin):
    inlines = [
        ScheduleInline,EnclosureInline
        ]
    prepopulated_fields = {'slug': ("title",)}
    search_fields = ['title',]
    list_display = ('title', 'update', 'show')
    list_filter = ('show', 'update')

    radio_fields = {'title_type': admin.HORIZONTAL, 'description_type': admin.HORIZONTAL, 'status': admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': ('show', 'author', 'title_type', 'title', 'slug', 'description_type', 'description')
        }),
        ('podcast options', {
            'classes': ('collapse',),
            'fields': ('captions', 'category', 'domain', 'frequency', 'priority', 'status')
        }),
        ('iTunes options', {
            'classes': ('collapse',),
            'fields': ('subtitle', 'summary', ('minutes', 'seconds'), 'keywords', ('explicit', 'block'))
        }),
        ('Media RSS options', {
            'classes': ('collapse',),
            'fields': ('role', 'media_category', ('standard', 'rating'), 'image', 'text', ('deny', 'restriction'))
        }),
        ('Dublin Core options', {
            'classes': ('collapse',),
            'fields': (('start', 'end'), 'scheme', 'name')
        }),
        ('Google Media options', {
            'classes': ('collapse',),
            'fields': ('preview', ('preview_start_mins', 'preview_start_secs'), ('preview_end_mins', 'preview_end_secs'), 'host')
        }),
    )



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
