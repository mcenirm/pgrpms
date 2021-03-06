%global pgmajorversion 94
%global pginstdir /usr/pgsql-9.4
%global sname geoip

Summary:	Geolocation using GeoIP for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.2.4
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/geoip/
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
This extension provides IP-based geolocation, i.e. you provide an IPv4 address
and the extension looks for info about country, city, GPS etc.

To operate, the extension needs data mapping IP addresses to the other info,
but these data are not part of the extension. A good free dataset is GeoLite
from MaxMind (available at www.maxmind.com).

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
make USE_PGXS=1 %{?_smp_mflags}

%install
rm -rf %{buildroot}

make  DESTDIR=%{buildroot} USE_PGXS=1 %{?_smp_mflags} install

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc README.md
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/uninstall_%{sname}.sql

%changelog
* Thu Sep 10 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.2.4-1
- Update to 0.2.4

* Wed Jan 21 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.2.3-1
- Initial packaging for PostgreSQL RPM Repository
