%define __cmake_in_source_build 1

Name:           etlegacy
Version:        2.76 
Release:        1%{?dist}
Summary:        Fully compatible client and server for the popular online FPS game Wolfenstein: Enemy Territory 

License:        GPLv3
URL:            https://www.etlegacy.com/
Source0:        https://github.com/etlegacy/etlegacy/archive/v%{version}/%{name}-%{version}.tar.gz
#Source1:        https://mirror.etlegacy.com/wolfadmin/wolfadmin.tar.gz

BuildRequires:  gcc gcc-c++
BuildRequires:  cmake
BuildRequires:  libpng-devel freetype-devel SDL2-devel curl-devel openssl-devel sqlite-devel
BuildRequires:  libtheora-devel libogg-devel libvorbis-devel libjpeg-turbo-devel
BuildRequires:  glew-devel
BuildRequires:  lua-devel
BuildRequires:  openal-soft-devel minizip-devel
#Requires:       

%description
Welcome to ET: Legacy, an open source project that aims to create a fully compatible client and server
for the popular online FPS game Wolfenstein: Enemy Territory - whose gameplay is still considered unmatched by many,
despite its great age. 

%prep
%autosetup


%build
%cmake -DBUNDLED_LIBS=OFF -DCROSS_COMPILE32=OFF \
	-DBUILD_MOD=OFF -DFEATURE_RENDERER2=OFF
%make_build


%install
%make_install


%files
%license COPYING.txt
%doc README.md



%changelog
* Mon Oct 26 2020 Petr Menšík <pemensik@redhat.com>
- 
