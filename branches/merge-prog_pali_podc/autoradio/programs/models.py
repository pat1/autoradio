
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy

import datetime
import calendar

class ParentCategory(models.Model):
    """Parent Category model."""
    PARENT_CHOICES = (
        ('Arts', 'Arts'),
        ('Business', 'Business'),
        ('Comedy', 'Comedy'),
        ('Education', 'Education'),
        ('Games & Hobbies', 'Games & Hobbies'),
        ('Government & Organizations', 'Government & Organizations'),
        ('Health', 'Health'),
        ('Kids & Family', 'Kids & Family'),
        ('Music', 'Music'),
        ('News & Politics', 'News & Politics'),
        ('Religion & Spirituality', 'Religion & Spirituality'),
        ('Science & Medicine', 'Science & Medicine'),
        ('Society & Culture', 'Society & Culture'),
        ('Sports & Recreation', 'Sports & Recreation'),
        ('Technology', 'Technology'),
        ('TV & Film', 'TV & Film'),
    )
    name = models.CharField(max_length=50, choices=PARENT_CHOICES, help_text='After saving this parent category, please map it to one or more Child Categories below.')
    slug = models.SlugField(blank=True, unique=False, help_text='A <a href="http://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield">slug</a> is a URL-friendly nickname. For example, a slug for "Games & Hobbies" is "games-hobbies".')

    class Meta:
        ordering = ['slug']
        verbose_name = 'category (iTunes parent)'
        verbose_name_plural = 'categories (iTunes parent)'

    def __unicode__(self):
        return u'%s' % (self.name)


class ChildCategory(models.Model):
    """Child Category model."""
    CHILD_CHOICES = (
        ('Arts', (
                ('Design', 'Design'),
                ('Fashion & Beauty', 'Fashion & Beauty'),
                ('Food', 'Food'),
                ('Literature', 'Literature'),
                ('Performing Arts', 'Performing Arts'),
                ('Visual Arts', 'Visual Arts'),
            )
        ),
        ('Business', (
                ('Business News', 'Business News'),
                ('Careers', 'Careers'),
                ('Investing', 'Investing'),
                ('Management & Marketing', 'Management & Marketing'),

                ('Shopping', 'Shopping'),
            )
        ),
        ('Education', (
                ('Education Technology', 'Education Technology'),
                ('Higher Education', 'Higher Education'),
                ('K-12', 'K-12'),
                ('Language Courses', 'Language Courses'),
                ('Training', 'Training'),
            )
        ),
        ('Games & Hobbies', (
                ('Automotive', 'Automotive'),
                ('Aviation', 'Aviation'),
                ('Hobbies', 'Hobbies'),
                ('Other Games', 'Other Games'),
                ('Video Games', 'Video Games'),
            )
        ),
        ('Government & Organizations', (
                ('Local', 'Local'),
                ('National', 'National'),
                ('Non-Profit', 'Non-Profit'),
                ('Regional', 'Regional'),
            )
        ),
        ('Health', (
                ('Alternative Health', 'Alternative Health'),
                ('Fitness & Nutrition', 'Fitness & Nutrition'),
                ('Self-Help', 'Self-Help'),
                ('Sexuality', 'Sexuality'),
            )
        ),
        ('Religion & Spirituality', (
                ('Buddhism', 'Buddhism'),
                ('Christianity', 'Christianity'),
                ('Hinduism', 'Hinduism'),
                ('Islam', 'Islam'),
                ('Judaism', 'Judaism'),
                ('Other', 'Other'),
                ('Spirituality', 'Spirituality'),
            )
        ),
        ('Science & Medicine', (
                ('Medicine', 'Medicine'),
                ('Natural Sciences', 'Natural Sciences'),
                ('Social Sciences', 'Social Sciences'),
            )
        ),
        ('Society & Culture', (
                ('History', 'History'),
                ('Personal Journals', 'Personal Journals'),
                ('Philosophy', 'Philosophy'),
                ('Places & Travel', 'Places & Travel'),
            )
        ),
        ('Sports & Recreation', (
                ('Amateur', 'Amateur'),
                ('College & High School', 'College & High School'),
                ('Outdoor', 'Outdoor'),
                ('Professional', 'Professional'),
            )
        ),
        ('Technology', (
                ('Gadgets', 'Gadgets'),
                ('Tech News', 'Tech News'),
                ('Podcasting', 'Podcasting'),
                ('Software How-To', 'Software How-To'),
            )
        ),
    )
    parent = models.ForeignKey(ParentCategory, related_name='child_category_parents')
    name = models.CharField(max_length=50, blank=True, choices=CHILD_CHOICES, help_text='Please choose a child category that corresponds to its respective parent category (e.g., "Design" is a child category of "Arts").<br />If no such child category exists for a parent category (e.g., Comedy, Kids & Family, Music, News & Politics, or TV & Film), simply leave this blank and save.')
    slug = models.SlugField(blank=True, unique=False, help_text='A <a href="http://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield">slug</a> is a URL-friendly nickname. For exmaple, a slug for "Fashion & Beauty" is "fashion-beauty".')

    class Meta:
        ordering = ['parent', 'slug']
        verbose_name = 'category (iTunes child)'
        verbose_name_plural = 'categories (iTunes child)'

    def __unicode__(self):
        if self.name!='':
            return u'%s > %s' % (self.parent, self.name)
        else:
            return u'%s' % (self.parent)



