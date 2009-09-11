%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"
)}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(
1)")}

%define name autoradio
%define version 1.1.1
%define unmangled_version 1.0
%define release 1

Summary: radio automation software
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GNU GPL v2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Paolo Patruno <p.patruno@iperbole.bologna.it>
Url: http://autoradiobc.sf.net
requires:python-mutagen >= 1.17, pyxmms, Django >= 1.0.3 , python-cherrypy2 , python-configobj

%description
\ 
AutoRadio Radio automation software. 
Simple to use, starting from digital audio files manages on-air broadcasting over a radio-station or web-radio. 
The main components are: 
Player (Xmms): plays all your media files and send digital sound to an audio device or audio server; 
Scheduler: real time manager for emission of special audio files like jingles, spots, playlist and programs; interact wi
User inteface: WEB interface to monitor the player and scheduler and admin the schedules for the complete control over y


%prep
%setup -n %{name}-%{unmangled_version} -n %{name}-%{unmangled_version}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT

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
