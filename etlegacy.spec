%define __cmake_in_source_build 1

# TODO: Current release does not work
# https://github.com/etlegacy/etlegacy/issues/1517
# Using master commit
#
# FIXME: debug information is not yet working

%global gitcommit 1ee8c7e848d6d8aa1f243b378888d5149952ee20
%global snapdate 20201026
%global snapinfo %{snapdate}git%(echo %{gitcommit}| cut -c 1-8)
#%%global gittag v%%{version}
%global gittag %{gitcommit}

Name:           etlegacy
Version:        2.76
# v2.76 tag has broken builds, snap has to be used from current master
Release:        1%{?snapinfo:.%{snapinfo}}%{?dist}
Summary:        Fully compatible client and server for the popular online FPS game Wolfenstein: Enemy Territory 

License:        GPLv3
URL:            https://www.etlegacy.com/
#Source0:        https://github.com/etlegacy/etlegacy/archive/v%%{version}/%%{name}-%%{version}.tar.gz
Source0:        https://github.com/etlegacy/etlegacy/archive/%{gittag}/%{name}-%{gittag}.tar.gz
#Source1:        https://mirror.etlegacy.com/wolfadmin/wolfadmin.tar.gz

Patch1:         etlegacy-2.76-description-install.patch

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
%autosetup -n %{name}-%{gittag} -p1

# Validation complains for mail address. I think this is error
# https://www.freedesktop.org/software/appstream/docs/chap-Metadata.html#tag-url
# mailto is explicitly mentioned.
sed -e 's|>\(mailto:\)\?mail@etlegacy.com</url>|>https://discord.gg/UBAZFys</url>|' -i misc/com.etlegacy.ETLegacy.metainfo.xml

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUNDLED_LIBS=OFF -DCROSS_COMPILE32=OFF \
       -DBUILD_MOD=OFF -DFEATURE_RENDERER2=OFF -DCMAKE_STRIP=/bin/true
%cmake_build


%install
%cmake_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.etlegacy.ETLegacy.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.etlegacy.ETLegacy.metainfo.xml


%files
%license COPYING.txt
%doc README.md
%{_bindir}/etl
%{_bindir}/etlded
%{_mandir}/man6/etl.6*
%{_mandir}/man6/etlded.6*
# FIXME: Move to %%_libdir
%{_usr}/lib/%{name}
%{_datadir}/icons/hicolor/scalable/apps/etl*
%{_datadir}/applications/com.etlegacy.ETLegacy.desktop
%{_metainfodir}/com.etlegacy.ETLegacy.metainfo.xml
%{_datadir}/mime/packages/etlegacy.xml


%changelog
* Mon Oct 26 2020 Petr Menšík <pemensik@redhat.com>
- initial package build
