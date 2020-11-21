%if !0%{?fedora} || 0%{?fedora} < 33
%define buildfull 1
%endif

Summary: S2 Geometry Library
Name: s2geometry
Version: 0.9.0+git1
Release: 1%{?dist}
License: Apache License 2.0
Group: Libraries/Geosciences
URL: s2geometry.io

Source: %{name}-%{version}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gcc-c++ cmake
BuildRequires: openssl-devel
BuildRequires: gtest-devel

%description
S2 library represents all data on a three-dimensional
sphere (similar to a globe). This makes it possible to build a
worldwide geographic database with no seams or singularities, using a
single coordinate system, and with low distortion everywhere compared
to the true shape of the Earth.

%package devel
Summary: s2geometry development headers
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: openssl-devel

%description devel
This package provides headers for development

%prep
%setup -q -n %{name}-%{version}

%build

%if 0%{?buildfull}
mkdir build || true
cd build
%cmake -DCMAKE_VERBOSE_MAKEFILE=ON -DBUILD_PYTHON=OFF -DBUILD_TESTING=OFF \
       -DBUILD_SHARED_LIBS=ON -DBUILD_EXAMPLES=OFF \
       ..
%{__make} %{?_smp_mflags}
%else
%cmake -DCMAKE_VERBOSE_MAKEFILE=ON -DBUILD_PYTHON=OFF -DBUILD_TESTING=OFF \
       -DBUILD_SHARED_LIBS=ON -DBUILD_EXAMPLES=OFF
%{cmake_build}
%endif

%install
%{__rm} -rf %{buildroot}

%if 0%{?buildfull}
cd build
DESTDIR=%{buildroot} cmake --build . --target install
%else
%{cmake_install}
%endif

%pre

%post -n s2geometry -p /sbin/ldconfig

%postun -n s2geometry -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_libdir}/libs2.so

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/s2

%changelog
* Sun Nov 15 2020 rinigus <rinigus.git@gmail.com> - 0.9.0-1
- initial packaging release for SFOS
