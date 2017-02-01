%{!?__python2: %define __python2 python2}
%{!?python2_sitelib: %define python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python2_lib; print get_python2_lib()"
)}
%{!?python2_sitearch: %define python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python2_lib; print get_python2_lib(
1)")}

%define name autoradio
%define version 2.8.7
%define release 8%{?dist}

Summary: radio automation software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
# tmpfiles.d configuration for the /var/run directory
#Source1:  %{name}-tmpfiles.conf
License: GNU GPL v2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Paolo Patruno <p.patruno@iperbole.bologna.it>
Url: https://github.com/pat1/autoradio
BuildRequires: python2-devel, python-setuptools, gettext, python-configobj, python-magic, python-django >= 1.7.0 , help2man, python-setuptools
Requires:python-mutagen >= 1.17 , python-django >= 1.7.0,  python-configobj, python-cherrypy, python-reportlab >= 2.0,  python-docutils, sqlite >= 3.6.22, speex-tools, python-magic, python-pillow, python-six 
#, python-django-extensions
Requires: initscripts
#%if 0%{?fedora} < 10
#Requires: pyxmms, xmms
#%else
## Requires: dbus-python, audacious >= 1.5
Requires: dbus-python, gstreamer, gstreamer-plugins-base, gstreamer-plugins-good, gstreamer-python
#, gstreamer-plugins-bad, gstreamer-plugins-bad-free, gstreamer-plugins-bad-free-extras
#%endif

# Compile options:
# --with cherrypy          : do not need cherrypy2
##%if 0%{?fedora} < 10
##%if 0%{?_with_}
##Requires: python-cherrypy
##%else
##Requires: python-cherrypy2
##%endif

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
##%{__python2} setup.py build
%py2_build

%install
##%{__python2} setup.py install --root=$RPM_BUILD_ROOT
%py2_install

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
%dir %{python2_sitelib}/%{name}
%{python2_sitelib}/%{name}/*
%{python2_sitelib}/%{name}-*
%{_mandir}/man1/*

%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf

#%{_datadir}/autoradio/*
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
