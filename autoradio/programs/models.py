
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from autoradio.programs.managers import EpisodeManager
import datetime
import calendar
from django.db.models import Q

from  django import VERSION as djversion

if ((djversion[0] == 1 and djversion[1] >= 3) or 
    djversion[0] > 1):

    from django.db import models
    from django.db.models import signals

    class DeletingFileField(models.FileField):
        """
        FileField subclass that deletes the refernced file when the model object
        itself is deleted.
        
        WARNING: Be careful using this class - it can cause data loss! This class
        makes at attempt to see if the file's referenced elsewhere, but it can get
        it wrong in any number of cases.
        """
        def contribute_to_class(self, cls, name):
            super(DeletingFileField, self).contribute_to_class(cls, name)
            signals.post_delete.connect(self.delete_file, sender=cls)
        
        def delete_file(self, instance, sender, **kwargs):
            file = getattr(instance, self.attname)
            # If no other object of this type references the file,
            # and it's not the default value for future objects,
            # delete it from the backend.
            
            if file and file.name != self.default and \
                    not sender._default_manager.filter(**{self.name: file.name}):
                file.delete(save=False)
            elif file:
                # Otherwise, just close the file, so it doesn't tie up resources.
                file.close()

else:
    DeletingFileField=models.FileField

class MediaCategory(models.Model):
    """Category model for Media RSS"""
    MEDIA_CATEGORY_CHOICES = (
        ('Action & Adventure', 'Action & Adventure'),
        ('Ads & Promotional', 'Ads & Promotional'),
        ('Anime & Animation', 'Anime & Animation'),
        ('Art & Experimental', 'Art & Experimental'),
        ('Business', 'Business'),
        ('Children & Family', 'Children & Family'),
        ('Comedy', 'Comedy'),
        ('Dance', 'Dance'),
        ('Documentary', 'Documentary'),
        ('Drama', 'Drama'),
        ('Educational', 'Educational'),
        ('Faith & Spirituality', 'Faith & Spirituality'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Foreign', 'Foreign'),
        ('Gaming', 'Gaming'),
        ('Gay & Lesbian', 'Gay & Lesbian'),
        ('Home Video', 'Home Video'),
        ('Horror', 'Horror'),
        ('Independent', 'Independent'),
        ('Mature & Adult', 'Mature & Adult'),
        ('Movie (feature)', 'Movie (feature)'),
        ('Movie (short)', 'Movie (short)'),
        ('Movie Trailer', 'Movie Trailer'),
        ('Music & Musical', 'Music & Musical'),
        ('Nature', 'Nature'),
        ('News', 'News'),
        ('Political', 'Political'),
        ('Religious', 'Religious'),
        ('Romance', 'Romance'),
        ('Independent', 'Independent'),
        ('Sci-Fi & Fantasy', 'Sci-Fi & Fantasy'),
        ('Science & Technology', 'Science & Technology'),
        ('Special Interest', 'Special Interest'),
        ('Sports', 'Sports'),
        ('Stock Footage', 'Stock Footage'),
        ('Thriller', 'Thriller'),
        ('Travel', 'Travel'),
        ('TV Show', 'TV Show'),
        ('Western', 'Western'),
    )
    name = models.CharField(max_length=50, choices=MEDIA_CATEGORY_CHOICES)
    slug = models.SlugField(blank=True, unique=False, help_text=gettext_lazy('A <a href="http://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield">slug</a> is a URL-friendly nickname. For example, a slug for "Games & Hobbies" is "games-hobbies".'))

    class Meta(object):
        ordering = ['slug']
        verbose_name = 'category (Media RSS)'
        verbose_name_plural = 'categories (Media RSS)'

    def __str__(self):
        return u'%s' % (self.name)


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
    name = models.CharField(max_length=50, choices=PARENT_CHOICES, help_text=gettext_lazy('After saving this parent category, please map it to one or more Child Categories below.'))
    slug = models.SlugField(blank=True, unique=False, help_text=gettext_lazy('A <a href="http://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield">slug</a> is a URL-friendly nickname. For example, a slug for "Games & Hobbies" is "games-hobbies".'))

    class Meta(object):
        ordering = ['slug']
        verbose_name = 'category (iTunes parent)'
        verbose_name_plural = 'categories (iTunes parent)'

    def __str__(self):
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
    parent = models.ForeignKey(ParentCategory, related_name='child_category_parents', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, choices=CHILD_CHOICES, help_text=gettext_lazy('Please choose a child category that corresponds to its respective parent category (e.g., "Design" is a child category of "Arts").<br />If no such child category exists for a parent category (e.g., Comedy, Kids & Family, Music, News & Politics, or TV & Film), simply leave this blank and save.'))
    slug = models.SlugField(blank=True, unique=False, help_text=gettext_lazy('A <a href="http://docs.djangoproject.com/en/dev/ref/models/fields/#slugfield">slug</a> is a URL-friendly nickname. For exmaple, a slug for "Fashion & Beauty" is "fashion-beauty".'))

    class Meta(object):
        ordering = ['parent', 'slug']
        verbose_name = 'category (iTunes child)'
        verbose_name_plural = 'categories (iTunes child)'

    def __str__(self):
        if self.name!='':
            return u'%s > %s' % (self.parent, self.name)
        else:
            return u'%s' % (self.parent)


def giorno_giorno():
       giorni=[]
       for giorno in (calendar.day_name):
              #giorno=giorno.decode('utf-8')
              giorni.append(( giorno, giorno))
       return giorni
#       yield 'Tutti','Tutti'

class Giorno(models.Model):

        name = models.CharField(max_length=20,choices=giorno_giorno(),unique=True,\
                                help_text=gettext_lazy("weekday name"))
        def __str__(self):
            return self.name

class Configure(models.Model):


       sezione = models.CharField(max_length=50,unique=True\
              			   ,default='show',editable=False)
       active = models.BooleanField(gettext_lazy("Active show"),default=True,\
                                         help_text=gettext_lazy("activate/deactivate the intere program class"))
       emission_starttime = models.TimeField(gettext_lazy('Programmed start time'),null=True,blank=True,\
                                                  help_text=gettext_lazy("The start time from wich the programs will be active"))
       emission_endtime = models.TimeField(gettext_lazy('Programmed end time'),null=True,blank=True,\
                                            help_text=gettext_lazy("The end time the programs will be active"))


       radiostation = models.CharField(max_length=50,unique=True, default='Radio',editable=True,\
                       help_text=gettext_lazy("The station name for the print of programs book"))
       channel = models.CharField(max_length=80,unique=True, default='103', editable=True,\
                       help_text=gettext_lazy("The station channel for the print of programs book"))
       mezzo = models.CharField(max_length=50,unique=True, default='analogico terrestre', editable=True,\
                       help_text=gettext_lazy("The station kind of emission for the print of programs book"))
       type = models.CharField(max_length=50,unique=True, default='radiofonica', editable=True,\
                       help_text=gettext_lazy("The station type for the print of programs book"))

       def __str__(self):

            if self.emission_starttime is None:
                emission_starttime = "-"
            else:
                emission_starttime = self.emission_starttime.isoformat()

            if self.emission_endtime is None:
                emission_endtime = "-"
            else:
                emission_endtime = self.emission_endtime.isoformat()

            return self.sezione+" "+self.active.__str__()+" "\
              +emission_starttime+" "\
              +emission_endtime


class ProgramType(models.Model):

    code = models.CharField(gettext_lazy("Code"),max_length=4,default=None,null=False,blank=False,unique=True)
    type = models.CharField(gettext_lazy("Type"),max_length=200,default=None,null=False,blank=False)
    subtype = models.CharField(gettext_lazy("SubType"),max_length=254,default=None,null=False,blank=False)
    description = models.TextField(gettext_lazy("Description"),default=None,null=True,blank=True)

    def __str__(self):
        return self.type+"/"+self.subtype

def Production():
       for production in (gettext_lazy("autoproduction"),gettext_lazy("eteroproduction")):
              yield production, production


class Show(models.Model):
    """Show model."""

    title = models.CharField(max_length=255,help_text=gettext_lazy("show title"))
    active = models.BooleanField(gettext_lazy("Active"),default=True,help_text=gettext_lazy("Activate the show for emission"))
    slug = models.SlugField(unique=True, help_text=gettext_lazy('Auto-generated from Title.'))
    length = models.FloatField(gettext_lazy("Time length (seconds)"),default=None,null=True,blank=True, help_text=gettext_lazy('Time lenght how you want to see it in the palimpsest'))
    type = models.ForeignKey(ProgramType, verbose_name=       gettext_lazy('Program Type'), help_text=gettext_lazy('The categorization that follow the italian law (you have to use it to produce the programs book') , on_delete=models.CASCADE)

    production = models.CharField(gettext_lazy("Production"),max_length=30,choices=Production(),default=None,null=True,blank=True, help_text=gettext_lazy('The type of production'))
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
    organization = models.CharField(max_length=255, help_text=gettext_lazy('Name of the organization, company or Web site producing the podcast.'))
    link = models.URLField(help_text=gettext_lazy('URL of either the main website or the podcast section of the main website.'))
    description = models.CharField(max_length=80,help_text=gettext_lazy('Describe subject matter, media format, episode schedule and other relevant information while incorporating keywords.'),default=None,null=True,blank=True)
    language = models.CharField(max_length=5, default='en-us', help_text=gettext_lazy('Default is American English. See <a href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes">ISO 639-1</a> and <a href="http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1</a> for more language codes.'), blank=True)
    copyright = models.CharField(max_length=255, default='All rights reserved', choices=COPYRIGHT_CHOICES, help_text=gettext_lazy('See <a href="http://creativecommons.org/about/license/">Creative Commons licenses</a> for more information.'))
    copyright_url = models.URLField('Copyright URL', blank=True, help_text=gettext_lazy('A URL pointing to additional copyright information. Consider a <a href="http://creativecommons.org/licenses/">Creative Commons license URL</a>.'))
    author = models.ManyToManyField(User, related_name='display_authors', help_text=gettext_lazy('Remember to save the user\'s name and e-mail address in the <a href="../../../auth/user/">User application</a>.<br />'))
    webmaster = models.ForeignKey(User, related_name='display_webmaster', blank=True, null=True, help_text=gettext_lazy('Remember to save the user\'s name and e-mail address in the <a href="../../../auth/user/">User application</a>.') , on_delete=models.CASCADE)
    category_show = models.CharField('Category', max_length=255, blank=True, help_text=gettext_lazy('Limited to one user-specified category for the sake of sanity.'))
    domain = models.URLField(blank=True, help_text=gettext_lazy('A URL that identifies a categorization taxonomy.'))
    ttl = models.PositiveIntegerField('TTL', help_text=gettext_lazy('"Time to Live," the number of minutes a channel can be cached before refreshing.'), blank=True, null=True)
    image = models.ImageField(upload_to='podcasts/shows/img/', help_text=gettext_lazy('An attractive, original square JPEG (.jpg) or PNG (.png) image of 600x600 pixels. Image will be scaled down to 50x50 pixels at smallest in iTunes.'), blank=True)
    feedburner = models.URLField('FeedBurner URL', help_text=gettext_lazy('Fill this out after saving this show and at least one episode. URL should look like "http://feeds.feedburner.com/TitleOfShow". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.'), blank=True)
    # iTunes
    subtitle = models.CharField(max_length=255, help_text=gettext_lazy('Looks best if only a few words, like a tagline.'), blank=True)
    summary = models.TextField(help_text=gettext_lazy('Allows 4,000 characters. Description will be used if summary is blank.'), blank=True)
    category = models.ManyToManyField(ChildCategory, related_name='show_categories', help_text=gettext_lazy('If selecting a category group with no child category (e.g., Comedy, Kids & Family, Music, News & Politics or TV & Film), save that parent category with a blank <a href="../../childcategory/">child category</a>.<br />Selecting multiple category groups makes the podcast more likely to be found by users.<br />'), blank=True)
    explicit = models.CharField(max_length=255, default='No', choices=EXPLICIT_CHOICES, help_text=gettext_lazy('"Clean" will put the clean iTunes graphic by it.'), blank=True)
    block = models.BooleanField(default=False, help_text=gettext_lazy('Check to block this show from iTunes. <br />Show will remain blocked until unchecked.'))
    redirect = models.URLField(help_text=gettext_lazy('The show\'s new URL feed if changing the URL of the current show feed. Must continue old feed for at least two weeks and write a 301 redirect for old feed.'), blank=True)
    keywords = models.CharField(max_length=255, help_text=gettext_lazy('A comma-demlimited list of up to 12 words for iTunes searches. Perhaps include misspellings of the title.'), blank=True)
    itunes = models.URLField('iTunes Store URL', help_text=gettext_lazy('Fill this out after saving this show and at least one episode. URL should look like "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.'), blank=True)


    class Meta(object):
        ordering = ['title']

    def __str__(self):
        return u'%s' % (self.title)

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('podcast_episodes', (), { 'slug': self.slug })

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('podcast_episodes', args=[str(self.slug)])


class Episode(models.Model):

    STATUS_CHOICES = (
        (1, 'Draft'),
        (2, 'Public'),
        (3, 'Private'),
    )
    SECONDS_CHOICES = tuple(('%02d' % x, str(x)) for x in range(60))
    EXPLICIT_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
        ('Clean', 'Clean'),
    )
    TYPE_CHOICES = (
        ('Plain', 'Plain text'),
        ('HTML', 'HTML'),
    )
    ROLE_CHOICES = (
        ('Actor', 'Actor'),
        ('Adaptor', 'Adaptor'),
        ('Anchor person', 'Anchor person'),
        ('Animal Trainer', 'Animal Trainer'),
        ('Animator', 'Animator'),
        ('Announcer', 'Announcer'),
        ('Armourer', 'Armourer'),
        ('Art Director', 'Art Director'),
        ('Artist/Performer', 'Artist/Performer'),
        ('Assistant Camera', 'Assistant Camera'),
        ('Assistant Chief Lighting Technician', 'Assistant Chief Lighting Technician'),
        ('Assistant Director', 'Assistant Director'),
        ('Assistant Producer', 'Assistant Producer'),
        ('Assistant Visual Editor', 'Assistant Visual Editor'),
        ('Author', 'Author'),
        ('Broadcast Assistant', 'Broadcast Assistant'),
        ('Broadcast Journalist', 'Broadcast Journalist'),
        ('Camera Operator', 'Camera Operator'),
        ('Carpenter', 'Carpenter'),
        ('Casting', 'Casting'),
        ('Causeur', 'Causeur'),
        ('Chief Lighting Technician', 'Chief Lighting Technician'),
        ('Choir', 'Choir'),
        ('Choreographer', 'Choreographer'),
        ('Clapper Loader', 'Clapper Loader'),
        ('Commentary or Commentator', 'Commentary or Commentator'),
        ('Commissioning Broadcaster', 'Commissioning Broadcaster'),
        ('Composer', 'Composer'),
        ('Computer programmer', 'Computer programmer'),
        ('Conductor', 'Conductor'),
        ('Consultant', 'Consultant'),
        ('Continuity Checker', 'Continuity Checker'),
        ('Correspondent', 'Correspondent'),
        ('Costume Designer', 'Costume Designer'),
        ('Dancer', 'Dancer'),
        ('Dialogue Coach', 'Dialogue Coach'),
        ('Director', 'Director'),
        ('Director of Photography', 'Director of Photography'),
        ('Distribution Company', 'Distribution Company'),
        ('Draughtsman', 'Draughtsman'),
        ('Dresser', 'Dresser'),
        ('Dubber', 'Dubber'),
        ('Editor/Producer (News)', 'Editor/Producer (News)'),
        ('Editor-in-chief', 'Editor-in-chief'),
        ('Editor-of-the-Day', 'Editor-of-the-Day'),
        ('Ensemble', 'Ensemble'),
        ('Executive Producer', 'Executive Producer'),
        ('Expert', 'Expert'),
        ('Fight Director', 'Floor Manager'),
        ('Floor Manager', 'Floor Manager'),
        ('Focus Puller', 'Focus Puller'),
        ('Foley Artist', 'Foley Artist'),
        ('Foley Editor', 'Foley Editor'),
        ('Foley Mixer', 'Foley Mixer'),
        ('Graphic Assistant', 'Graphic Assistant'),
        ('Graphic Designer', 'Graphic Designer'),
        ('Greensman', 'Greensman'),
        ('Grip', 'Grip'),
        ('Hairdresser', 'Hairdresser'),
        ('Illustrator', 'Illustrator'),
        ('Interviewed Guest', 'Interviewed Guest'),
        ('Interviewer', 'Interviewer'),
        ('Key Character', 'Key Character'),
        ('Key Grip', 'Key Grip'),
        ('Key Talents', 'Key Talents'),
        ('Leadman', 'Leadman'),
        ('Librettist', 'Librettist'),
        ('Lighting director', 'Lighting director'),
        ('Lighting Technician', 'Lighting Technician'),
        ('Location Manager', 'Location Manager'),
        ('Lyricist', 'Lyricist'),
        ('Make Up Artist', 'Make Up Artist'),
        ('Manufacturer', 'Manufacturer'),
        ('Matte Artist', 'Matte Artist'),
        ('Music Arranger', 'Music Arranger'),
        ('Music Group', 'Music Group'),
        ('Musician', 'Musician'),
        ('News Reader', 'News Reader'),
        ('Orchestra', 'Orchestra'),
        ('Participant', 'Participant'),
        ('Photographer', 'Photographer'),
        ('Post-Production Editor', 'Post-Production Editor'),
        ('Producer', 'Producer'),
        ('Production Assistant', 'Production Assistant'),
        ('Production Company', 'Production Company'),
        ('Production Department', 'Production Department'),
        ('Production Manager', 'Production Manager'),
        ('Production Secretary', 'Production Secretary'),
        ('Programme Production Researcher', 'Programme Production Researcher'),
        ('Property Manager', 'Property Manager'),
        ('Publishing Company', 'Publishing Company'),
        ('Puppeteer', 'Puppeteer'),
        ('Pyrotechnician', 'Pyrotechnician'),
        ('Reporter', 'Reporter'),
        ('Rigger', 'Rigger'),
        ('Runner', 'Runner'),
        ('Scenario', 'Scenario'),
        ('Scenic Operative', 'Scenic Operative'),
        ('Script Supervisor', 'Script Supervisor'),
        ('Second Assistant Camera', 'Second Assistant Camera'),
        ('Second Assistant Director', 'Second Assistant Director'),
        ('Second Unit Director', 'Second Unit Director'),
        ('Set Designer', 'Set Designer'),
        ('Set Dresser', 'Set Dresser'),
        ('Sign Language', 'Sign Language'),
        ('Singer', 'Singer'),
        ('Sound Designer', 'Sound Designer'),
        ('Sound Mixer', 'Sound Mixer'),
        ('Sound Recordist', 'Sound Recordist'),
        ('Special Effects', 'Special Effects'),
        ('Stunts', 'Stunts'),
        ('Subtitles', 'Subtitles'),
        ('Technical Director', 'Technical Director'),
        ('Translation', 'Translation'),
        ('Transportation Manager', 'Transportation Manager'),
        ('Treatment / Programme Proposal', 'Treatment / Programme Proposal'),
        ('Vision Mixer', 'Vision Mixer'),
        ('Visual Editor', 'Visual Editor'),
        ('Visual Effects', 'Visual Effects'),
        ('Wardrobe', 'Wardrobe'),
        ('Witness', 'Witness'),
    )
    STANDARD_CHOICES = (
        ('Simple', 'Simple'),
        ('MPAA', 'MPAA'),
        ('V-chip', 'TV Parental Guidelines'),
    )
    RATING_CHOICES = (
        ('Simple', (
                ('Adult', 'Adult'),
                ('Nonadult', 'Non-adult'),
            )
        ),
        ('MPAA', (
                ('G', 'G: General Audiences'),
                ('PG', 'PG: Parental Guidance Suggested'),
                ('PG-13', 'PG-13: Parents Strongly Cautioned'),
                ('R', 'R: Restricted'),
                ('NC-17', 'NC-17: No One 17 and Under Admitted'),
            )
        ),
        ('TV Parental Guidelines', (
                ('TV-Y', 'TV-Y: All children'),
                ('TV-Y7-FV', 'TV-Y7/TV-Y7-FV: Directed to older children'),
                ('TV-G', 'TV-G: General audience'),
                ('TV-PG', 'TV-PG: Parental guidance'),
                ('TV-14', 'TV-14: Parents strongly cautioned'),
                ('TV-MA', 'TV-MA: Mature audiences'),
            )
        ),
    )
    FREQUENCY_CHOICES = (
        ('always', 'Always'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('never', 'Never'),
    )
    # RSS 2.0
    show = models.ForeignKey(Show , on_delete=models.CASCADE)
    title = models.CharField(max_length=255, help_text=gettext_lazy('Make it specific but avoid explicit language. Limit to 100 characters for a Google video sitemap.'))
    active = models.BooleanField(gettext_lazy("Active"),default=True)
    date = models.DateTimeField(gettext_lazy('Recording date'),auto_now_add=True)

    title_type = models.CharField('Title type', max_length=255, blank=True, default='Plain', choices=TYPE_CHOICES)
    slug = models.SlugField(unique=True, help_text=gettext_lazy('Auto-generated from Title.'))
    author = models.ManyToManyField(User, related_name='episode_authors', help_text=gettext_lazy('Remember to save the user\'s name and e-mail address in the <a href="../../../auth/user/">User application</a>.'))
    description_type = models.CharField('Description type', max_length=255, blank=True, default='Plain', choices=TYPE_CHOICES)
    description = models.TextField(help_text=gettext_lazy('Avoid explicit language. Google video sitempas allow 2,048 characters.'))
    captions = DeletingFileField(upload_to='podcasts/episodes/captions/', help_text=gettext_lazy('For video podcasts. Good captioning choices include <a href="http://en.wikipedia.org/wiki/SubViewer">SubViewer</a>, <a href="http://en.wikipedia.org/wiki/SubRip">SubRip</a> or <a href="http://www.w3.org/TR/ttaf1-dfxp/">TimedText</a>.'), blank=True,max_length=255)
    category = models.CharField(max_length=255, blank=True, help_text=gettext_lazy('Limited to one user-specified category for the sake of sanity.'))
    domain = models.URLField(blank=True, help_text=gettext_lazy('A URL that identifies a categorization taxonomy.'))
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, blank=True, help_text=gettext_lazy('The frequency with which the episode\'s data changes. For sitemaps.'), default='never')
    priority = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True, help_text=gettext_lazy('The relative priority of this episode compared to others. 1.0 is the most important. For sitemaps.'), default='0.5')
    status = models.IntegerField(choices=STATUS_CHOICES, default=2)
    update = models.DateTimeField(auto_now=True)
    # iTunes
    subtitle = models.CharField(max_length=255, help_text=gettext_lazy('Looks best if only a few words like a tagline.'), blank=True)
    summary = models.TextField(help_text=gettext_lazy('Allows 4,000 characters. Description will be used if summary is blank.'), blank=True)
    minutes = models.PositiveIntegerField(blank=True, null=True)
    seconds = models.CharField(max_length=2, blank=True, null=True, choices=SECONDS_CHOICES)
    keywords = models.CharField(max_length=255, help_text=gettext_lazy('A comma-delimited list of words for searches, up to 12; perhaps include misspellings.'), blank=True, null=True)
    explicit = models.CharField(max_length=255, choices=EXPLICIT_CHOICES, help_text=gettext_lazy('"Clean" will put the clean iTunes graphic by it.'), default='No')
    block = models.BooleanField(help_text=gettext_lazy('Check to block this episode from iTunes because <br />its content might cause the entire show to be <br />removed from iTunes.'), default=False)
    # Media RSS
    role = models.CharField(max_length=255, blank=True, choices=ROLE_CHOICES, help_text=gettext_lazy('Role codes provided by the <a href="http://www.ebu.ch/en/technical/metadata/specifications/role_codes.php">European Broadcasting Union</a>.'))
    media_category = models.ManyToManyField(MediaCategory, related_name='episode_categories', blank=True)
    standard = models.CharField(max_length=255, blank=True, choices=STANDARD_CHOICES, default='Simple')
    rating = models.CharField(max_length=255, blank=True, choices=RATING_CHOICES, help_text=gettext_lazy('If used, selection must match respective Scheme selection.'), default='Nonadult')
    image = models.ImageField(upload_to='podcasts/episodes/img/', help_text=gettext_lazy('A still image from a video file, but for episode artwork to display in iTunes, image must be <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">saved to file\'s <strong>metadata</strong></a> before episode uploading!'), blank=True)
    text = models.TextField(blank=True, help_text=gettext_lazy('Media RSS text transcript. Must use <media:text> tags. Please see the <a href="https://www.google.com/webmasters/tools/video/en/video.html#tagMediaText">Media RSS 2.0</a> specification for syntax.'))
    deny = models.BooleanField(default=False, help_text=gettext_lazy('Check to deny episode to be shown to users from specified countries.'))
    restriction = models.CharField(max_length=255, blank=True, help_text=gettext_lazy('A space-delimited list of <a href="http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1-coded countries</a>.'))
    # Dublin Core
    start = models.DateTimeField(blank=True, null=True, help_text=gettext_lazy('Start date and time that the media is valid.'))
    end = models.DateTimeField(blank=True, null=True, help_text=gettext_lazy('End date and time that the media is valid.'))
    scheme = models.CharField(max_length=255, blank=True, default='W3C-DTF')
    name = models.CharField(max_length=255, blank=True, help_text=gettext_lazy('Any helper name to distinguish this time period.'))
    # Google Media
    preview = models.BooleanField(default=False, help_text=gettext_lazy("Check to allow Google to show a preview of your media in search results."))
    preview_start_mins = models.PositiveIntegerField('Preview start (minutes)', blank=True, null=True, help_text=gettext_lazy('Start time (minutes) of the media\'s preview, <br />shown on Google.com search results before <br />clicking through to see full video.'))
    preview_start_secs = models.CharField('Preview start (seconds)', max_length=2, blank=True, null=True, choices=SECONDS_CHOICES, help_text=gettext_lazy('Start time (seconds) of the media\'s preview.'))
    preview_end_mins = models.PositiveIntegerField('Preview end (minutes)', blank=True, null=True, help_text=gettext_lazy('End time (minutes) of the media\'s preview, <br />shown on Google.com search results before <br />clicking through to see full video.'))
    preview_end_secs = models.CharField('Preview end (seconds)', max_length=2, blank=True, null=True, choices=SECONDS_CHOICES, help_text=gettext_lazy('End time (seconds) of the media\'s preview.'))
    host = models.BooleanField(default=False, help_text=gettext_lazy('Check to allow Google to host your media after it expires. Must set expiration date in Dublin Core.'))
    # Behind the scenes
    objects = EpisodeManager()

    class Meta(object):
        ordering = ['-date', 'slug']

    def __str__(self):
        return u'%s' % (self.title)

    #@models.permalink
    #def get_absolute_url(self):
    #    return ('podcast_episode', (), { 'show_slug': self.show.slug, 'episode_slug': self.slug })

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('podcast_episode', args=[str(self.show.slug),str(self.slug)])

    def seconds_total(self):
        try:
            return (((float(self.minutes)) * 60) + (float(self.seconds)))
        except:
            return 0




    def was_recorded_today(self):
        return self.rec_date.date() == datetime.date.today()
    was_recorded_today.short_description = gettext_lazy('Recorded today?')

    def __str__(self):
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

    title = models.CharField(max_length=255, blank=True, default=None, help_text=gettext_lazy('Title is generally only useful with multiple enclosures.'))
    file = DeletingFileField(upload_to='podcasts/episodes/files/', help_text=gettext_lazy('Either upload or use the "Player" text box below. If uploading, file must be less than or equal to 30 MB for a Google video sitemap.'),blank=False, null=False,max_length=255)
    mime = models.CharField('Format', max_length=255, choices=MIME_CHOICES, blank=True)
    medium = models.CharField(max_length=255, blank=True, choices=MEDIUM_CHOICES)
    expression = models.CharField(max_length=25, choices=EXPRESSION_CHOICES, blank=True)
    frame = models.CharField('Frame rate', max_length=5, help_text=gettext_lazy('Measured in frames per second (fps), often 29.97.'),choices=FRAME_CHOICES,blank=True)
    bitrate = models.CharField('Bit rate', max_length=6, blank=True, help_text=gettext_lazy('Measured in kilobits per second (kbps), often 128 or 192.'),choices=BITRATE_CHOICES)
    sample = models.CharField('Sample rate', max_length=5, blank=True, help_text=gettext_lazy('Measured in kilohertz (kHz), often 44.1.'),choices=SAMPLE_CHOICHES)
    channel = models.CharField(max_length=5, blank=True, help_text=gettext_lazy('Number of channels; 2 for stereo, 1 for mono.'),choices=CHANNEL_CHOICES)
    algo = models.CharField('Hash algorithm', max_length=50, blank=True, choices=ALGO_CHOICES)
    hash = models.CharField(max_length=255, blank=True, help_text=gettext_lazy('MD-5 or SHA-1 file hash.'))
    player = models.URLField(help_text=gettext_lazy('URL of the player console that plays the media. Could be your own .swf, but most likely a YouTube URL, such as <a href="http://www.youtube.com/v/UZCfK8pVztw">http://www.youtube.com/v/UZCfK8pVztw</a> (not the permalink, which looks like <a href="http://www.youtube.com/watch?v=UZCfK8pVztw">http://www.youtube.com/watch?v=UZCfK8pVztw</a>).'), blank=True)
    embed = models.BooleanField(help_text=gettext_lazy('Check to allow Google to embed your external player in search results on <a href="http://video.google.com">Google Video</a>.'), blank=True)
    width = models.PositiveIntegerField(blank=True, null=True, help_text=gettext_lazy("Width of the browser window in <br />which the URL should be opened. <br />YouTube's default is 425."))
    height = models.PositiveIntegerField(blank=True, null=True, help_text=gettext_lazy("Height of the browser window in <br />which the URL should be opened. <br />YouTube's default is 344."))
    episode = models.ForeignKey(Episode, help_text=gettext_lazy('Include any number of media files; for example, perhaps include an iPhone-optimized, AppleTV-optimized and Flash Video set of video files. Note that the iTunes feed only accepts the first file. More uploading is available after clicking "Save and continue editing."'), on_delete=models.CASCADE)

    class Meta(object):
        ordering = ['mime', 'file']


    def save(self, *args, **kwargs):
        """
        Return a default title numbered by enclosure number
        a missing title is not a good idea for rss and web interface
        """
        if  self.title == "":
            self.title = "Part "+str(Enclosure.objects.filter(Q(episode=self.episode)).all().count()+1)
        super(Enclosure, self).save(*args, **kwargs)


    def __str__(self):
        return u'%s' % (self.file)


class Schedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

       episode = models.ForeignKey(Episode, \
                verbose_name=gettext_lazy('Linked episode:'), on_delete=models.CASCADE)

       emission_date = models.DateTimeField(gettext_lazy('programmed date'),\
                                                 help_text=gettext_lazy("This is the date and time when the program will be on air"))


       #    def emitted(self):
       #           return self.emission_done != None 
       #    emitted.short_description = 'Trasmesso'

       def was_scheduled_today(self):
              return self.emission_date.date() == datetime.date.today()
    
       was_scheduled_today.short_description = gettext_lazy('Scheduled for today?')

       def refepisode(self):
              return self.episode.title
       refepisode.short_description = gettext_lazy('Linked episode:')

       def __str__(self):
               return str(self.episode.title)



class ScheduleDone(models.Model):

       schedule = models.ForeignKey(Schedule, \
                verbose_name=gettext_lazy('Linked schedule:'), on_delete=models.CASCADE)

       enclosure = models.ForeignKey(Enclosure, \
                verbose_name=gettext_lazy('Linked enclosure:'), on_delete=models.CASCADE)

       emission_done = models.DateTimeField(gettext_lazy('emission done')\
              				     ,null=True,editable=False )

       def __str__(self):
               return str(self.emission_done)



class PeriodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    show = models.ForeignKey(Show,verbose_name=\
              			gettext_lazy('refer to show:'), on_delete=models.CASCADE)

    start_date = models.DateField(gettext_lazy('Programmed start date'),null=True,blank=True,\
                             help_text=gettext_lazy("The program will be in palimpsest starting from this date"))
    end_date = models.DateField(gettext_lazy('Programmed end date'),null=True,blank=True,\
                             help_text=gettext_lazy("The program will be in palimpsest ending this date"))
    time = models.TimeField(gettext_lazy('Programmed time'),null=True,blank=True,\
                                help_text=gettext_lazy("This is the time when the program is planned in palimpsest"))
    giorni = models.ManyToManyField(Giorno,verbose_name=gettext_lazy('Programmed days'),blank=True,\
                                        help_text=gettext_lazy("The program will be in palimpsest those weekdays"))


    def __str__(self):
        return str(self.show)

class AperiodicSchedule(models.Model):

#    program = models.ForeignKey(Program, edit_inline=models.TABULAR,\
#    num_in_admin=2,verbose_name='si riferisce al programma:',editable=False)

    show = models.ForeignKey(Show, verbose_name=\
              			gettext_lazy('refer to Show:'), on_delete=models.CASCADE)

    emission_date = models.DateTimeField(gettext_lazy('Programmed date'),\
                             help_text=gettext_lazy("This is the date and time when the program is planned in palimsest"))

    def was_scheduled_today(self):
        return self.emission_date.date() == datetime.date.today()
    
    was_scheduled_today.short_description = gettext_lazy('Programmed for today?')

    def __str__(self):
        return str(self.show)

