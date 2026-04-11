Summary: radio automation software
Name: autoradio
Version: 4.2.1
Release: 1
Source0: %{name}-%{version}.tar.gz
# tmpfiles.d configuration for the /var/run directory
#Source1:  %%{name}-tmpfiles.conf
License: GNU GPL v2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Paolo Patruno <p.patruno@iperbole.bologna.it>
Url: https://github.com/pat1/autoradio

BuildRequires: python3-devel, python3-setuptools, gettext
BuildRequires: python3-configobj, python3-file-magic , help2man
BuildRequires: python3-mutagen
BuildRequires:  desktop-file-utils
%if 0%{?fedora}
BuildRequires: python3-django
%else
BuildRequires: python3-django4.2
%endif

Requires:python3-mutagen >= 1.17, python3-configobj, python3-cherrypy, python3-reportlab >= 2.0,  python3-docutils, sqlite >= 3.6.22, speex-tools, python3-file-magic, python3-pillow, pydub >= 0.25.2
Requires:rsgain,sox

%if 0%{?fedora}
Requires: python3-django
%else
Requires: python3-django4.2
%endif

#, python-django-extensions
#Requires: initscripts
#%if 0%%{?fedora} < 10
#Requires: pyxmms, xmms
#%else
## Requires: dbus-python, audacious >= 1.5
Requires: python3-dbus, python3-gstreamer1, gstreamer1-plugins-base, gstreamer1-plugins-good
#, gstreamer-plugins-bad, gstreamer-plugins-bad-free, gstreamer-plugins-bad-free-extras
#%endif

%description
\ 

Radio automation software. Simple to use, starting from digital audio
files, manage on-air broadcasting over a radio-station or
web-radio. The main components are:

    * Player integrated (gstreamer) or external (Xmms/Audacious):
      plays all your media files and send digital sound to an audio
      device or audio server

    * Scheduler: real time manager for emission of special audio files
      like jingles, spots, playlist and programs; interact with player
      like supervisor User

    * inteface: WEB interface to monitor the player and scheduler and
      admin the schedules for the complete control over your station
      format. The web interface allows you to easily publish podcasts
      that conform to the RSS 2.0 and iTunes RSS podcast specifications
      The web interface provide a "full compatible" ogg player.

Developed with Python, Django, Dbus it works in an production enviroment

%prep
%setup -n %{name}-%{version} -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

##%{__install} -d -m 0710 %{buildroot}%{_var}/{run/autoradio,log/autoradio}

mkdir -p %{buildroot}%{_localstatedir}/run/
mkdir -p %{buildroot}%{_localstatedir}/log/
%{__install} -d -m 0710 %{buildroot}%{_localstatedir}/{run/autoradio,log/autoradio}

mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d
%{__install} -m 0644 %{name}-tmpfiles.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf


%{__install} -d %{buildroot}%{_datadir}/pixmaps/
%{__install} logo/autochannel_assembler.png %{buildroot}%{_datadir}/pixmaps/
%{__install} logo/autoplayergui.png %{buildroot}%{_datadir}/pixmaps/
desktop-file-install \
    --add-category="AudioVideo" \
    --dir=%{buildroot}%{_datadir}/applications \
    desktop/autochannel_assembler.desktop
desktop-file-install \
    --add-category="AudioVideo" \
    --dir=%{buildroot}%{_datadir}/applications \
    desktop/autoplayergui.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)

