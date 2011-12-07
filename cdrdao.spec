Summary:   Writes audio CD-Rs in disk-at-once (DAO) mode
Name:      cdrdao
Version:   1.2.3
Release:   4%{?dist}
License:   GPLv2+
Group:     Applications/Multimedia
URL:       http://cdrdao.sourceforge.net/
Source0:   http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtkmm24-devel
BuildRequires:  libgnomeuimm26-devel
BuildRequires:  libsigc++20-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  desktop-file-utils
BuildRequires:  libao-devel

# Only exclude s390
ExcludeArch: s390 s390x

# Some missing includes cause failure build
Patch1: cdrdao-1.2.3-stat.patch

%description
Cdrdao records audio CD-Rs in disk-at-once (DAO) mode, based on a
textual description of the CD contents. Recording in DAO mode writes
the complete disc (lead-in, one or more tracks, and lead-out) in a
single step. DAO allows full control over the length and the contents
of pre-gaps, the pause areas between tracks.


%package -n gcdmaster
Summary:      A Gnome2 Disk-At-Once (DAO) Audio CD writer
Group:        Applications/Multimedia
Requires:     cdrdao = %{version}-%{release}

Requires(post):   shared-mime-info desktop-file-utils
Requires(postun): shared-mime-info desktop-file-utils
Requires(pre):    GConf2
Requires(post):   GConf2
Requires(preun):  GConf2


%description -n gcdmaster
Gcdmaster is a GNOME2 GUI front-end to cdrdao that makes it easy to
visualize and manipulate audio information before burning it onto
CD. Its features include: cut/copy/paste of sound samples, track marks
edition and silence insertion.


%prep
%setup -q
%patch1 -p1 -b .stat


%build
%configure \
        --with-xdao \
        --without-scglib \
        --without-lame

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

desktop-file-install \
  --vendor "" \
  --mode 644 \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --delete-original \
  $RPM_BUILD_ROOT%{_datadir}/applications/gcdmaster.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%post -n gcdmaster
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/gcdmaster.schemas > /dev/null  || :
killall -HUP gconfd-2 &>/dev/null || :


