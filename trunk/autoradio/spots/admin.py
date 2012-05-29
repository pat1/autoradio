from models import Giorno, Configure, Fascia, Spot
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy

class MySpotAdminForm(forms.ModelForm):
    """
    Check file if it is a known media file.
    """
    class Meta:
        model = Spot

    def clean_file(self):

	    import mutagen, os

	    file = self.cleaned_data.get('file',False)
	    if file:
		    #if file._size > 40*1024*1024:
			#    raise forms.ValidationError("Audio file too large ( > 4mb )")
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
                    audio = not (mutagen.File(file.temporary_file_path()) is None)
                except:
                    audio = False

                if not audio:
                    raise forms.ValidationError(ugettext_lazy("Not a valid audio file"))
                return file
	    else:
                raise forms.ValidationError(ugettext_lazy("Couldn't read uploaded file"))


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

	form = MySpotAdminForm


admin.site.register(Spot, SpotAdmin)

