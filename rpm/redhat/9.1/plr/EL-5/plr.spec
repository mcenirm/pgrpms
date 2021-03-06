%global pginstdir	/usr/pgsql-9.1
%global pgmajorversion	91
%global sname	plr
Summary:	Procedural language interface between PostgreSQL and R
Name:		%{sname}%{pgmajorversion}
Version:	8.3.0.15
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://www.joeconway.com/%{sname}/%{sname}-%{version}.tar.gz
Patch0:		Makefile-pgxs.patch
URL:		http://www.joeconway.com/plr/
BuildRequires:	postgresql%{pgmajorversion}-devel R-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Procedural Language Handler for the "R software environment for 
statistical computing and graphics".

%prep
%setup -q -n %{sname}
%patch0 -p1

%build
make USE_PGXS=1 %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make USE_PGXS=1 DESTDIR=%{buildroot}/ install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig 
%postun -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
%{_docdir}/pgsql/extension/README.plr

%changelog
* Sat Dec 28 2013 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-15-1
- Update to 8.3.0.15

* Mon Mar 25 2013 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-14-1
- Update to 8.3.0.14

* Tue Sep 11 2012 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-13-1
- Update to 8.3.0.13

* Fri Oct 8 2010 - Devrim GUNDUZ <devrim@gunduz.org> 8.3.0-11-1
- Initial packaging for 9.0, which also suits new PostgreSQL RPM layout.