%postun -n gcdmaster
update-mime-database %{_datadir}/mime > /dev/null 2>&1 || :
update-desktop-database %{_datadir}/applications > /dev/null 2>&1 || :
if [ "$1" -gt 1 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gcdmaster.schemas >/dev/null || :
  killall -HUP gconfd-2 &>/dev/null || :
fi


%preun
if [ "$1" -eq 0 ]; then
  export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
  gconftool-2 --makefile-uninstall-rule %{_sysconfdir}/gconf/schemas/gcdmaster.schemas > /dev/null || :
  killall -HUP gconfd-2 &>/dev/null || :
fi


%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING README CREDITS ChangeLog
%{_bindir}/cdrdao
%{_bindir}/*toc*
%{_datadir}/cdrdao
%{_mandir}/*/cdrdao*
%{_mandir}/*/cue2toc*
%{_mandir}/*/toc2cue*
%{_mandir}/*/toc2cddb*

%files -n gcdmaster
%defattr(-, root, root, -)
%{_bindir}/gcdmaster
%{_datadir}/gcdmaster
%{_datadir}/applications/*.desktop
%{_datadir}/mime-info/gcdmaster*
%{_datadir}/mime/packages/gcdmaster.xml
%{_datadir}/application-registry/gcdmaster.applications
%{_datadir}/pixmaps/*
%{_sysconfdir}/gconf/schemas/gcdmaster.schemas
%{_mandir}/man1/gcdmaster*


%changelog
* Wed Jan 20 2010 Roman Rakus rrakus@redhat.com 1.2.3-3
- no need option --with-mp3-support. it needs libmad(don't ship)
- change license to GPLv2+
- Some missing includes cause failure build
  Resolves Merge review

* Mon Jan 11 2010 rrakus@redhat.com 1.2.3-2
- Forgot to add new source
- Removed unnecessary patches
  Resolves: #554391

* Mon Jan 11 2010 rrakus@redhat.com 1.2.3-1
- Update to release 1.2.3
- Resolves #554391

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.2.3-0.rc2.5
- Rebuilt for RHEL 6

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.2.3-0.rc2.4
- Update desktop file according to F-12 FedoraStudio feature

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-0.rc2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Denis Leroy <denis@poolshark.org> - 1.2.3-0.rc2.2
- Make sure version is printed with usage, to fix k3b

* Tue Apr  7 2009 Denis Leroy <denis@poolshark.org> - 1.2.3-0.rc2.1
- Update to latest 1.2.3 release candidate
- Merged with gcdmaster spec file
- Added scripts to manage gcdmaster new schemas file
- Moved desktop file fix into patch
- Added patch to fix gcc 4.4 compile

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-5
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 harald@redhat.com 1.2.2-4
- added string.h includes to make it compile again

* Fri Aug 17 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-3
- changed license to GPLv2

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-2
- fixed specfile issues (bug #225639)

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-1
- version 1.2.2
- built without cdrecord-devel now

* Mon Aug 21 2006 Harald Hoyer <harald@redhat.com> - 1.2.1-2
- rebuild with new/old cdrtools

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.1-1.1
- rebuild

* Wed Mar 08 2006 Harald Hoyer <harald@redhat.com> - 1.2.1-1
- version 1.2.1 (1.2.0 was not functional)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Harald Hoyer <harald@redhat.com>
- rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jul 18 2005 Harald Hoyer <harald@redhat.com> 1.2.0-1
- version 1.2.0

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Tue Feb 22 2005 Karsten Hopp <karsten@redhat.de> 1.1.9-8 
- cdrdao builds just fine without the pccts package and uses 
  its own pccts copy.

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Wed Oct 13 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-6
- build requires newer cdrecord-devel

* Tue Sep 21 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-5
- removed INSTALL from doc (bug 132908)

* Wed Sep 08 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-4
- build requires newer cdrecord-devel

* Tue Sep 07 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-3
- build requires newer cdrecord-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-1
- version 1.1.9

* Wed Apr 14 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-4
- fixed BuildRequires

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-3
- fixed ISO C++ issues

* Fri Feb 20 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-2
- fixed ambigous operator cast

* Wed Feb 18 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-1
- use scsilib from cdrecord-devel

* Mon Feb 16 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-1
- version 1.1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Harald Hoyer <harald@redhat.de> 1.1.7-8.atapi.1
- added ATAPI: support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Harald Hoyer <harald@redhat.de> 1.1.7-6
- refined O_EXCL patch, nonroot sg handling

* Mon May 12 2003 Harald Hoyer <harald@redhat.de> 1.1.7-5
- refined O_EXCL patch, nonroot sg handling

* Wed Feb 26 2003 Harald Hoyer <harald@redhat.de> 1.1.7-4
- refined O_EXCL patch

* Tue Feb 25 2003 Harald Hoyer <harald@redhat.de> 1.1.7-3
- readded O_EXCL patch

* Tue Feb 04 2003 Phil Knirsch <pknirsch@redhat.com> 1.1.7-2
- Added s390x again as newer models will have SCSI.

* Thu Jan 29 2003 Harald Hoyer <harald@redhat.de> 1.1.7-1
- updated to 1.1.7

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov 28 2002 Harald Hoyer <harald@redhat.de> 1.1.5-11
- added cdrdao-1.1.5-EXCL.patch to lock the CDROM device
- more archs for scsilib (cdrtools)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-9
- Rebuilt in new environment with gcc 3.2

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-6
- Bumped release, and rebuilt against new toolchain.

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-5
- Bumped release, and rebuilt against new toolchain.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.1.5-4
- automated rebuild

* Sun Dec 23 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-3
- Added missing /usr/share/cdrdao/drivers file (#57785)
- Also built 1.1.5-1.72.0 package for 7.x

* Sat Dec 22 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-2
- Bumped release and rebuilt so rawhide package doesn't release number
  conflict with previous 1.1.5-1 package built against 7.2

* Fri Dec 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix non-standard C++ code

* Tue Dec 18 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-1
- Updated to 1.1.5
- Updated endianness patch for ia64
- s/Copyright/License/ in specfile
- Changed to bz2 compression for smaller sources
- Fixed BuildRoot line (was hard coded)

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Tue Jun 26 2001 Bill Nottingham <notting@redhat.com>
- include on ia64

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add excludearch for s390 s390x

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Fri Sep 8 2000 Tim Powers <timp@redhat.com>
- removed all references to xcdrdao, we don't ship it. So no applnk, no gtkmm
  requirements either.

* Thu Sep 7 2000 Tim Powers <timp@redhat.com>
- fixed bad Requires line, was still requiring gtk--, when the package changed
  to gtkmm

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- man pages in correct location
- use %%makeinstall

* Mon May 8 2000 Tim Powers <timp@redhat.com>
- use applnk for dirs
- use %%configure
- remove redundant defines
- rebuilt for 7.0

* Tue Nov 2 1999 Tim Powers <timp@redhat.com>
- updated to 1.1.3
- we now have xcdrdao
- added gnome menu stuff

* Fri Aug 21 1999 Tim Powers <timp@redhat.com>
- removed wmconfig stuff. Nosuch file names xcdrdao

* Wed Aug 18 1999 Dale Lovelace <dale@redhat.com>
- add cdrdao.wmconfig

* Sat Jul 10 1999 Tim Powers <timp@redhat.com>
- updated to 1.1.1 
- built for 6.1

* Mon May 10 1999 Cristian Gafton <gafton@redhat.com>
- gtk-- does not wokr on the alpha, so we have no xcdrdao for it.
- cheesy workaround for the broken tar archive

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package 
