Name:		plproxy
Version:	2.1
Release:	1%{?dist}
Summary:	PL/Proxy is database partitioning system implemented as PL language.
Group:		Applications/Databases
License:	BSD
URL:		http://pgfoundry.org/projects/plproxy/
Source0:	http://pgfoundry.org/frs/download.php/2665/%{name}-%{version}.tar.gz
Patch0:		%{name}-Makefile.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	postgresql-devel >= 8.1 flex >= 2.5.4, bison
Requires:	postgresql >= 8.1

%description
PL/Proxy is database partitioning system implemented as PL language.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
#make %{?_smp_mflags} install
install -d %{buildroot}%{_datadir}/%{name}-%{version}/
install -d %{buildroot}%{_libdir}/pgsql
install -m 644 plproxy.sql %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} -rp sql/ %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} -rp config/ %{buildroot}%{_datadir}/%{name}-%{version}/
%{__cp} libplproxy.so %{buildroot}%{_libdir}/pgsql/%{name}.so
%{__rm} -f %{buildroot}/%{_datadir}/pgsql/contrib/%{name}.sql

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README NEWS AUTHORS COPYRIGHT 
%{_datadir}/%{name}-%{version}/*
%{_libdir}/pgsql/%{name}.so*

%changelog
* Sat May 15 2010 - Devrim GUNDUZ <devrim@gunduz.org> 2.1-1
- Update to 2.1

* Wed Oct 28 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.9-1
- Update to 2.0.9

* Mon Feb 2 2009 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.8-1
- Update to 2.0.8
- Add a patch for EL-4, so that we can get rid of make problem.

* Tue Oct 7 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.7-1
- Update to 2.0.7

* Sat Sep 20 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.6-1
- Update to 2.0.6

* Sun Jun 15 2008 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.5-1
- Update to 2.0.5
- Remove scanner.c and scanner.h, they are no longer needed.

* Tue Aug 28 2007 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.2-2
- Add pre-generated scanner.c and scanner.h as sources. Only very
recent versions of flex can compile plproxy.

* Tue Aug 28 2007 - Devrim GUNDUZ <devrim@gunduz.org> 2.0.2-1
- Initial build 
