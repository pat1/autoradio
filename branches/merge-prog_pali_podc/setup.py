from distutils.core import setup
import os

from distutils.command.build import build as build_
from setuptools.command.develop import develop as develop_
from distutils.core import Command
#from buildutils.cmd import Command
#from distutils.cmd import Command

from django.core import management
from django.core.management import setup_environ
from autoradio import settings

setup_environ(settings)

class build(build_):

    sub_commands = build_.sub_commands[:]
    sub_commands.append(('compilemessages', None))

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


# Compile the list of files available, because distutils doesn't have
# an easy way to do this.
package_data = []
data_files = []

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

for dirpath, dirnames, filenames in os.walk('amarok'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])


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
      version='2.0.0alpha',
      description='radio automation software',
      author='Paolo Patruno',
      author_email='p.patruno@iperbole.bologna.it',
      platforms = ["any"],
      url='http://autoradiobc.sf.net',
      cmdclass={'build': build,'compilemessages':compilemessages},
      packages=['autoradio', 'autoradio.playlists','autoradio.spots', 
                'autoradio.jingles', 'autoradio.programs',
                'autoradio.player'],
      package_data={'autoradio.programs': ['fixtures/*.json']},
      scripts=['autoradiod','autoradioweb','autoradioctrl'],
      data_files = data_files,
      license = "GNU GPL v2",
      requires= [ "mutagen","django","reportlab"],
      long_description="""\ 
AutoRadio Radio automation software. 
Simple to use, starting from digital audio files manages on-air broadcasting over a radio-station or web-radio. 
The main components are: 
Player (Xmms): plays all your media files and send digital sound to an audio device or audio server; 
Scheduler: real time manager for emission of special audio files like jingles, spots, playlist and programs; interact wi
User inteface: WEB interface to monitor the player and scheduler and admin the schedules for the complete control over y
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