def giorno_giorno():
	for giorno in calendar.day_name:
		yield giorno, giorno
#	yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True)
        def __unicode__(self):
            return self.name

class Configure(models.Model):


	sezione = models.CharField(max_length=50,unique=True\
					   ,default='show',editable=False)
	active = models.BooleanField(ugettext_lazy("Active show"),default=True)
        emission_starttime = models.TimeField(ugettext_lazy('Programmed start time'))
        emission_endtime = models.TimeField(ugettext_lazy('Programmed end time'))

        radiostation = models.CharField(max_length=50,unique=True\
					   ,default='Radio',editable=True)
        channel = models.CharField(max_length=80,unique=True\
					   ,default='103',editable=True)

        mezzo = models.CharField(max_length=50,unique=True\
					   ,default='analogico terrestre',editable=True)

        type = models.CharField(max_length=50,unique=True\
					   ,default='radiofonica',editable=True)



        def __unicode__(self):
            return self.sezione+" "+self.active.__str__()+" "\
		+self.emission_starttime.isoformat()+" "\
		+self.emission_endtime.isoformat()


class ProgramType(models.Model):

    code = models.CharField(ugettext_lazy("Code"),max_length=4,default=None,null=False,blank=False,unique=True)
    type = models.CharField(ugettext_lazy("Type"),max_length=200,default=None,null=False,blank=False)
    subtype = models.CharField(ugettext_lazy("SubType"),max_length=254,default=None,null=False,blank=False)
    description = models.TextField(ugettext_lazy("Description"),default=None,null=True,blank=True)

    def __unicode__(self):
        return self.type+"/"+self.subtype

def Production():
	for production in (ugettext_lazy("autoproduction"),ugettext_lazy("eteroproduction")):
		yield production, production


