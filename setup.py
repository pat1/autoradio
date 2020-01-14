from __future__ import print_function
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
import django
django.setup()


class distclean(Command):
    description = "remove man pages static files and *.mo files"
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
        try:
            shutil.rmtree("static")
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
                    print('removing: %s' % os.path.join(root, name))
                    if not(self.dry_run): os.remove(os.path.join(root, name))


        try:
            os.remove("autoradio/programs/static/programs/playogg/js/jquery-1.12.4.min.js")
        except:
            print("autoradio/programs/static/programs/playogg/js/jquery-1.12.4.min.js not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/js/jquery.min.js")
        except:
            print("autoradio/programs/static/programs/playogg/js/jquery.min.js not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/flash/AnOgg.swf")
        except:
            print("autoradio/programs/static/programs/playogg/flash/AnOgg.swf not removed")
        try:
            os.remove("anoggplayer/anoggplayer/AnOgg.swf")
        except:
            print("anoggplayer/anoggplayer/AnOgg.swf not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/java/cortado.jar")
        except:
            print("autoradio/programs/static/programs/playogg/java/cortado.jar not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/java/cortado-ovt-stripped-0.6.0.jar")
        except:
            print("autoradio/programs/static/programs/playogg/java/cortado-ovt-stripped-0.6.0.jar not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/swfobject/expressInstall.swf")
        except:
            print("autoradio/programs/static/programs/playogg/swfobject/expressInstall.swf not removed")
        try:
            os.remove("autoradio/programs/static/programs/playogg/swfobject/swfobject.js")
        except:
            print("autoradio/programs/static/programs/playogg/swfobject/swfobject.js not removed")


class build(build_):

    sub_commands = build_.sub_commands[:]
    sub_commands.append(('djangocollectstatic', None))
    sub_commands.append(('compilemessages', None))
    sub_commands.append(('createmanpages', None))

class buildall(build_):
    description = "compile and install binary"
    user_options = []   
    boolean_options = []
    sub_commands = Command.sub_commands[:]
    sub_commands.append(('haxecompileanoggplayer', None))
    sub_commands.append(('installbin', None))


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
            subprocess.check_call(["help2man","-n","autoradiod daemon for autoradio suite","-N","-o","man/man1/autoradiod.1","./autoradiod"])
            subprocess.check_call(["gzip","-f", "man/man1/autoradiod.1"])
            subprocess.check_call(["help2man","-n","autoradioweb daemon for autoradio suite","-N","-o","man/man1/autoradioweb.1","./autoradioweb"])
            subprocess.check_call(["gzip", "-f","man/man1/autoradioweb.1"])
            subprocess.check_call(["help2man","-n","autoradio controller tool","-N","-o","man/man1/autoradioctrl.1","./autoradioctrl"])
            subprocess.check_call(["gzip", "-f","man/man1/autoradioctrl.1"])
            subprocess.check_call(["help2man","-n","autoradio dbus daemon","-N","-o","man/man1/autoradiodbusd.1","./autoradiodbusd"])
            subprocess.check_call(["gzip", "-f","man/man1/autoradiodbusd.1"])
            subprocess.check_call(["help2man","-n","autoradio jack daemon","-N","-o","man/man1/jackdaemon.1","./jackdaemon"])
            subprocess.check_call(["gzip", "-f","man/man1/jackdaemon.1"])
            subprocess.check_call(["help2man","-n","autoradio player daemon","-N","-o","man/man1/autoplayerd.1","./autoplayerd"])
            subprocess.check_call(["gzip", "-f","man/man1/autoplayerd.1"])
            subprocess.check_call(["help2man","-n","autoradio player GUI","-N","-o","man/man1/autoplayergui.1","./autoplayergui"])
            subprocess.check_call(["gzip", "-f","man/man1/autoplayergui.1"])

        except:
            pass


class haxecompileanoggplayer(Command):
    description = "generate anoggplayer executable with haxe"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):

        try:
            import subprocess
            import os
            os.chdir("anoggplayer/anoggplayer")
            subprocess.check_call(["make"])
            os.chdir("../..")
        except:
            print("WARNING !!!!!  anoggplayer not created")

