Summary: ShoutCast compatible streaming media server
Name: icecast
Version: 2.3.1
Release: 3%{?dist}
Group: Applications/Multimedia
License: GPL
URL: http://www.icecast.org/
Source0: http://downloads.xiph.org/releases/icecast/icecast-%{version}.tar.gz
Source1: status3.xsl
Source2: icecast.init
Source3: icecast.logrotate
Source4: icecast.xml
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides: streaming-server

BuildRequires: automake
BuildRequires: libvorbis-devel >= 1.0, libogg-devel >= 1.0, curl-devel >= 7.10.0
BuildRequires: libxml2-devel, libxslt-devel, speex-devel
# To be enabled as soon as Fedora's libtheora supports ogg_stream_init
BuildRequires: libtheora-devel >= 1.0

Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service


%description
Icecast is a streaming media server which currently supports Ogg Vorbis
and MP3 audio streams. It can be used to create an Internet radio
station or a privately running jukebox and many things in between.  It
is very versatile in that new formats can be added relatively easily and
supports open standards for commuincation and interaction.


%prep
%setup -q
find -name "*.html" -or -name "*.jpg" -or -name "*.css" | xargs chmod 644
%{__sed} -i -e 's/icecast2/icecast/g' debian/icecast2.1


%build
# theora support is to be enabled as soon as Fedora's libtheora supports
# ogg_stream_init
# --disable-theora
%configure
%{__make} %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/icecast/doc
rm -rf %{buildroot}%{_docdir}/icecast
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icecast/web/status3.xsl
install -D -m 755 %{SOURCE2} %{buildroot}%{_initrddir}/icecast
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/icecast
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/icecast.xml
install -D -m 644 debian/icecast2.1 %{buildroot}%{_mandir}/man1/icecast.1
mkdir -p %{buildroot}%{_localstatedir}/log/icecast
mkdir -p %{buildroot}%{_localstatedir}/run/icecast


%clean 
rm -rf %{buildroot}


%pre
/usr/sbin/useradd -M -r -d /usr/share/icecast -s /sbin/nologin \
	-c "icecast streaming server" icecast > /dev/null 2>&1 || :


%post
/sbin/chkconfig --add icecast


%preun
if [ $1 = 0 ]; then
        /sbin/service icecast stop >/dev/null 2>&1
        /sbin/chkconfig --del icecast
fi


%postun
if [ "$1" -ge "1" ]; then
        /sbin/service icecast condrestart >/dev/null 2>&1
fi
if [ $1 = 0 ] ; then
	userdel icecast >/dev/null 2>&1 || :
fi


%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS ChangeLog
%doc doc/*.html
%doc doc/*.jpg
%doc doc/*.css
%config(noreplace) %{_sysconfdir}/icecast.xml
%{_sysconfdir}/logrotate.d/icecast
%{_initrddir}/icecast
%{_bindir}/icecast
%{_datadir}/icecast
%{_mandir}/man1/icecast.1.gz
%dir %attr(-,icecast,icecast) %{_localstatedir}/log/icecast
%dir %attr(-,icecast,icecast) %{_localstatedir}/run/icecast

%changelog
* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.3.1-3
- FE6 Rebuild

* Thu May 04 2006 Andreas Thienemann <andreas@bawue.net> 2.3.1-2
- Enabled Theora Streaming

* Fri Feb 03 2006 Andreas Thienemann <andreas@bawue.net> 2.3.1-1
- Updated to icecast 2.3.1-1

* Wed Aug 03 2005 Andreas Thienemann <andreas@bawue.net> 2.2.0-1
- Initial specfile
