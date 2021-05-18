%define __cmake_in_source_build 1

# TODO: Current release does not work
# https://github.com/etlegacy/etlegacy/issues/1517
# Using master commit
#
# FIXME: debug information is not yet working

#%%global gitcommit 886f0ef0d6a48b527a25409dbd6eb350e6610e48
%if 0%{?gitcommit:1}
%global snapdate 20211102
%global snapinfo %{snapdate}git%(echo %{gitcommit}| cut -c 1-8)
%global gittag v%%{version}
%global gitver %{gitcommit}
%else
%global gittag v%%{version}
%global gitver %{version}
%endif

# etl is also RH internal tool. Rename binary to etlegacy
%bcond_with altbin

Name:           etlegacy
Version:        2.77.1
# v2.76 tag has broken builds, snap has to be used from current master
Release:        1%{?snapinfo:.%{snapinfo}}%{?dist}
Summary:        Fully compatible client and server for the popular online FPS game Wolfenstein: Enemy Territory 

License:        GPLv3
URL:            https://www.etlegacy.com/
#Source0:        https://github.com/etlegacy/etlegacy/archive/v%%{version}/%%{name}-%%{version}.tar.gz
Source0:        https://github.com/etlegacy/etlegacy/archive/%{gittag}/%{name}-%{gitver}.tar.gz
#Source1:        https://mirror.etlegacy.com/wolfadmin/wolfadmin.tar.gz

BuildRequires:  gcc gcc-c++
BuildRequires:  cmake
BuildRequires:  libpng-devel freetype-devel SDL2-devel curl-devel openssl-devel sqlite-devel
BuildRequires:  libtheora-devel libogg-devel libvorbis-devel libjpeg-turbo-devel
BuildRequires:  glew-devel
BuildRequires:  lua-devel
BuildRequires:  openal-soft-devel minizip-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       shared-mime-info

%description
Welcome to ET: Legacy, an open source project that aims to create a fully compatible client and server
for the popular online FPS game Wolfenstein: Enemy Territory - whose gameplay is still considered unmatched by many,
despite its great age. 

%prep
%autosetup -n %{name}-%{gitver} -p1

%build
%cmake -DBUNDLED_LIBS=OFF -DCROSS_COMPILE32=OFF -DBUILD_MOD=OFF \
       -DFEATURE_RENDERER2=ON -DINSTALL_DEFAULT_BASEDIR=%{_prefix}
%cmake_build


%install
%cmake_install
%if %{with altbin}
mv %{buildroot}%{_bindir}/{etl,etlegacy}
mv %{buildroot}%{_mandir}/man6/et{l,legacy}.6*
sed -e 's/^Exec=etl /Exec=etlegacy /' -i %{buildroot}%{_datadir}/applications/com.etlegacy.ETLegacy.desktop
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.etlegacy.ETLegacy.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.etlegacy.ETLegacy.metainfo.xml


%files
%license COPYING.txt
%doc README.md
%{_bindir}/etl*
%{_mandir}/man6/etl*.6*
# FIXME: Move to %%_libdir
%{_usr}/lib/%{name}
%{_datadir}/icons/hicolor/scalable/apps/etl*
%{_datadir}/applications/com.etlegacy.ETLegacy.desktop
%{_metainfodir}/com.etlegacy.ETLegacy.metainfo.xml
%{_datadir}/mime/packages/etlegacy.xml


%changelog
* Wed May 19 2021 Petr Menšík <pemensik@redhat.com> - 2.77.1-1
- Update to 2.77.1

* Mon Nov 02 2020 Petr Menšík <pemensik@redhat.com> - 2.76-2.20201102git886f0ef0
- Update to more recent commit

* Mon Oct 26 2020 Petr Menšík <pemensik@redhat.com>
- initial package build