class Show(models.Model):
    """Show model."""

    title = models.CharField(max_length=255)
    active = models.BooleanField(ugettext_lazy("Active"),default=True)
    slug = models.SlugField(unique=True, help_text='Auto-generated from Title.')
    length = models.FloatField(ugettext_lazy("Time length (seconds)"),default=None,null=True,blank=True)
    type = models.ForeignKey(ProgramType, verbose_name=	ugettext_lazy('Program Type'))

    production = models.CharField(ugettext_lazy("Production"),max_length=30,choices=Production(),default=None,null=True,blank=True)
    COPYRIGHT_CHOICES = (
	    ('Public domain', 'Public domain'),
	    ('Creative Commons: Attribution (by)', 'Creative Commons: Attribution (by)'),
	    ('Creative Commons: Attribution-Share Alike (by-sa)', 'Creative Commons: Attribution-Share Alike (by-sa)'),
	    ('Creative Commons: Attribution-No Derivatives (by-nd)', 'Creative Commons: Attribution-No Derivatives (by-nd)'),
	    ('Creative Commons: Attribution-Non-Commercial (by-nc)', 'Creative Commons: Attribution-Non-Commercial (by-nc)'),
	    ('Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)', 'Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)'),
	    ('Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)', 'Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)'),
	    ('All rights reserved', 'All rights reserved'),
	    )
    EXPLICIT_CHOICES = (
	    ('Yes', 'Yes'),
	    ('No', 'No'),
	    ('Clean', 'Clean'),
	    )
    # RSS 2.0
    organization = models.CharField(max_length=255, help_text='Name of the organization, company or Web site producing the podcast.')
    link = models.URLField(help_text='URL of either the main website or the podcast section of the main website.')
    description = models.TextField(help_text='Describe subject matter, media format, episode schedule and other relevant information while incorporating keywords.')
    language = models.CharField(max_length=5, default='en-us', help_text='Default is American English. See <a href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes">ISO 639-1</a> and <a href="http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1</a> for more language codes.', blank=True)
    copyright = models.CharField(max_length=255, default='All rights reserved', choices=COPYRIGHT_CHOICES, help_text='See <a href="http://creativecommons.org/about/license/">Creative Commons licenses</a> for more information.')
    copyright_url = models.URLField('Copyright URL', blank=True, help_text='A URL pointing to additional copyright information. Consider a <a href="http://creativecommons.org/licenses/">Creative Commons license URL</a>.')
    author = models.ManyToManyField(User, related_name='display_authors', help_text='Remember to save the user\'s name and e-mail address in the <a href="../../../auth/user/">User application</a>.<br />')
    webmaster = models.ForeignKey(User, related_name='display_webmaster', blank=True, null=True, help_text='Remember to save the user\'s name and e-mail address in the <a href="../../../auth/user/">User application</a>.')
    category_show = models.CharField('Category', max_length=255, blank=True, help_text='Limited to one user-specified category for the sake of sanity.')
    domain = models.URLField(blank=True, help_text='A URL that identifies a categorization taxonomy.')
    ttl = models.PositiveIntegerField('TTL', help_text='"Time to Live," the number of minutes a channel can be cached before refreshing.', blank=True, null=True)
    image = models.ImageField(upload_to='podcasts/shows/img/', help_text='An attractive, original square JPEG (.jpg) or PNG (.png) image of 600x600 pixels. Image will be scaled down to 50x50 pixels at smallest in iTunes.', blank=True)
    feedburner = models.URLField('FeedBurner URL', help_text='Fill this out after saving this show and at least one episode. URL should look like "http://feeds.feedburner.com/TitleOfShow". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.', blank=True)
    # iTunes
    subtitle = models.CharField(max_length=255, help_text='Looks best if only a few words, like a tagline.', blank=True)
    summary = models.TextField(help_text='Allows 4,000 characters. Description will be used if summary is blank.', blank=True)
    category = models.ManyToManyField(ChildCategory, related_name='show_categories', help_text='If selecting a category group with no child category (e.g., Comedy, Kids & Family, Music, News & Politics or TV & Film), save that parent category with a blank <a href="../../childcategory/">child category</a>.<br />Selecting multiple category groups makes the podcast more likely to be found by users.<br />', blank=True)
    explicit = models.CharField(max_length=255, default='No', choices=EXPLICIT_CHOICES, help_text='"Clean" will put the clean iTunes graphic by it.', blank=True)
    block = models.BooleanField(default=False, help_text='Check to block this show from iTunes. <br />Show will remain blocked until unchecked.')
    redirect = models.URLField(help_text='The show\'s new URL feed if changing the URL of the current show feed. Must continue old feed for at least two weeks and write a 301 redirect for old feed.', blank=True)
    keywords = models.CharField(max_length=255, help_text='A comma-demlimited list of up to 12 words for iTunes searches. Perhaps include misspellings of the title.', blank=True)
    itunes = models.URLField('iTunes Store URL', help_text='Fill this out after saving this show and at least one episode. URL should look like "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.', blank=True)


    class Meta:
        ordering = ['organization', 'slug']

    def __unicode__(self):
        return u'%s' % (self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('podcast_episodes', (), { 'slug': self.slug })


class Episode(models.Model):

	title = models.CharField(max_length=255)
        active = models.BooleanField(ugettext_lazy("Active"),default=True)
	rec_date = models.DateTimeField(ugettext_lazy('Recording date'))
	def was_recorded_today(self):
		return self.rec_date.date() == datetime.date.today()
	was_recorded_today.short_description = ugettext_lazy('Recorded today?')

	show = models.ForeignKey(Show)

	def __unicode__(self):
		return self.title


class Enclosure(models.Model):
    """Enclosure model."""
    MIME_CHOICES = (
        ('audio/ogg', '.ogg (audio)'),
        ('audio/mpeg', '.mp3 (audio)'),
        ('audio/x-m4a', '.m4a (audio)'),
        ('video/mp4', '.mp4 (audio or video)'),
        ('video/x-m4v', '.m4v (video)'),
        ('video/quicktime', '.mov (video)'),
        ('application/pdf', '.pdf (document)'),
        ('image/jpeg', '.jpg, .jpeg, .jpe (image)')
    )
    MEDIUM_CHOICES = (
        ('Audio', 'Audio'),
        ('Video', 'Video'),
        ('Document', 'Document'),
        ('Image', 'Image'),
        ('Executable', 'Executable'),
    )
    EXPRESSION_CHOICES = (
        ('Sample', 'Sample'),
        ('Full', 'Full'),
        ('Nonstop', 'Non-stop'),
    )
    ALGO_CHOICES = (
        ('MD5', 'MD5'),
        ('SHA-1', 'SHA-1'),
    )

    FRAME_CHOICES = (( '29.97','29.97'),)
    BITRATE_CHOICES = (
        ( "8","8"),
        ("11.025","11.025"),
        ("16","16"),
        ("22.050","22.050"),
        ("32","32"),
        ("44.1","44.1"),
        ("48","48"),
        ("96","96")
        )
    SAMPLE_CHOICHES = (
        ("24","24"),
        ("48","48"),
        ("64","64"),
        ("96","96"),
        ("128","128"),
        ("160","160"),
        ("196","196"),
        ("320","320")
        )
    CHANNEL_CHOICES = (
        ("2","2"),
        ("1","1")
        )

    title = models.CharField(max_length=255, blank=True, help_text='Title is generally only useful with multiple enclosures.')
    file = models.FileField(upload_to='podcasts/episodes/files/', help_text='Either upload or use the "Player" text box below. If uploading, file must be less than or equal to 30 MB for a Google video sitemap.',blank=False, null=False)
    mime = models.CharField('Format', max_length=255, choices=MIME_CHOICES, blank=True)
    medium = models.CharField(max_length=255, blank=True, choices=MEDIUM_CHOICES)
    expression = models.CharField(max_length=25, choices=EXPRESSION_CHOICES, blank=True)
    frame = models.CharField('Frame rate', max_length=5, help_text='Measured in frames per second (fps), often 29.97.',choices=FRAME_CHOICES,blank=True)
    bitrate = models.CharField('Bit rate', max_length=5, blank=True, help_text='Measured in kilobits per second (kbps), often 128 or 192.',choices=BITRATE_CHOICES)
    sample = models.CharField('Sample rate', max_length=5, blank=True, help_text='Measured in kilohertz (kHz), often 44.1.',choices=SAMPLE_CHOICHES)
    channel = models.CharField(max_length=5, blank=True, help_text='Number of channels; 2 for stereo, 1 for mono.',choices=CHANNEL_CHOICES)
    algo = models.CharField('Hash algorithm', max_length=50, blank=True, choices=ALGO_CHOICES)
    hash = models.CharField(max_length=255, blank=True, help_text='MD-5 or SHA-1 file hash.')
    player = models.URLField(help_text='URL of the player console that plays the media. Could be your own .swf, but most likely a YouTube URL, such as <a href="http://www.youtube.com/v/UZCfK8pVztw">http://www.youtube.com/v/UZCfK8pVztw</a> (not the permalink, which looks like <a href="http://www.youtube.com/watch?v=UZCfK8pVztw">http://www.youtube.com/watch?v=UZCfK8pVztw</a>).', blank=True)
    embed = models.BooleanField(help_text='Check to allow Google to embed your external player in search results on <a href="http://video.google.com">Google Video</a>.', blank=True)
    width = models.PositiveIntegerField(blank=True, null=True, help_text='Width of the browser window in <br />which the URL should be opened. <br />YouTube\'s default is 425.')
    height = models.PositiveIntegerField(blank=True, null=True, help_text='Height of the browser window in <br />which the URL should be opened. <br />YouTube\'s default is 344.')
    episode = models.ForeignKey(Episode, help_text='Include any number of media files; for example, perhaps include an iPhone-optimized, AppleTV-optimized and Flash Video set of video files. Note that the iTunes feed only accepts the first file. More uploading is available after clicking "Save and continue editing."')

    class Meta:
        ordering = ['mime', 'file']

    def __unicode__(self):
        return u'%s' % (self.file)


class Schedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

	episode = models.ForeignKey(Episode, \
		  verbose_name=ugettext_lazy('Linked episode:'))

	emission_date = models.DateTimeField(ugettext_lazy('programmed date'))


	#    def emitted(self):
	#	    return self.emission_done != None 
	#    emitted.short_description = 'Trasmesso'

	def was_scheduled_today(self):
		return self.emission_date.date() == datetime.date.today()
    
	was_scheduled_today.short_description = ugettext_lazy('Scheduled for today?')

	def refepisode(self):
		return self.episode.title
	refepisode.short_description = ugettext_lazy('Linked episode:')

	def __unicode__(self):
	        return unicode(self.episode.title)



class ScheduleDone(models.Model):

	schedule = models.ForeignKey(Schedule, \
		  verbose_name=ugettext_lazy('Linked schedule:'))

	enclosure = models.ForeignKey(Enclosure, \
		  verbose_name=ugettext_lazy('Linked enclosure:'))

	emission_done = models.DateTimeField(ugettext_lazy('emission done')\
						     ,null=True,editable=False )

	def __unicode__(self):
	        return unicode(self.emission_done)



class PeriodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    show = models.ForeignKey(Show,verbose_name=\
					ugettext_lazy('refer to show:'))

    start_date = models.DateField(ugettext_lazy('Programmed start date'),null=True,blank=True)
    end_date = models.DateField(ugettext_lazy('Programmed end date'),null=True,blank=True)
    time = models.TimeField(ugettext_lazy('Programmed time'),null=True,blank=True)
    giorni = models.ManyToManyField(Giorno,verbose_name=ugettext_lazy('Programmed days'),null=True,blank=True)
    

    def __unicode__(self):
        return unicode(self.show)

class AperiodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    show = models.ForeignKey(Show, verbose_name=\
					ugettext_lazy('refer to Show:'))

    emission_date = models.DateTimeField(ugettext_lazy('Programmed date'))

    def was_scheduled_today(self):
        return self.emission_date.date() == datetime.date.today()
    
    was_scheduled_today.short_description = ugettext_lazy('Programmed for today?')

    def __unicode__(self):
        return unicode(self.show)


