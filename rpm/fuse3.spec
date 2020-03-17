Name:       fuse3
Version:    3.9.0
Release:    1
Summary:    File System in Userspace (FUSE) v3 utilities
License:    GPLv2
URL:        http://fuse.sf.net
Source0:    %{name}-%{version}.tar.bz2
Source1:    fuse.conf

BuildRequires:    which
BuildRequires:    libselinux-devel
BuildRequires:    meson, ninja
Requires:         fuse-common

%description
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 userspace tools to
mount a FUSE filesystem.

%package libs
Summary:    File System in Userspace (FUSE) v3 libraries
License:    LGPLv2

%description libs
Devel With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains the FUSE v3 libraries.

%package devel
Summary:    File System in Userspace (FUSE) v3 devel files
Requires:   %{name}-libs = %{version}-%{release}
Requires:   pkgconfig
License:    LGPLv2

%description devel
With FUSE it is possible to implement a fully functional filesystem in a
userspace program. This package contains development files (headers,
pgk-config) to develop FUSE v3 based applications/filesystems.

%package doc
Summary:    Documentation for %{name}
Requires:   %{name} = %{version}-%{release}

%description doc
Man pages for %{name}.

%package -n fuse-common
Summary:    Common files for File System in Userspace (FUSE) v2 and v3
License:    GPLv2

%description -n fuse-common
Common files for FUSE v2 and FUSE v3.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
# Define udev rules dir so that we don't need .pc dependency.
%meson -Dudevrulesdir=/lib/udev/rules.d -Duseroot=false
%meson_build

%install
export MESON_INSTALL_DESTDIR_PREFIX=%{buildroot}/usr %meson_install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Get rid of static libs
rm -f %{buildroot}/%{_libdir}/*.a

# Install config-file
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}

%ifnarch %{ix86} x86_64
# For some reason /dev/fuse doesn't exist on ARM builds and make install
# creates the node which doesn't belong to the package, thus these lines.
rm -f %{buildroot}/dev/fuse
rm -rf  %{buildroot}/dev
%endif

# Delete pointless udev rules, default udev rules contain fuse already.
rm -f %{buildroot}/lib/udev/rules.d/99-fuse3.rules

%post -p /sbin/ldconfig libs
%postun -p /sbin/ldconfig libs

%files
%license LICENSE GPL2.txt
%{_sbindir}/mount.fuse3
%attr(4755,root,root) %{_bindir}/fusermount3
%exclude %{_sysconfdir}/init.d/fuse3

%files libs
%defattr(-,root,root,-)
%license LGPL2.txt
%{_libdir}/libfuse3.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libfuse3.so
%{_libdir}/pkgconfig/fuse3.pc
%dir %{_includedir}/fuse3
%{_includedir}/fuse3/*.h

%files doc
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog.rst README.md
%{_mandir}/man1/*
%{_mandir}/man8/*

%files -n fuse-common
%defattr(-,root,root,-)
%config %{_sysconfdir}/fuse.conf
