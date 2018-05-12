# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent 1
%define _enable_debug_packages %nil
%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	1.3.15
Release:	1
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
Source0:	http://download.deluge-torrent.org/source/%{name}-%{version}.tar.gz
# (Debian) add patch to disable checking for updates by default
Patch0:		new_release_check.patch
Patch1:		deluge-1.1.8-use-multithreaded-boost.patch
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(python2)
BuildRequires:	boost-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	imagemagick
BuildRequires:	pythonegg(setuptools)
BuildRequires:	intltool
%if %{sys_libtorrent}
BuildRequires:	python-libtorrent-rasterbar >= 0.14.9
%endif
Requires:	librsvg2
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs
Requires:	python-twisted-web
Requires:	python-simplejson
Requires:	python-notify
Requires:	python-OpenSSL
Requires:	python-chardet
Requires:	python-pkg-resources
%if %{sys_libtorrent}
Requires:	python-libtorrent-rasterbar >= 0.14.9
BuildArch:	noarch
%endif

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%files
%doc ChangeLog
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%if %{sys_libtorrent}
%{py2_puresitedir}/*
%else
%{py2_platsitedir}/*
%endif
%{_datadir}/pixmaps/%{name}.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}*.1.*

#----------------------------------------------------------------------------

%prep
%setup -q

%patch0 -p1 -b .update
%patch1 -p1 -b .mt

%build
%ifarch x86_64 sparc64
	CFLAGS="%{optflags} -DAMD64" %{__python2} setup.py build
%else
	CFLAGS="%{optflags}" %{__python2} setup.py build
%endif

%install
%{__python2} ./setup.py install -O1 --skip-build --root=%{buildroot}
