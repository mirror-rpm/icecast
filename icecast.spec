Summary: ShoutCast compatible streaming media server
Name: icecast
Version: 2.3.2
Release: 7%{?dist}
Group: Applications/Multimedia
License: GPLv2
URL: http://www.icecast.org/
Source0: http://downloads.xiph.org/releases/icecast/icecast-%{version}.tar.gz
Source1: status3.xsl
Source2: icecast.service
Source3: icecast.logrotate
Source4: icecast.xml

Provides: streaming-server

BuildRequires: automake
BuildRequires: libvorbis-devel >= 1.0, libogg-devel >= 1.0, curl-devel >= 7.10.0
BuildRequires: libxml2-devel, libxslt-devel, speex-devel, libtheora-devel >= 1.0
BuildRequires: openssl-devel
BuildRequires: systemd-units

Requires(pre): /usr/sbin/useradd
Requires(post): systemd-sysv
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


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
%configure \
	--with-curl \
	--with-openssl \
	--with-ogg \
	--with-theora \
	--with-speex
%{__make} %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_datadir}/icecast/doc
rm -rf %{buildroot}%{_docdir}/icecast
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icecast/web/status3.xsl
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/icecast.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/icecast
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/icecast.xml
install -D -m 644 debian/icecast2.1 %{buildroot}%{_mandir}/man1/icecast.1
mkdir -p %{buildroot}%{_localstatedir}/log/icecast
mkdir -p %{buildroot}%{_localstatedir}/run/icecast


%pre
/usr/sbin/useradd -M -r -d /usr/share/icecast -s /sbin/nologin \
	-c "icecast streaming server" icecast > /dev/null 2>&1 || :


%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable icecast.service > /dev/null 2>&1 || :
    /bin/systemctl stop icecast.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart icecast.service >/dev/null 2>&1 || :
fi
if [ $1 = 0 ] ; then
	userdel icecast >/dev/null 2>&1 || :
fi


%triggerun -- icecast < 2.3.2-7
# Save the current service runlevel info
/usr/bin/systemd-sysv-convert --save icecast >/dev/null 2>&1 ||:
# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del icecast >/dev/null 2>&1 || :
/bin/systemctl try-restart icecast.service >/dev/null 2>&1 || :


%files
%doc AUTHORS COPYING NEWS ChangeLog TODO
%doc doc/*.html doc/*.jpg doc/*.css
%doc conf/*.dist examples/icecast_auth-1.0.tar.gz
%config(noreplace) %{_sysconfdir}/icecast.xml
%{_sysconfdir}/logrotate.d/icecast
%{_unitdir}/icecast.service
%{_bindir}/icecast
%{_datadir}/icecast
%{_mandir}/man1/icecast.1.gz
%dir %attr(-,icecast,icecast) %{_localstatedir}/log/icecast
%dir %attr(-,icecast,icecast) %{_localstatedir}/run/icecast

%changelog
* Fri Feb 24 2012 Petr Pisar <ppisar@redhat.com> - 2.3.2-7
- Remove obsolete buildroot and defattr declarations from spec file
- Move to systemd (bug #782149)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
p Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 21 2009 Andreas Thienemann <andreas@bawue.net> - 2.3.2-4
- Added SSL support
- Added LSB header to the initscripts
- Reworked config example to contain newest changes
- Added alternative config files and authentication example

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.3.2-1
- update to 2.3.2
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.3.1-5
- Autorebuild for GCC 4.3

* Mon Nov 06 2006 Jindrich Novy <jnovy@redhat.com> - 2.3.1-4
- rebuild because of the new curl

* Fri Sep 08 2006 Andreas Thienemann <andreas@bawue.net> - 2.3.1-3
- FE6 Rebuild

* Thu May 04 2006 Andreas Thienemann <andreas@bawue.net> 2.3.1-2
- Enabled Theora Streaming

* Fri Feb 03 2006 Andreas Thienemann <andreas@bawue.net> 2.3.1-1
- Updated to icecast 2.3.1-1

* Wed Aug 03 2005 Andreas Thienemann <andreas@bawue.net> 2.2.0-1
- Initial specfile