%doc COPYING README doc/*
%config(noreplace) %{_sysconfdir}/%{name}/autoradio-site.cfg
%config(noreplace) %{_sysconfdir}/%{name}/dbus-autoradio.conf
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/*
%{python3_sitelib}/%{name}-*
%{_mandir}/man1/*

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf

%{_datadir}/applications/autochannel_assembler.desktop
%{_datadir}/pixmaps/autochannel_assembler.png
%{_datadir}/applications/autoplayergui.desktop
%{_datadir}/pixmaps/autoplayergui.png

#%%{_datadir}/autoradio/*
%{_bindir}/autoradiod
%{_bindir}/autoradioweb
%{_bindir}/autoradioctrl
%{_bindir}/autoplayerd
%{_bindir}/autoplayergui
%{_bindir}/autoradiodbusd
%{_bindir}/jackdaemon
%{_bindir}/autometatraced
%{_bindir}/autochannel_assembler

%attr(-,autoradio,autoradio) %dir %{_datadir}/autoradio
%attr(-,autoradio,autoradio) %{_datadir}/%{name}/*

%attr(-,autoradio,autoradio) %dir %{_var}/log/%{name}/
%attr(-,autoradio,autoradio) %dir %{_var}/run/%{name}/

%pre

/usr/bin/getent group autoradio >/dev/null || /usr/sbin/groupadd  autoradio
/usr/bin/getent passwd autoradio >/dev/null || \
        /usr/sbin/useradd  -g autoradio  -d %{_datadir}/autoradio -M \
                -c "autoradio user for radio automation software" autoradio

#/usr/bin/getent group autoradio >/dev/null || /usr/sbin/groupadd -r autoradio
#/usr/bin/getent passwd autoradio >/dev/null || \
#        /usr/sbin/useradd -r -s /sbin/nologin -d %{_datadir}/autoradio -g autoradio \
#                -c "autoradio user for radio automation software" autoradio
## Fix homedir for upgrades
#/usr/sbin/usermod --home %{_datadir}/autoradio autoradio &>/dev/null
##exit 0


#%post
#
## set some useful variables
#AUTORADIO="autoradio"
#CHOWN="/bin/chown"
#ADDUSER="/usr/sbin/adduser"
#USERDEL="/usr/sbin/userdel"
#USERADD="/usr/sbin/useradd"
#GROUPDEL="/usr/sbin/groupdel"
#GROUPMOD="/usr/sbin/groupmod"
#ID="/usr/bin/id"
#
#set -e
#
####
## 1. get current autoradio uid and gid if user exists.
#if $ID $AUTORADIO > /dev/null 2>&1; then
#   IUID=`$ID --user $AUTORADIO`
#   IGID=`$ID --group $AUTORADIO`
#else
#   IUID="NONE"
#   IGID="NONE"
#fi
#
#####
### 2. Ensure that no standard account or group will remain before adding the
###    new user
##if [ "$IUID" = "NONE" ] || [ $IUID -ge 1000 ]; then # we must do sth :)
##  if ! [ "$IUID" = "NONE" ] && [ $IUID -ge 1000 ]; then
##      # autoradio user exists but isn't a system user... delete it.
##      $USERDEL $PEERCAST
##      $GROUPDEL $PEERCAST
##  fi
##
#####
#
## 3. Add the system account.
##    Issue a debconf warning if it fails. 
#  if $GROUPMOD $AUTORADIO > /dev/null 2>&1; then 
#    # peercast group already exists, use --ingroup
#    if ! $ADDUSER --system --disabled-password --disabled-login --home /usr/share/autoradio --no-create-home --ingroup $AUTORADIO $AUTORADIO; then
#      echo "The adduser command failed."
#    fi
#  else
#    if ! $ADDUSER --system --disabled-password --disabled-login --home /usr/share/peercast --no-create-home --group $AUTORADIO; then
#      echo "The adduser command failed."
#    fi
#  fi
#fi
#set +e
#
####
## 4. change ownership of directory
#$CHOWN -R $AUTORADIO:$AUTORADIO /usr/share/autoradio/
#$CHOWN -R $AUTORADIO:$AUTORADIO /var/log/autoradio/
#$CHOWN -R $AUTORADIO:$AUTORADIO /etc/autoradio/
#$CHOWN -R $AUTORADIO:$AUTORADIO /var/run/autoradio/

%changelog
* Sat Apr 11 2026 Paolo Patruno <p.patruno@iperbole.bologna.it> 4.2.1-1
- 4.2.1 release (p.patruno@iperbole.bologna.it)
- bug in multichannel ogg channel reorder (p.patruno@iperbole.bologna.it)
- bug to apply sox on enclosure (wrong check on tags)
  (p.patruno@iperbole.bologna.it)
- bug in autoradioctrl (p.patruno@iperbole.bologna.it)
- added options to autoradioctrl to remove orphaned files
  (p.patruno@iperbole.bologna.it)
- bugs in multichannel gest_spot and do not use sox in multichannel enclosure
  (p.patruno@iperbole.bologna.it)
- more verbose in palimpsest with spots title (p.patruno@iperbole.bologna.it)
- palimpsest book for multichannel (p.patruno@iperbole.bologna.it)
- 4.1 release (p.patruno@iperbole.bologna.it)
- bug in autoradiod (p.patruno@iperbole.bologna.it)
- added a delay to be sure the insert in the autoplayer playlist to be atomic
  (p.patruno@iperbole.bologna.it)
- do not remap writing ogg multichannel because autoplayer remap 5.1 in any
  case (p.patruno@iperbole.bologna.it)
- release 4.0.19 (p.patruno@iperbole.bologna.it)
- replaygain tuning (p.patruno@iperbole.bologna.it)
- release 4.0.18 (p.patruno@iperbole.bologna.it)
- new levels for multitrack files (p.patruno@iperbole.bologna.it)
- handle replaygain with change programs and not with create only; added tags
  to recognize whe sox is applyed (p.patruno@iperbole.bologna.it)
- handle replaygain with change jingles and spots and not with create only
  (p.patruno@iperbole.bologna.it)
- added audioconvert to gstreamer chain to work better with replaygain
  (p.patruno@iperbole.bologna.it)
- bugs in replaygain implementation; new release
  (p.patruno@iperbole.bologna.it)
- bug in replaygain for programs (p.patruno@iperbole.bologna.it)
- headroom=9 pre-amp=6 in gstreamer rgvolume for more volume to output
  (p.patruno@iperbole.bologna.it)
- implemented replaygain in mutichannel chain (p.patruno@iperbole.bologna.it)
- better sox command (p.patruno@iperbole.bologna.it)
- added sox normalization and compander for programs
  (p.patruno@iperbole.bologna.it)
- implemented ReplayGain 2.0 loudness normalizer in programs, spot, jingle on
  upload via rsgain external program and in player via gstreamer
  (p.patruno@iperbole.bologna.it)
- try to use ogg as multichannel format; added autochannel_assembler tool
  (p.patruno@iperbole.bologna.it)
- fascias multichannel in flac; enable flac upload as alternative to ogg; new
  version (p.patruno@iperbole.bologna.it)
- exchange autor and title in programs for autometatraced
  (p.patruno@iperbole.bologna.it)
- new release (p.patruno@iperbole.bologna.it)
- bugs around midnigth (p.patruno@iperbole.bologna.it)
- django 3 problem with default in Max query (p.patruno@iperbole.bologna.it)
- better management of enclosure order (p.patruno@iperbole.bologna.it)
- order enclosure by field and not id (p.patruno@iperbole.bologna.it)
- better admin for playlists (p.patruno@iperbole.bologna.it)
- new release (p.patruno@iperbole.bologna.it)
- better admin (p.patruno@iperbole.bologna.it)
- check duplicated episode; new release (p.patruno@iperbole.bologna.it)
- bugs and better admin (p.patruno@iperbole.bologna.it)
- better admin for schedule (p.patruno@iperbole.bologna.it)
- bugs and schedule check in form (p.patruno@iperbole.bologna.it)
- bugs (p.patruno@iperbole.bologna.it)
- bugsd solved and new release (p.patruno@iperbole.bologna.it)
- bug (p.patruno@iperbole.bologna.it)
- new release (p.patruno@iperbole.bologna.it)
- bugs (p.patruno@iperbole.bologna.it)
- check user for show author; added permission to overwrite the check
  (p.patruno@iperbole.bologna.it)
- tags added for programs, spots and jingle by autoradio with signals now as
  default in config (p.patruno@iperbole.bologna.it)
- generate fascia in multichannel mode as wav (ogg have a bug in ffmpeg);
  overwrite Artist and Title metadata in enclosure; new release
  (p.patruno@iperbole.bologna.it)
- new release (p.patruno@iperbole.bologna.it)
- documentation (p.patruno@iperbole.bologna.it)
- bug in autoplayergui Artist metadata (p.patruno@iperbole.bologna.it)
- release 4.0.4 (p.patruno@iperbole.bologna.it)
- added number of tracks to playlist, autoplayer and autoplayergui
  (p.patruno@iperbole.bologna.it)
- better exception management in autoplayergui (p.patruno@iperbole.bologna.it)
- autoplayergui exit on dbus error (p.patruno@iperbole.bologna.it)
- better autoplayergui (p.patruno@iperbole.bologna.it)
- better player; bug in mpris2 interface; bug in config default; neew monor
  release (p.patruno@iperbole.bologna.it)
- gui with cursor and bar with timing (p.patruno@iperbole.bologna.it)
- better autoplayergui (play from current cursor position and bug in config
  files (p.patruno@iperbole.bologna.it)
- bugs and support for monochannel fascias: release 4.0.2
  (p.patruno@iperbole.bologna.it)
- multichannel local config default to False (p.patruno@iperbole.bologna.it)
- start to play if not is now called at boot of autoradiod, no any more;
  multichannel improvements (p.patruno@iperbole.bologna.it)
- working on channels (p.patruno@iperbole.bologna.it)
- working on multichannel (p.patruno@iperbole.bologna.it)
- multichannel in django, player and first step in spot
  (p.patruno@iperbole.bologna.it)
- bug in autometatraced (p.patruno@iperbole.bologna.it)

* Tue Nov 18 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.4-1
- release 3.8.4 (p.patruno@iperbole.bologna.it)
- added multiple icecast servers (p.patruno@iperbole.bologna.it)
- try to solve too many open files in autoradiod
  (p.patruno@iperbole.bologna.it)

* Fri Nov 14 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.3-3
- compatibilitu for different version of python and fedora and el distribution
  (p.patruno@iperbole.bologna.it)

* Fri Nov 14 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.3-2
- 

* Fri Nov 14 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.3-1
- release 3.8.3 (p.patruno@iperbole.bologna.it)
- close #43 (p.patruno@iperbole.bologna.it)
- release 3.8.2 (p.patruno@iperbole.bologna.it)

* Mon Nov 10 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.2-1
- play twice bug: when the player change media file there is a little time it
  is in stop state so we have to check it more times to restart to play to do
  not repeat to play twice the same media file (p.patruno@iperbole.bologna.it)
- solve: autoradio rely on pygtkcompat. pygtkcompat was a transitional
  mechanism for porting from pygobject 2 to pygobject 3, and the pygobject
  developers removed it after the 3.50.x release series.
  (p.patruno@iperbole.bologna.it)
- bug in logging messages (p.patruno@iperbole.bologna.it)
- preparing new debian release (p.patruno@iperbole.bologna.it)

* Thu Oct 09 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.1-2
- release 3.8.1 (p.patruno@iperbole.bologna.it)
- do not define locale for copr build system (p.patruno@iperbole.bologna.it)
- do not define locale for copr build system (p.patruno@iperbole.bologna.it)

* Thu Oct 09 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8.1-1
- updated spec file and install autoradio.wsgi (p.patruno@iperbole.bologna.it)
- bugs with datetime management with and without tzinfo
  (p.patruno@iperbole.bologna.it)
- 3.8 release (p.patruno@iperbole.bologna.it)

* Sun Oct 05 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.8-1
- added default playlist for cold start (p.patruno@iperbole.bologna.it)
- porting to django 5 (p.patruno@iperbole.bologna.it)
- bug in autometatraced for popolare news (p.patruno@iperbole.bologna.it)
- bug: sleeping wrong time and with last metadata 'tra poco'
  (p.patruno@iperbole.bologna.it)
- filter spots by active (p.patruno@iperbole.bologna.it)

* Sat Aug 02 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-7
- bugs and better admin for spots; solve ignored active field in spot
  (p.patruno@iperbole.bologna.it)
- minors on autometatraced (p.patruno@iperbole.bologna.it)
- better admin for show (p.patruno@iperbole.bologna.it)

* Mon Feb 17 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-6
- bug in gest_spot mutagen file (p.patruno@iperbole.bologna.it)

* Mon Feb 17 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-5
- better admin interface (p.patruno@iperbole.bologna.it)
- skip jingle and spots in autometatraced during playlist
  (p.patruno@iperbole.bologna.it)
- bug wrong jingle order for null date (p.patruno@iperbole.bologna.it)
- added next program message to autometatraced (p.patruno@iperbole.bologna.it)

* Sat Feb 15 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-4
- added next on air in autometatraced (p.patruno@iperbole.bologna.it)

* Wed Feb 12 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-3
- bug: new inserted jingles with a big number of old jingles ordered with NULL
  emission_date was never emitted (p.patruno@iperbole.bologna.it)

* Fri Feb 07 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-2
- added autometatraced in spec file (p.patruno@iperbole.bologna.it)

* Fri Feb 07 2025 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.7-1
- added autometatraced schedule logger and streaming updater
  (p.patruno@iperbole.bologna.it)
- solve bug in palimpsest around midnight and better management for metadata in
  streaming (p.patruno@iperbole.bologna.it)
- try to solve too many file opened error (p.patruno@iperbole.bologna.it)
- dynamic initial values in programsbook form (p.patruno@iperbole.bologna.it)
- bug for palimpsest generation (p.patruno@iperbole.bologna.it)
- configuration for jackd changed (p.patruno@iperbole.bologna.it)
- reverse order for spots (p.patruno@iperbole.bologna.it)

* Mon Apr 08 2024 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-6
- close #35 (p.patruno@iperbole.bologna.it)
- migrate to django 3 (p.patruno@iperbole.bologna.it)

* Fri Apr 05 2024 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-5
- close #39 (p.patruno@iperbole.bologna.it)
- close #36 (p.patruno@iperbole.bologna.it)
- close #40 (p.patruno@iperbole.bologna.it)
- DJango 3.x compatibility (tchet@debian.org)

* Fri Dec 29 2023 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-4
- sintax error (p.patruno@iperbole.bologna.it)

* Fri Dec 29 2023 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-3
- remove python3-future dependency (p.patruno@iperbole.bologna.it)

* Fri Dec 29 2023 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-2
- bugs on string codec (p.patruno@iperbole.bologna.it)

* Fri Dec 29 2023 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.6-1
- drop extraneous imports of part of stdlib (alexandre.detiste@gmail.com)
- remove Python2 support (alexandre.detiste@gmail.com)
- remove SIX crumbs (alexandre.detiste@gmail.com)
- minor improvements (p.patruno@iperbole.bologna.it)

* Wed Sep 29 2021 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.5-1
- changed securesec (the time to have to play in current position in playlist
  when we insert track in playlist) from 10 to 20 sec
  (p.patruno@iperbole.bologna.it)
- revert busaddress patch and limit the number of districa call to solve
  infinite loop, ported the web interface (p.patruno@iperbole.bologna.it)
- migrate to the last mpris2 python interface (p.patruno@iperbole.bologna.it)
- close #30 (p.patruno@iperbole.bologna.it)
- bug loading playlist; generator in python 3 do not work if used more time
  (p.patruno@iperbole.bologna.it)
- more documentation (p.patruno@iperbole.bologna.it)
- new release for debian new convenction with matainer
  (p.patruno@iperbole.bologna.it)
- new README (p.patruno@iperbole.bologna.it)

* Thu Jan 23 2020 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.3-4
- exception with player without track list (p.patruno@iperbole.bologna.it)

* Wed Jan 15 2020 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.3-3
- working on spec file (p.patruno@iperbole.bologna.it)
- little update in documentation (p.patruno@iperbole.bologna.it)

* Wed Jan 15 2020 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.3-2
- working on spec file (p.patruno@iperbole.bologna.it)
- working on spec file (p.patruno@iperbole.bologna.it)
- working on spec file (p.patruno@iperbole.bologna.it)
- working on spec file (p.patruno@iperbole.bologna.it)
- new sper release (p.patruno@iperbole.bologna.it)

* Wed Jan 15 2020 Paolo Patruno <p.patruno@iperbole.bologna.it> 3.3-1
- added shebang for python3 ; release 3.3 (p.patruno@iperbole.bologna.it)
- release 3.2 for Debian (p.patruno@iperbole.bologna.it)
- migrate to django 2.2 and python3 bugs (p.patruno@iperbole.bologna.it)
- bug on debian install (default locale) and python3 refinements
  (root@localhost.localdomain)
- ready for release 3.0 (p.patruno@iperbole.bologna.it)
- ported player to python 3 (p.patruno@iperbole.bologna.it)
- new migration for python3 (p.patruno@iperbole.bologna.it)
- porting to python3 with futurize (p.patruno@iperbole.bologna.it)
- sure you specify the proper version support in your setup.py file
  (p.patruno@iperbole.bologna.it)
- new stable release for Debian (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it> 2.8.9-1
- 

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it> 2.8.8-1
- standard spec file (ppatruno@arpa.emr.it)
- bug in spec (ppatruno@arpa.emr.it)
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- bug in spec (ppatruno@arpa.emr.it)
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- removed SOURCE1 fron spec file (ppatruno@arpa.emr.it)
- better monit example (ppatruno@arpa.emr.it)
- new package built with tito (ppatruno@arpa.emr.it)
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it>
- lost autoradio-tmpfiles.conf (ppatruno@arpa.emr.it)

* Wed Feb 01 2017 Paolo Patruno <ppatruno@arpa.emr.it> 2.8.7-8
- new package built with tito

* Sat Aug 10 2013 Paolo Patruno <pat1@localhost.localdomain> - 2.8.0-1%{?dist}
- bumped to version 2.8

* Mon Feb 18 2013 Paolo Patruno <pat1@iperbole.bologna.it> - 2.7.0-1%{?dist}
- autoradio 2.7 with pygst

* Sat Apr 14 2012 Paolo Patruno <p.patruno@iperbole.bologna.it> - 2.3-2%{?dist}
- tmpfiles.d is a service provided by both systemd and upstart in Fedora 15 and later for managing temporary files and directories for daemons https://fedoraproject.org/wiki/Packaging:Tmpfiles.d

* Sat Apr 14 2012 Paolo Patruno <p.patruno@iperbole.bologna.it> - 2.3-1%{?dist}
- updated to 2.3


* Fri Aug 12 2011 Paolo Patruno <p.patruno@iperbole.bologna.it> - 2.1beta-1%{?dist}
- upstream version 2.1beta
