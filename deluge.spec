%define name deluge
%define version 0.5.1.90
%define release %mkrel 1

Summary: Bittorrent client based on GTK+ 2
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://download.deluge-torrent.org/testing/%{name}-%{version}.tar.gz

# FOR SYSTEM LIBTORRENT Source1: %{name}-fixed-setup.py

# There's a check to see what style the distro uses for Boost libs
# in setup.py. It doesn't work for a buildsystem-type environment
# as it relies on the existence of /etc/issue , which is generated
# at boot time. So let's just patch the check out of existence and
# set the variable to the correct value.
Patch0: deluge-0.5.1.90-nomt.patch
License: GPL
Group: Networking/File transfer
Url: http://deluge-torrent.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: desktop-file-utils
# FOR SYSTEM LIBTORRENT BuildRequires: libtorrent-rasterbar-devel
BuildRequires: python-devel
BuildRequires: libboost-devel
BuildRequires: libz-devel
BuildRequires: openssl-devel
BuildRequires: ImageMagick
Requires: pyxdg

%description
Deluge is a Bittorrent client written in Python and GTK+. Deluge is 
intended to bring a native, full-featured client to Linux GTK+ desktop 
environments such as GNOME and XFCE.

%prep
%setup -q
# FOR SYSTEM LIBTORRENT install -m 0755 %{SOURCE1} ./setup.py
%patch0 -p1 -b .nomt

%build
# FOR SYSTEM LIBTORRENT # We forcibly don't store the installation directory during the build, so
# FOR SYSTEM LIBTORRENT # we need to ensure that it is properly inserted into the code as required.
# FOR SYSTEM LIBTORRENT sed -i -e "s:INSTALL_PREFIX = '@datadir@':INSTALL_PREFIX = '%{_usr}':" \
# FOR SYSTEM LIBTORRENT 	src/dcommon.py

%ifarch x86_64 sparc64
	CFLAGS="%{optflags} -DAMD64" python setup.py build
%else
	CFLAGS="%{optflags}" python setup.py build
%endif

%install
rm -rf $RPM_BUILD_ROOT
python ./setup.py install --root=$RPM_BUILD_ROOT

desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-category="Application" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*

mkdir -p %buildroot{%_liconsdir,%_miconsdir}
mkdir -p %buildroot%{_iconsdir}/hicolor
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16}
mkdir -p %buildroot%{_iconsdir}/hicolor/{48x48,32x32,24x24,22x22,16x16}/apps
convert -scale 48 pixmaps/%{name}256.png %buildroot%_liconsdir/%{name}.png
convert -scale 48 pixmaps/%{name}256.png %buildroot%_datadir/pixmaps/%{name}.png
convert -scale 48 pixmaps/%{name}256.png %buildroot%_iconsdir/hicolor/48x48/apps/%{name}.png 
convert -scale 32 pixmaps/%{name}256.png %buildroot%_iconsdir/%{name}.png
convert -scale 32 pixmaps/%{name}256.png %buildroot%_iconsdir/hicolor/32x32/apps/%{name}.png
convert -scale 24 pixmaps/%{name}256.png %buildroot%_iconsdir/hicolor/24x24/apps/%{name}.png
convert -scale 22 pixmaps/%{name}256.png %buildroot%_iconsdir/hicolor/22x22/apps/%{name}.png
convert -scale 16 pixmaps/%{name}256.png %buildroot%_miconsdir/%{name}.png
convert -scale 16 pixmaps/%{name}256.png %buildroot%_iconsdir/hicolor/16x16/apps/%{name}.png
rm -f %buildroot%{_datadir}/pixmaps/%{name}.xpm

perl -pi -e 's,%{name}.xpm,%{name},g' %buildroot%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

%post
%update_icon_cache hicolor
%update_menus
%update_desktop_database
%postun
%clean_icon_cache hicolor
%clean_menus
%clean_desktop_database

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %name.lang
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%if %mdkversion >=200710
%py_platsitedir/deluge-%{version}-py*
%endif
%dir %py_platsitedir/deluge
%py_platsitedir/deluge/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%_datadir/pixmaps/%{name}.png
%_iconsdir/hicolor/16x16/apps/%{name}.png
%_iconsdir/hicolor/22x22/apps/%{name}.png
%_iconsdir/hicolor/24x24/apps/%{name}.png
%_iconsdir/hicolor/32x32/apps/%{name}.png
%_iconsdir/hicolor/48x48/apps/%{name}.png
%_liconsdir/%{name}.png
%_iconsdir/%{name}.png
%_miconsdir/%{name}.png


