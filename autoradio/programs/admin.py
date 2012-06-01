from django.contrib import admin
from models import Giorno, Configure, ProgramType, Show, Schedule, \
    PeriodicSchedule,AperiodicSchedule,Episode,Enclosure,ScheduleDone
from autoradio.programs.models import ParentCategory, ChildCategory, MediaCategory
from django import forms
from django.utils.translation import ugettext_lazy
import autoradio.settings

import magic

ma = magic.open(magic.MAGIC_MIME_TYPE)
ma.load()

mymime_audio=("application/ogg","audio/mpeg", "audio/mp4", "audio/x-flac", "audio/x-wav") 
mymime_ogg=("application/ogg",)

webmime_audio = ("audio/mpeg","audio/flac","video/ogg")
websuffix_audio = (".mp3",".wav",".ogg",".oga",".flac",".Mp3",".Wav",".Ogg",".Oga",".Flac",".MP3",".WAV",".OGG",".OGA",".FLAC" )

webmime_ogg = ("video/ogg","audio/oga")
websuffix_ogg = (".ogg",".oga",".Ogg",".Oga",".OGG")

class MyEnclosureInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        import mutagen, os

        # get forms that actually have valid data
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1

                    file = form.cleaned_data.get('file',False)
                    if file:

                        if autoradio.settings.permit_no_playable_files:

                            try:
                                type = file.content_type in webmime_audio
                            except:
                                #here when the file is not uploaded (modify for example)
                                return file

                            if not type:
                                raise forms.ValidationError(ugettext_lazy("Content-Type is not audio/mpeg or audio/flac or video/ogg"))

                            if not os.path.splitext(file.name)[1] in websuffix_audio:
                                raise forms.ValidationError(ugettext_lazy("Doesn't have proper extension: .mp3, .wav, .ogg, .oga, .flac"))

                            try:
                                mime = ma.file(file.temporary_file_path())
                                audio = mime in mymime_audio
                            except:
                                audio=False

                            if not audio:
                                raise forms.ValidationError(ugettext_lazy("Not a valid audio file"))

                            if autoradio.settings.require_tags_in_enclosure:
                                #Check file if it is a known media file. The check is based on mutagen file test.
                                try:
                                    audio = not mutagen.File(file.temporary_file_path()) is None
                                except:
                                    audio = False

                                if not audio:
                                    raise forms.ValidationError(ugettext_lazy("Not a valid audio file: probably no tags present"))

                        else:

                            try:
                                type = file.content_type in webmime_ogg
                            except:
                                #here when the file is not uploaded (modify for example)
                                return file

                            if not type:
                                raise forms.ValidationError(ugettext_lazy("Content-Type is not audio/oga or video/ogg"))

                            if not os.path.splitext(file.name)[1] in websuffix_ogg:
                                raise forms.ValidationError(ugettext_lazy("Doesn't have proper extension: .ogg, .oga"))

                            try:
                                mime = ma.file(file.temporary_file_path())
                                audio = mime in mymime_ogg
                            except:
                                audio=False

                            if not audio:
                                raise forms.ValidationError(ugettext_lazy("Not a valid ogg/oga vorbis audio file"))

                            if autoradio.settings.require_tags_in_enclosure:
                                #Check file if it is a known media file. The check is based on mutagen file test.
                                try:
                                    mut=mutagen.File(file.temporary_file_path())
                                    audio = not mut is None
                                    sample_rate=mut.info.sample_rate
                                except:
                                    audio = False
                                    sample_rate=0

                                if not audio:
                                    raise forms.ValidationError(ugettext_lazy("Not a valid ogg/oga vorbis audio file: probably no tags present"))

                                if not sample_rate == 44100:
                                    raise forms.ValidationError(ugettext_lazy("Sample rate is Not 44100Hz: cannot use it in podcasting web interface"))
            
                        return file

                    else:
                        raise forms.ValidationError(ugettext_lazy("Couldn't read uploaded file"))

            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass

        if count < 1:
            raise forms.ValidationError(ugettext_lazy('You must have at least one Enclosure'))



class MyEnclosureAdminForm(forms.ModelForm):
    """
    Check file if it is a known media file.
    """
    class Meta:
        model = Enclosure

    def clean_file(self):

	    import mutagen, os

	    file = self.cleaned_data.get('file',False)
	    if file:

                if autoradio.settings.permit_no_playable_files:

                    try:
                        type = file.content_type in ["audio/mpeg","audio/flac","video/ogg"]
                    except:
                        return file

                    if not type:
                        raise forms.ValidationError(ugettext_lazy("Content-Type is not audio/mpeg or audio/flac or video/ogg"))
    
                    if not os.path.splitext(file.name)[1] in [".mp3",".wav",".ogg",".oga",".flac",
							      ".Mp3",".Wav",".Ogg",".Oga",".Flac",
							      ".MP3",".WAV",".OGG",".OGA",".FLAC" ]:
                        raise forms.ValidationError(ugettext_lazy("Doesn't have proper extension: .mp3, .wav, .ogg, .oga, .flac"))
                    #Check file if it is a known media file. The check is based on mutagen file test.
                    try:
                        audio = not mutagen.File(file.temporary_file_path()) is None
                    except:
                        audio = False

                    if not audio:
                        raise forms.ValidationError(ugettext_lazy("Not a valid audio file"))
                    return file

                else:

                    try:
                        type = file.content_type in ["video/ogg","audio/oga"]
                    except:
                        return file

                    if not type:
                        raise forms.ValidationError(ugettext_lazy("Content-Type is not audio/oga or video/ogg"))

                    if not os.path.splitext(file.name)[1] in [".ogg",".oga",".Ogg",".Oga",".OGG"]:
                        raise forms.ValidationError(ugettext_lazy("Doesn't have proper extension: .ogg, .oga"))
                    #Check file if it is a known media file. The check is based on mutagen file test.
                    try:
                        mut=mutagen.File(file.temporary_file_path())
                        audio = not mut is None
                        sample_rate=mut.info.sample_rate

                    except:
                        audio = False
                        sample_rate=0

                    if not audio:
                        raise forms.ValidationError(ugettext_lazy("Not a valid audio file"))

                    if not sample_rate == 44100:
                        raise forms.ValidationError(ugettext_lazy("Sample rate is Not 44100Hz: cannot use it in podcasting web interface"))
            
                    return file
                
	    else:
		    raise forms.ValidationError(ugettext_lazy("Couldn't read uploaded file"))


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

    formset = MyEnclosureInlineFormset


class ScheduleInline(admin.StackedInline):
#class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra=2
    max_num=10

class PeriodicScheduleInline(admin.StackedInline):
    model = PeriodicSchedule
    extra=2

class AperiodicScheduleInline(admin.StackedInline):
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

    list_display = ('episode','title',)
    list_filter = ['medium','mime','bitrate']
    search_fields = ['title','file']

    fieldsets = (
        (None, {
                'fields': ('episode','title', 'file',)
                }),
        ('Podcast options', {
                'classes': ('collapse',),
                'fields': ('mime', 'medium','expression','frame','bitrate',\
                               'sample','channel','algo','hash','player','embed','width','height')
                }),
        )

    form = MyEnclosureAdminForm

admin.site.register(Enclosure, EnclosureAdmin)
