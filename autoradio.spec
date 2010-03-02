%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
)}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(
1)")}

%define name autoradio
%define version 1.4.0
%define release 1%{?dist}

Summary: radio automation software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: GNU GPL v2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Paolo Patruno <p.patruno@iperbole.bologna.it>
Url: http://autoradiobc.sf.net
BuildRequires: python-configobj , Django >= 1.0.3 
Requires:python-mutagen >= 1.17 , Django >= 1.0.3,  python-configobj, python-cherrypy, python-reportlab >= 2.0,  python-docutils
%if 0%{?fedora} < 10
Requires: pyxmms, xmms
%else
Requires: dbus-python, audacious >= 1.5
%endif

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
AutoRadio Radio automation software. 
Simple to use, starting from digital audio files manages on-air broadcasting over a radio-station or web-radio. 
The main components are: 
Player (Xmms): plays all your media files and send digital sound to an audio device or audio server; 
Scheduler: real time manager for emission of special audio files like jingles, spots, playlist and programs; interact wi
User inteface: WEB interface to monitor the player and scheduler and admin the schedules for the complete control over y


%prep
%setup -n %{name}-%{version} -n %{name}-%{version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT

mkdir -p  $RPM_BUILD_ROOT/%{_var}/log/autoradio/
mkdir -p  $RPM_BUILD_ROOT/%{_var}/run/autoradio/


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

%doc COPYING README
%config(noreplace) %{_sysconfdir}/autoradio/autoradio-site.cfg
%dir %{python_sitelib}/autoradio
%{python_sitelib}/autoradio/*
%{python_sitelib}/autoradio-*

%dir %{_datadir}/autoradio
%{_datadir}/autoradio/*

#%{_datadir}/autoradio/locale/*
%{_bindir}/autoradiod
%{_bindir}/autoradioweb
%{_bindir}/autoradioctrl

%dir %{_var}/log/autoradio/
%dir %{_var}/run/autoradio/

%post

# set some useful variables
AUTORADIO="autoradio"
CHOWN="/bin/chown"
ADDUSER="/usr/sbin/adduser"
USERDEL="/usr/sbin/userdel"
USERADD="/usr/sbin/useradd"
GROUPDEL="/usr/sbin/groupdel"
GROUPMOD="/usr/sbin/groupmod"
ID="/usr/bin/id"

set -e

###
# 1. get current autoradio uid and gid if user exists.
if $ID $AUTORADIO > /dev/null 2>&1; then
   IUID=`$ID --user $AUTORADIO`
   IGID=`$ID --group $AUTORADIO`
else
   IUID="NONE"
   IGID="NONE"
fi

####
## 2. Ensure that no standard account or group will remain before adding the
##    new user
#if [ "$IUID" = "NONE" ] || [ $IUID -ge 1000 ]; then # we must do sth :)
#  if ! [ "$IUID" = "NONE" ] && [ $IUID -ge 1000 ]; then
#      # autoradio user exists but isn't a system user... delete it.
#      $USERDEL $PEERCAST
#      $GROUPDEL $PEERCAST
#  fi
#
####

# 3. Add the system account.
#    Issue a debconf warning if it fails. 
  if $GROUPMOD $AUTORADIO > /dev/null 2>&1; then 
    # peercast group already exists, use --ingroup
    if ! $ADDUSER --system --disabled-password --disabled-login --home /usr/share/autoradio --no-create-home --ingroup $AUTORADIO $AUTORADIO; then
      echo "The adduser command failed."
    fi
  else
    if ! $ADDUSER --system --disabled-password --disabled-login --home /usr/share/peercast --no-create-home --group $AUTORADIO; then
      echo "The adduser command failed."
    fi
  fi
fi
set +e

###
# 4. change ownership of directory
$CHOWN -R $AUTORADIO:$AUTORADIO /usr/share/autoradio/
$CHOWN -R $AUTORADIO:$AUTORADIO /var/log/autoradio/
$CHOWN -R $AUTORADIO:$AUTORADIO /etc/autoradio/
$CHOWN -R $AUTORADIO:$AUTORADIO /var/run/autoradio/
