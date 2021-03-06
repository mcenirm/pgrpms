%global pgmajorversion 96
%global pginstdir /usr/pgsql-9.6
%global sname ldap_fdw

Summary:	LDAP Data Wrapper for PostgreSQL
Name:		%{sname}%{pgmajorversion}
Version:	0.1.1
Release:	1%{?dist}
License:	BSD
Group:		Applications/Databases
Source0:	http://api.pgxn.org/dist/%{sname}/%{version}/%{sname}-%{version}.zip
Patch0:		%{sname}-makefile-pgxs.patch
URL:		http://pgxn.org/dist/ldap_fdw/
BuildRequires:	postgresql%{pgmajorversion}-devel, curl-devel
Requires:	postgresql%{pgmajorversion}-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This is an initial working on a PostgreSQL's Foreign Data Wrapper (FDW) to
query LDAP servers.

%prep
%setup -q -n %{sname}-%{version}
%patch0 -p0

%build
%{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}

%{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

# Install README file under PostgreSQL installation directory:
install -d %{buildroot}%{pginstdir}/share/extension
install -m 755 README.md %{buildroot}%{pginstdir}/share/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{_docdir}/pgsql/extension/README.md

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/share/extension/README-%{sname}.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}--%{version}.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Mon Mar 16 2015 - Devrim GUNDUZ <devrim@gunduz.org> 0.1.1-1
- Initial RPM packaging for PostgreSQL RPM Repository
