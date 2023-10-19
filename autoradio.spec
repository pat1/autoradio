Summary: radio automation software
Name: autoradio
Version: 3.5
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
BuildRequires: python3-devel, python3-setuptools, gettext, python3-configobj, python3-magic, python3-django >= 2.2 , help2man, python3-setuptools
Requires:python3-mutagen >= 1.17 , python3-django >= 2.2,  python3-configobj, python3-cherrypy, python3-reportlab >= 2.0,  python3-docutils, sqlite >= 3.6.22, speex-tools, python3-magic, python3-pillow
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

#%%{_datadir}/autoradio/*
%{_bindir}/autoradiod
%{_bindir}/autoradioweb
%{_bindir}/autoradioctrl
%{_bindir}/autoplayerd
%{_bindir}/autoplayergui
%{_bindir}/autoradiodbusd
%{_bindir}/jackdaemon

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
