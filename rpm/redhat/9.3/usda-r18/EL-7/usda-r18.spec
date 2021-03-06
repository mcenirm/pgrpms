Summary:	The USDA Food Database Sample for PostgreSQL
Name:		usda-r18
Version:	1.0
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
URL:		http://pgfoundry.org/projects/dbsamples
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:	http://pgfoundry.org/frs/download.php/555/%{name}-%{version}.tar.gz

Requires:	postgresql91
Buildarch:	noarch

%global		_usdadir  %{_datadir}/%{name}

%description
The USDA Food Database is published by the US Department of Agriculture.

%prep
%setup -q -n %{name}-%{version}

%build

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_usdadir}
install -m 644 -p *.sql %{buildroot}%{_usdadir}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc README
%dir %{_usdadir}
%attr(644,root,root) %{_usdadir}/*.sql

%changelog
* Fri Jan 7 2011 Devrim Gunduz <devrim@gunduz.org> 1.0-2
- Require PostgreSQL 9.1, not versionless one.

* Sat Feb 2 2008 Devrim Gunduz <devrim@gunduz.org> 1.0-1
- Initial packaging for Fedora/EPEL
