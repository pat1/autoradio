
from .models import Giorno, Configure, Jingle
from django.contrib import admin
from django import forms
from django.utils.translation import gettext_lazy
import autoradio.settings
import magic
import autoradio.mime

ma = magic.open(magic.MAGIC_MIME_TYPE)
ma.load()

class MyJingleAdminForm(forms.ModelForm):
    """
    Check file if it is a known media file.
    """
    class Meta(object):
        model = Jingle
        fields = '__all__'

    def clean_file(self):

        import mutagen, os

        file = self.cleaned_data.get('file',False)
        if file:
            #if file._size > 40*1024*1024:
            #    raise forms.ValidationError("Audio file too large ( > 4mb )")
            try:
                type = file.content_type in webmime_audio
            except:
                return file

            if not type:
                raise forms.ValidationError(gettext_lazy("Content-Type is not audio/mpeg or audio/flac or video/ogg"))

            if not os.path.splitext(file.name)[1] in websuffix_audio:
                raise forms.ValidationError(gettext_lazy("Doesn't have proper extension: .mp3, .wav, .ogg, .oga, .flac"))


            try:
                mime = ma.file(file.temporary_file_path())
                audio = mime in mymime_audio
            except:
                audio=False
                    
            if not audio:
                raise forms.ValidationError(gettext_lazy("Not a valid audio file"))

            if autoradio.settings.require_tags_in_enclosure:
                #Check file if it is a known media file. The check is based on mutagen file test.
                try:
                    audio = not (mutagen.File(file.temporary_file_path()) is None)
                except:
                    audio = False

                if not audio:
                    raise forms.ValidationError(gettext_lazy("Not a valid audio file: probably no tags present"))

            return file

        else:
            raise forms.ValidationError(gettext_lazy("Couldn't read uploaded file"))


class GiornoAdmin(admin.ModelAdmin):
	search_fields = ['name']

admin.site.register(Giorno, GiornoAdmin)


class ConfigureAdmin(admin.ModelAdmin):
		list_display = ('sezione','active','emission_freq',)

admin.site.register(Configure, ConfigureAdmin)


class JingleAdmin(admin.ModelAdmin):
    fieldsets = (
	(None, {'fields': ('active','jingle','file','rec_date')}),
	('Emission information', {'fields': ('start_date','end_date','start_time','end_time','giorni','priorita')}),
    )
    list_display = ('active','jingle','file','start_date','end_date','emission_done')
    list_display_links = ('jingle',)
    list_editable = ('active','start_date','end_date')
    list_filter = ['active','rec_date','giorni']
    search_fields = ['jingle','file']
    date_hierarchy = 'rec_date'

    form = MyJingleAdminForm

admin.site.register(Jingle, JingleAdmin)

