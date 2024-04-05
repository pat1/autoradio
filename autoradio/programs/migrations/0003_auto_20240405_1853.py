# Generated by Django 3.1.13 on 2024-04-05 18:53

import autoradio.programs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0002_fixture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='show',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='childcategory',
            name='name',
            field=models.CharField(blank=True, choices=[('Arts', (('Design', 'Design'), ('Fashion & Beauty', 'Fashion & Beauty'), ('Food', 'Food'), ('Literature', 'Literature'), ('Performing Arts', 'Performing Arts'), ('Visual Arts', 'Visual Arts'))), ('Business', (('Business News', 'Business News'), ('Careers', 'Careers'), ('Investing', 'Investing'), ('Management & Marketing', 'Management & Marketing'), ('Shopping', 'Shopping'))), ('Education', (('Education Technology', 'Education Technology'), ('Higher Education', 'Higher Education'), ('K-12', 'K-12'), ('Language Courses', 'Language Courses'), ('Training', 'Training'))), ('Games & Hobbies', (('Automotive', 'Automotive'), ('Aviation', 'Aviation'), ('Hobbies', 'Hobbies'), ('Other Games', 'Other Games'), ('Video Games', 'Video Games'))), ('Government & Organizations', (('Local', 'Local'), ('National', 'National'), ('Non-Profit', 'Non-Profit'), ('Regional', 'Regional'))), ('Health', (('Alternative Health', 'Alternative Health'), ('Fitness & Nutrition', 'Fitness & Nutrition'), ('Self-Help', 'Self-Help'), ('Sexuality', 'Sexuality'))), ('Religion & Spirituality', (('Buddhism', 'Buddhism'), ('Christianity', 'Christianity'), ('Hinduism', 'Hinduism'), ('Islam', 'Islam'), ('Judaism', 'Judaism'), ('Other', 'Other'), ('Spirituality', 'Spirituality'))), ('Science & Medicine', (('Medicine', 'Medicine'), ('Natural Sciences', 'Natural Sciences'), ('Social Sciences', 'Social Sciences'))), ('Society & Culture', (('History', 'History'), ('Personal Journals', 'Personal Journals'), ('Philosophy', 'Philosophy'), ('Places & Travel', 'Places & Travel'))), ('Sports & Recreation', (('Amateur', 'Amateur'), ('College & High School', 'College & High School'), ('Outdoor', 'Outdoor'), ('Professional', 'Professional'))), ('Technology', (('Gadgets', 'Gadgets'), ('Tech News', 'Tech News'), ('Podcasting', 'Podcasting'), ('Software How-To', 'Software How-To')))], help_text='Please choose a child category that corresponds to its respective parent category (e.g., "Design" is a child category of "Arts").<br />If no such child category exists for a parent category (e.g., Comedy, Kids & Family, Music, News & Politics, or TV & Film), simply leave this blank and save.', max_length=50),
        ),
        migrations.AlterField(
            model_name='configure',
            name='channel',
            field=models.CharField(default='103', help_text='The station channel for the print of programs book', max_length=80, unique=True),
        ),
        migrations.AlterField(
            model_name='configure',
            name='mezzo',
            field=models.CharField(default='analogico terrestre', help_text='The station kind of emission for the print of programs book', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='configure',
            name='radiostation',
            field=models.CharField(default='Radio', help_text='The station name for the print of programs book', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='configure',
            name='sezione',
            field=models.CharField(default='show', editable=False, max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='configure',
            name='type',
            field=models.CharField(default='radiofonica', help_text='The station type for the print of programs book', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='algo',
            field=models.CharField(blank=True, choices=[('MD5', 'MD5'), ('SHA-1', 'SHA-1')], max_length=50, verbose_name='Hash algorithm'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='bitrate',
            field=models.CharField(blank=True, choices=[('8', '8'), ('11.025', '11.025'), ('16', '16'), ('22.050', '22.050'), ('32', '32'), ('44.1', '44.1'), ('48', '48'), ('96', '96')], help_text='Measured in kilobits per second (kbps), often 128 or 192.', max_length=6, verbose_name='Bit rate'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='channel',
            field=models.CharField(blank=True, choices=[('2', '2'), ('1', '1')], help_text='Number of channels; 2 for stereo, 1 for mono.', max_length=5),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='embed',
            field=models.BooleanField(blank=True, help_text='Check to allow Google to embed your external player in search results on <a href="http://video.google.com">Google Video</a>.'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='expression',
            field=models.CharField(blank=True, choices=[('Sample', 'Sample'), ('Full', 'Full'), ('Nonstop', 'Non-stop')], max_length=25),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='file',
            field=autoradio.programs.models.DeletingFileField(help_text='Either upload or use the "Player" text box below. If uploading, file must be less than or equal to 30 MB for a Google video sitemap.', max_length=255, upload_to='podcasts/episodes/files/'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='frame',
            field=models.CharField(blank=True, choices=[('29.97', '29.97')], help_text='Measured in frames per second (fps), often 29.97.', max_length=5, verbose_name='Frame rate'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='medium',
            field=models.CharField(blank=True, choices=[('Audio', 'Audio'), ('Video', 'Video'), ('Document', 'Document'), ('Image', 'Image'), ('Executable', 'Executable')], max_length=255),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='mime',
            field=models.CharField(blank=True, choices=[('audio/ogg', '.ogg (audio)'), ('audio/mpeg', '.mp3 (audio)'), ('audio/x-m4a', '.m4a (audio)'), ('video/mp4', '.mp4 (audio or video)'), ('video/x-m4v', '.m4v (video)'), ('video/quicktime', '.mov (video)'), ('application/pdf', '.pdf (document)'), ('image/jpeg', '.jpg, .jpeg, .jpe (image)')], max_length=255, verbose_name='Format'),
        ),
        migrations.AlterField(
            model_name='enclosure',
            name='sample',
            field=models.CharField(blank=True, choices=[('24', '24'), ('48', '48'), ('64', '64'), ('96', '96'), ('128', '128'), ('160', '160'), ('196', '196'), ('320', '320')], help_text='Measured in kilohertz (kHz), often 44.1.', max_length=5, verbose_name='Sample rate'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='captions',
            field=autoradio.programs.models.DeletingFileField(blank=True, help_text='For video podcasts. Good captioning choices include <a href="http://en.wikipedia.org/wiki/SubViewer">SubViewer</a>, <a href="http://en.wikipedia.org/wiki/SubRip">SubRip</a> or <a href="http://www.w3.org/TR/ttaf1-dfxp/">TimedText</a>.', max_length=255, upload_to='podcasts/episodes/captions/'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='description_type',
            field=models.CharField(blank=True, choices=[('Plain', 'Plain text'), ('HTML', 'HTML')], default='Plain', max_length=255, verbose_name='Description type'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='explicit',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Clean', 'Clean')], default='No', help_text='"Clean" will put the clean iTunes graphic by it.', max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='frequency',
            field=models.CharField(blank=True, choices=[('always', 'Always'), ('hourly', 'Hourly'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly'), ('never', 'Never')], default='never', help_text="The frequency with which the episode's data changes. For sitemaps.", max_length=10),
        ),
        migrations.AlterField(
            model_name='episode',
            name='image',
            field=models.ImageField(blank=True, help_text='A still image from a video file, but for episode artwork to display in iTunes, image must be <a href="http://answers.yahoo.com/question/index?qid=20080501164348AAjvBvQ">saved to file\'s <strong>metadata</strong></a> before episode uploading!', upload_to='podcasts/episodes/img/'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='preview_end_mins',
            field=models.PositiveIntegerField(blank=True, help_text="End time (minutes) of the media's preview, <br />shown on Google.com search results before <br />clicking through to see full video.", null=True, verbose_name='Preview end (minutes)'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='preview_end_secs',
            field=models.CharField(blank=True, choices=[('00', '0'), ('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'), ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59')], help_text="End time (seconds) of the media's preview.", max_length=2, null=True, verbose_name='Preview end (seconds)'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='preview_start_mins',
            field=models.PositiveIntegerField(blank=True, help_text="Start time (minutes) of the media's preview, <br />shown on Google.com search results before <br />clicking through to see full video.", null=True, verbose_name='Preview start (minutes)'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='preview_start_secs',
            field=models.CharField(blank=True, choices=[('00', '0'), ('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'), ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59')], help_text="Start time (seconds) of the media's preview.", max_length=2, null=True, verbose_name='Preview start (seconds)'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='priority',
            field=models.DecimalField(blank=True, decimal_places=1, default='0.5', help_text='The relative priority of this episode compared to others. 1.0 is the most important. For sitemaps.', max_digits=2, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='rating',
            field=models.CharField(blank=True, choices=[('Simple', (('Adult', 'Adult'), ('Nonadult', 'Non-adult'))), ('MPAA', (('G', 'G: General Audiences'), ('PG', 'PG: Parental Guidance Suggested'), ('PG-13', 'PG-13: Parents Strongly Cautioned'), ('R', 'R: Restricted'), ('NC-17', 'NC-17: No One 17 and Under Admitted'))), ('TV Parental Guidelines', (('TV-Y', 'TV-Y: All children'), ('TV-Y7-FV', 'TV-Y7/TV-Y7-FV: Directed to older children'), ('TV-G', 'TV-G: General audience'), ('TV-PG', 'TV-PG: Parental guidance'), ('TV-14', 'TV-14: Parents strongly cautioned'), ('TV-MA', 'TV-MA: Mature audiences')))], default='Nonadult', help_text='If used, selection must match respective Scheme selection.', max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='role',
            field=models.CharField(blank=True, choices=[('Actor', 'Actor'), ('Adaptor', 'Adaptor'), ('Anchor person', 'Anchor person'), ('Animal Trainer', 'Animal Trainer'), ('Animator', 'Animator'), ('Announcer', 'Announcer'), ('Armourer', 'Armourer'), ('Art Director', 'Art Director'), ('Artist/Performer', 'Artist/Performer'), ('Assistant Camera', 'Assistant Camera'), ('Assistant Chief Lighting Technician', 'Assistant Chief Lighting Technician'), ('Assistant Director', 'Assistant Director'), ('Assistant Producer', 'Assistant Producer'), ('Assistant Visual Editor', 'Assistant Visual Editor'), ('Author', 'Author'), ('Broadcast Assistant', 'Broadcast Assistant'), ('Broadcast Journalist', 'Broadcast Journalist'), ('Camera Operator', 'Camera Operator'), ('Carpenter', 'Carpenter'), ('Casting', 'Casting'), ('Causeur', 'Causeur'), ('Chief Lighting Technician', 'Chief Lighting Technician'), ('Choir', 'Choir'), ('Choreographer', 'Choreographer'), ('Clapper Loader', 'Clapper Loader'), ('Commentary or Commentator', 'Commentary or Commentator'), ('Commissioning Broadcaster', 'Commissioning Broadcaster'), ('Composer', 'Composer'), ('Computer programmer', 'Computer programmer'), ('Conductor', 'Conductor'), ('Consultant', 'Consultant'), ('Continuity Checker', 'Continuity Checker'), ('Correspondent', 'Correspondent'), ('Costume Designer', 'Costume Designer'), ('Dancer', 'Dancer'), ('Dialogue Coach', 'Dialogue Coach'), ('Director', 'Director'), ('Director of Photography', 'Director of Photography'), ('Distribution Company', 'Distribution Company'), ('Draughtsman', 'Draughtsman'), ('Dresser', 'Dresser'), ('Dubber', 'Dubber'), ('Editor/Producer (News)', 'Editor/Producer (News)'), ('Editor-in-chief', 'Editor-in-chief'), ('Editor-of-the-Day', 'Editor-of-the-Day'), ('Ensemble', 'Ensemble'), ('Executive Producer', 'Executive Producer'), ('Expert', 'Expert'), ('Fight Director', 'Floor Manager'), ('Floor Manager', 'Floor Manager'), ('Focus Puller', 'Focus Puller'), ('Foley Artist', 'Foley Artist'), ('Foley Editor', 'Foley Editor'), ('Foley Mixer', 'Foley Mixer'), ('Graphic Assistant', 'Graphic Assistant'), ('Graphic Designer', 'Graphic Designer'), ('Greensman', 'Greensman'), ('Grip', 'Grip'), ('Hairdresser', 'Hairdresser'), ('Illustrator', 'Illustrator'), ('Interviewed Guest', 'Interviewed Guest'), ('Interviewer', 'Interviewer'), ('Key Character', 'Key Character'), ('Key Grip', 'Key Grip'), ('Key Talents', 'Key Talents'), ('Leadman', 'Leadman'), ('Librettist', 'Librettist'), ('Lighting director', 'Lighting director'), ('Lighting Technician', 'Lighting Technician'), ('Location Manager', 'Location Manager'), ('Lyricist', 'Lyricist'), ('Make Up Artist', 'Make Up Artist'), ('Manufacturer', 'Manufacturer'), ('Matte Artist', 'Matte Artist'), ('Music Arranger', 'Music Arranger'), ('Music Group', 'Music Group'), ('Musician', 'Musician'), ('News Reader', 'News Reader'), ('Orchestra', 'Orchestra'), ('Participant', 'Participant'), ('Photographer', 'Photographer'), ('Post-Production Editor', 'Post-Production Editor'), ('Producer', 'Producer'), ('Production Assistant', 'Production Assistant'), ('Production Company', 'Production Company'), ('Production Department', 'Production Department'), ('Production Manager', 'Production Manager'), ('Production Secretary', 'Production Secretary'), ('Programme Production Researcher', 'Programme Production Researcher'), ('Property Manager', 'Property Manager'), ('Publishing Company', 'Publishing Company'), ('Puppeteer', 'Puppeteer'), ('Pyrotechnician', 'Pyrotechnician'), ('Reporter', 'Reporter'), ('Rigger', 'Rigger'), ('Runner', 'Runner'), ('Scenario', 'Scenario'), ('Scenic Operative', 'Scenic Operative'), ('Script Supervisor', 'Script Supervisor'), ('Second Assistant Camera', 'Second Assistant Camera'), ('Second Assistant Director', 'Second Assistant Director'), ('Second Unit Director', 'Second Unit Director'), ('Set Designer', 'Set Designer'), ('Set Dresser', 'Set Dresser'), ('Sign Language', 'Sign Language'), ('Singer', 'Singer'), ('Sound Designer', 'Sound Designer'), ('Sound Mixer', 'Sound Mixer'), ('Sound Recordist', 'Sound Recordist'), ('Special Effects', 'Special Effects'), ('Stunts', 'Stunts'), ('Subtitles', 'Subtitles'), ('Technical Director', 'Technical Director'), ('Translation', 'Translation'), ('Transportation Manager', 'Transportation Manager'), ('Treatment / Programme Proposal', 'Treatment / Programme Proposal'), ('Vision Mixer', 'Vision Mixer'), ('Visual Editor', 'Visual Editor'), ('Visual Effects', 'Visual Effects'), ('Wardrobe', 'Wardrobe'), ('Witness', 'Witness')], help_text='Role codes provided by the <a href="http://www.ebu.ch/en/technical/metadata/specifications/role_codes.php">European Broadcasting Union</a>.', max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='scheme',
            field=models.CharField(blank=True, default='W3C-DTF', max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='seconds',
            field=models.CharField(blank=True, choices=[('00', '0'), ('01', '1'), ('02', '2'), ('03', '3'), ('04', '4'), ('05', '5'), ('06', '6'), ('07', '7'), ('08', '8'), ('09', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='standard',
            field=models.CharField(blank=True, choices=[('Simple', 'Simple'), ('MPAA', 'MPAA'), ('V-chip', 'TV Parental Guidelines')], default='Simple', max_length=255),
        ),
        migrations.AlterField(
            model_name='episode',
            name='status',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Public'), (3, 'Private')], default=2),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title_type',
            field=models.CharField(blank=True, choices=[('Plain', 'Plain text'), ('HTML', 'HTML')], default='Plain', max_length=255, verbose_name='Title type'),
        ),
        migrations.AlterField(
            model_name='mediacategory',
            name='name',
            field=models.CharField(choices=[('Action & Adventure', 'Action & Adventure'), ('Ads & Promotional', 'Ads & Promotional'), ('Anime & Animation', 'Anime & Animation'), ('Art & Experimental', 'Art & Experimental'), ('Business', 'Business'), ('Children & Family', 'Children & Family'), ('Comedy', 'Comedy'), ('Dance', 'Dance'), ('Documentary', 'Documentary'), ('Drama', 'Drama'), ('Educational', 'Educational'), ('Faith & Spirituality', 'Faith & Spirituality'), ('Health & Fitness', 'Health & Fitness'), ('Foreign', 'Foreign'), ('Gaming', 'Gaming'), ('Gay & Lesbian', 'Gay & Lesbian'), ('Home Video', 'Home Video'), ('Horror', 'Horror'), ('Independent', 'Independent'), ('Mature & Adult', 'Mature & Adult'), ('Movie (feature)', 'Movie (feature)'), ('Movie (short)', 'Movie (short)'), ('Movie Trailer', 'Movie Trailer'), ('Music & Musical', 'Music & Musical'), ('Nature', 'Nature'), ('News', 'News'), ('Political', 'Political'), ('Religious', 'Religious'), ('Romance', 'Romance'), ('Independent', 'Independent'), ('Sci-Fi & Fantasy', 'Sci-Fi & Fantasy'), ('Science & Technology', 'Science & Technology'), ('Special Interest', 'Special Interest'), ('Sports', 'Sports'), ('Stock Footage', 'Stock Footage'), ('Thriller', 'Thriller'), ('Travel', 'Travel'), ('TV Show', 'TV Show'), ('Western', 'Western')], max_length=50),
        ),
        migrations.AlterField(
            model_name='parentcategory',
            name='name',
            field=models.CharField(choices=[('Arts', 'Arts'), ('Business', 'Business'), ('Comedy', 'Comedy'), ('Education', 'Education'), ('Games & Hobbies', 'Games & Hobbies'), ('Government & Organizations', 'Government & Organizations'), ('Health', 'Health'), ('Kids & Family', 'Kids & Family'), ('Music', 'Music'), ('News & Politics', 'News & Politics'), ('Religion & Spirituality', 'Religion & Spirituality'), ('Science & Medicine', 'Science & Medicine'), ('Society & Culture', 'Society & Culture'), ('Sports & Recreation', 'Sports & Recreation'), ('Technology', 'Technology'), ('TV & Film', 'TV & Film')], help_text='After saving this parent category, please map it to one or more Child Categories below.', max_length=50),
        ),
        migrations.AlterField(
            model_name='show',
            name='category_show',
            field=models.CharField(blank=True, help_text='Limited to one user-specified category for the sake of sanity.', max_length=255, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='show',
            name='copyright',
            field=models.CharField(choices=[('Public domain', 'Public domain'), ('Creative Commons: Attribution (by)', 'Creative Commons: Attribution (by)'), ('Creative Commons: Attribution-Share Alike (by-sa)', 'Creative Commons: Attribution-Share Alike (by-sa)'), ('Creative Commons: Attribution-No Derivatives (by-nd)', 'Creative Commons: Attribution-No Derivatives (by-nd)'), ('Creative Commons: Attribution-Non-Commercial (by-nc)', 'Creative Commons: Attribution-Non-Commercial (by-nc)'), ('Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)', 'Creative Commons: Attribution-Non-Commercial-Share Alike (by-nc-sa)'), ('Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)', 'Creative Commons: Attribution-Non-Commercial-No Dreivatives (by-nc-nd)'), ('All rights reserved', 'All rights reserved')], default='All rights reserved', help_text='See <a href="http://creativecommons.org/about/license/">Creative Commons licenses</a> for more information.', max_length=255),
        ),
        migrations.AlterField(
            model_name='show',
            name='copyright_url',
            field=models.URLField(blank=True, help_text='A URL pointing to additional copyright information. Consider a <a href="http://creativecommons.org/licenses/">Creative Commons license URL</a>.', verbose_name='Copyright URL'),
        ),
        migrations.AlterField(
            model_name='show',
            name='explicit',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Clean', 'Clean')], default='No', help_text='"Clean" will put the clean iTunes graphic by it.', max_length=255),
        ),
        migrations.AlterField(
            model_name='show',
            name='feedburner',
            field=models.URLField(blank=True, help_text='Fill this out after saving this show and at least one episode. URL should look like "http://feeds.feedburner.com/TitleOfShow". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.', verbose_name='FeedBurner URL'),
        ),
        migrations.AlterField(
            model_name='show',
            name='image',
            field=models.ImageField(blank=True, help_text='An attractive, original square JPEG (.jpg) or PNG (.png) image of 600x600 pixels. Image will be scaled down to 50x50 pixels at smallest in iTunes.', upload_to='podcasts/shows/img/'),
        ),
        migrations.AlterField(
            model_name='show',
            name='itunes',
            field=models.URLField(blank=True, help_text='Fill this out after saving this show and at least one episode. URL should look like "http://phobos.apple.com/WebObjects/MZStore.woa/wa/viewPodcast?id=000000000". See <a href="http://code.google.com/p/django-podcast/">documentation</a> for more.', verbose_name='iTunes Store URL'),
        ),
        migrations.AlterField(
            model_name='show',
            name='language',
            field=models.CharField(blank=True, default='en-us', help_text='Default is American English. See <a href="http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes">ISO 639-1</a> and <a href="http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements">ISO 3166-1</a> for more language codes.', max_length=5),
        ),
        migrations.AlterField(
            model_name='show',
            name='ttl',
            field=models.PositiveIntegerField(blank=True, help_text='"Time to Live," the number of minutes a channel can be cached before refreshing.', null=True, verbose_name='TTL'),
        ),
    ]
