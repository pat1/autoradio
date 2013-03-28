from distutils.core import setup
import os

from distutils.command.build import build as build_
from setuptools.command.develop import develop as develop_
from distutils.core import Command
#from buildutils.cmd import Command
#from distutils.cmd import Command

from django.core import management
from autoradio import _version_

os.environ['DJANGO_SETTINGS_MODULE'] = 'autoradio.settings'
from django.conf import settings


class distclean(Command):
    description = "remove man pages and *.mo files"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        import shutil
        from os.path import join
        try:
            shutil.rmtree("man")
        except:
            pass
        for root, dirs, files in os.walk('locale'):
            for name in files:
                if name[-3:] == ".mo":
                    os.remove(join(root, name))

        # remove all the .pyc files
        for root, dirs, files in os.walk(os.getcwd(), topdown=False):
            for name in files:
                if name.endswith('.pyc') and os.path.isfile(os.path.join(root, name)):
                    print 'removing: %s' % os.path.join(root, name)
                    if not(self.dry_run): os.remove(os.path.join(root, name))


class build(build_):

    sub_commands = build_.sub_commands[:]
    sub_commands.append(('compilemessages', None))
    sub_commands.append(('createmanpages', None))

class compilemessages(Command):
    description = "generate .mo files from .po"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        management.call_command("compilemessages")

class createmanpages(Command):
    description = "generate man page with help2man"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):
        try:
            import subprocess
            subprocess.check_call(["mkdir","-p", "man/man1"])
            subprocess.check_call(["help2man","-N","-o","man/man1/autoradiod.1","./autoradiod"])
            subprocess.check_call(["gzip","-f", "man/man1/autoradiod.1"])
            subprocess.check_call(["help2man","-N","-o","man/man1/autoradioweb.1","./autoradioweb"])
            subprocess.check_call(["gzip", "-f","man/man1/autoradioweb.1"])
            subprocess.check_call(["help2man","-N","-o","man/man1/autoradioctrl.1","./autoradioctrl"])
            subprocess.check_call(["gzip", "-f","man/man1/autoradioctrl.1"])
        except:
            pass

# Compile the list of files available, because distutils doesn't have
# an easy way to do this.
package_data = []
data_files = []

for dirpath, dirnames, filenames in os.walk('man'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])


for dirpath, dirnames, filenames in os.walk('media/sito'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])


for dirpath, dirnames, filenames in os.walk('doc'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])

#for dirpath, dirnames, filenames in os.walk('amarok'):
#    # Ignore dirnames that start with '.'
#    for i, dirname in enumerate(dirnames):
#        if dirname.startswith('.'): del dirnames[i]
#    if filenames:
#        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])


for dirpath, dirnames, filenames in os.walk('locale'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])

for dirpath, dirnames, filenames in os.walk('templates'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])

data_files.append(('/etc/autoradio',['autoradio-site.cfg']))
data_files.append(('/etc/autoradio',['dbus-autoradio.conf']))


#for dirpath, dirnames, filenames in os.walk('autoradio/templates'):
#    # Ignore dirnames that start with '.'
#    for i, dirname in enumerate(dirnames):
#        if dirname.startswith('.'): del dirnames[i]
#    if filenames:
#        for file in filenames:
#            package_data.append('templates/'+ os.path.join(dirname, file))
#
#for dirpath, dirnames, filenames in os.walk('autoradio/locale'):
#    # Ignore dirnames that start with '.'
#    for i, dirname in enumerate(dirnames):
#        if dirname.startswith('.'): del dirnames[i]
#    if filenames:
#        for file in filenames:
#            package_data.append('locale/'+ os.path.join(dirname, file))

#package_data.append('autoradio_config')
#package_data.append('settings')


setup(name='autoradio',
      version=_version_,
      description='radio automation software',
      author='Paolo Patruno',
      author_email='p.patruno@iperbole.bologna.it',
      platforms = ["any"],
      url='http://autoradiobc.sf.net',
      cmdclass={'build': build,'compilemessages':compilemessages,'createmanpages':createmanpages,"distclean":distclean},
      packages=['autoradio', 'autoradio.playlists','autoradio.spots', 
                'autoradio.jingles', 'autoradio.programs',
                'autoradio.player', 'autoradio.doc',
                'autoradio.autoplayer', 'autoradio.mpris2',
                'autoradio.pydbusdecorator',],
      package_data={'autoradio.programs': ['fixtures/*.json']},
      scripts=['autoradiod','autoradioweb','autoradioctrl','autoradio.wsgi',
               'autoplayerd','autoplayergui','autoradiodbusd','jackdaemon'],
      data_files = data_files,
      license = "GNU GPL v2",
      requires= [ "mutagen","django","reportlab"],
      long_description="""\ 
Radio automation software. Simple to use, starting from digital audio
files, manage on-air broadcasting over a radio-station or
web-radio. The main components are:

    * Player (integrated or external Xmms/Audacious): plays all your media
      files and send digital sound to an audio device or audio server
 
    * Scheduler: real time manager for emission of special audio files
      like jingles, spots, playlist and programs; interact with player
      like supervisor User

    * inteface: WEB interface to monitor the player and scheduler and
      admin the schedules for the complete control over your station
      format. The web interface allows you to easily publish podcasts
      that conform to the RSS 2.0 and iTunes RSS podcast
      specifications
"""
     )
     

      #package_data = {'autoradio': package_data},
      #py_modules = [ 'autoradio_config', 'settings'],

      #
      #package_data = {'autoradio': ['templates/base_incasinato.html']},

      #ackage_data={'autoradio' : ['templates']},
      #packages=['autoradio.mutagen', 'autoradio.programs','autoradio.jingles','autoradio.spots','autoradio.playlists'],
      #py_modules = [ 'autoradio.dir2ogg', 'autoradio.mkplaylist',  'autoradio.xmmsweb', 'autoradio_config', 'autoradio.gest_playlist',\
      #                  'autoradio.gest_spot', 'autoradio.manageamarok', 'autoradio.managepytone',\
      #                  'setup', 'autoradio.autoradio_core',\
      #                  'autoradio.autoxmms', 'autoradio.gest_jingle', 'autoradio.gest_program',\
      #                  'autoradio.managexmms', 'settings', 'autoradio.urls'],