class djangocollectstatic(Command):
    description = "collect static files for web server to serve it"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):

        from django.core import management
        management.call_command("collectstatic", verbosity=0, interactive=False)

        #print "execute django collectstatic files"
        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autoradio.settings")
        #from django.core.management import execute_from_command_line
        #execute_from_command_line([ "execname",'collectstatic',"--noinput"])


class installbin(Command):
    description = "install flash and java binary for full distribution not debian compliant"
    user_options = []   
    boolean_options = []

    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass

    def run(self):

        import os
        #if (not os.path.exists("../../autoradio/programs/static/programs/playogg/flash")):
        #    os.mkdir("../../autoradio/programs/static/programs/playogg/flash")
        os.link("jquery/jquery-1.12.4.min.js","autoradio/programs/static/programs/playogg/js/jquery-1.12.4.min.js")
        os.link("jquery/jquery.min.js","autoradio/programs/static/programs/playogg/js/jquery.min.js")
        os.link("anoggplayer/anoggplayer/AnOgg.swf","autoradio/programs/static/programs/playogg/flash/AnOgg.swf")
        os.link("cortado/cortado.jar","autoradio/programs/static/programs/playogg/java/cortado.jar")
        os.link("cortado/cortado-ovt-stripped-0.6.0.jar","autoradio/programs/static/programs/playogg/java/cortado-ovt-stripped-0.6.0.jar")
        os.link("expressinstall/expressInstall.swf", "autoradio/programs/static/programs/playogg/swfobject/expressInstall.swf")
        os.link("expressinstall/swfobject.js", "autoradio/programs/static/programs/playogg/swfobject/swfobject.js")


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

data_files.append(['share/autoradio/server/',['autoradio.wsgi']])

for dirpath, dirnames, filenames in os.walk('static'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if filenames:
        data_files.append(['share/autoradio/'+dirpath, [os.path.join(dirpath, f) for f in filenames]])

data_files.append(('share/autoradio/media',[]))
#data_files.append(('share/autoradio/static',[]))
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
      classifiers=(
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
      ),
      cmdclass={'build': build,'compilemessages':compilemessages,'createmanpages':createmanpages,"distclean":distclean,"haxecompileanoggplayer":haxecompileanoggplayer,"installbin":installbin,"buildall":buildall,"djangocollectstatic":djangocollectstatic},
      packages=['autoradio', 'autoradio.playlists','autoradio.spots', 
                'autoradio.jingles', 'autoradio.programs',
                'autoradio.playlists.migrations','autoradio.spots.migrations', 
                'autoradio.jingles.migrations', 'autoradio.programs.migrations',
                'autoradio.player', 'autoradio.doc',
                'autoradio.autoplayer', 'autoradio.mpris2',
                'autoradio.dbusdecorator'],
      package_data={
          'autoradio.doc': ['templates/doc/*'],
          'autoradio.programs': ['fixtures/*.json',
                                 'static/programs/*.png',
                                 'static/programs/css/*',
                                 'static/programs/css/*',
                                 'static/programs/playogg/*.png',
                                 'static/programs/playogg/flash/*',
                                 'static/programs/playogg/java/*',
                                 'static/programs/playogg/js/*',
                                 'static/programs/playogg/swfobject/*',
                                 'templates/*.html',
                                 'templates/palimpsest/*.html',
                                 'templates/player/*.html',
                                 'templates/podcast/*.html',
                                 'templates/schedule/*.html',
                                 'templates/xmms/*.html'
                             ],
          'autoradio':['global_static/*'],
      },
      scripts=['autoradiod','autoradioweb','autoradioctrl',
               'autoplayerd','autoplayergui','autoradiodbusd','jackdaemon'],
      data_files = data_files,
      license = "GNU GPL v2",
      requires= [ "mutagen","django","reportlab","configobj"],
      long_description="""\ 
Radio automation software. Simple to use, starting from digital audio
files, manage on-air broadcasting over a radio-station or
web-radio. The main components are:

    * Player (integrated gstreamer or external Xmms/Audacious): plays all your media
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
