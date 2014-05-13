Name:		pgdg-sl94
Version:	9.4
Release:	1
Summary:	PostgreSQL 9.4.X PGDG RPMs for Scientific Linux - Yum Repository Configuration
Group:		System Environment/Base 
License:	BSD
URL:		http://yum.postgresql.org
Source0:	http://yum.postgresql.org/RPM-GPG-KEY-PGDG-94
Source2:	pgdg-94-sl.repo
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
Requires:	sl-release

%description
This package contains yum configuration for RHEL, and also the GPG
key for PGDG RPMs.

%prep
%setup -q  -c -T

%build

%install
rm -rf %{buildroot}

install -Dpm 644 %{SOURCE0} \
	%{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-94

install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE2}  \
	%{buildroot}%{_sysconfdir}/yum.repos.d/

%clean
rm -rf %{buildroot}

%post 
/bin/rpm --import %{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-PGDG-94

%files
%defattr(-,root,root,-)
%config %{_sysconfdir}/yum.repos.d/*
%dir %{_sysconfdir}/pki/rpm-gpg
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Thu May 8 2014 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.4-1
- 9.4 set

* Sun Apr 21 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.3-1 
- 9.3 set

* Sun Sep 23 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2-8
- Fix name of the GPG key file, per report from Rafael Martinez.

* Sat May 19 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2-7
- Fix repo name.

* Fri Sep 23 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2-6
- Change the package name, and add PostgreSQL major version number.
  This will let us install the repo RPMs easier. Also, rename RPM key,
  so that --import won't throw any errors.
- Own %%{_sysconfdir}/pki/rpm-gpg
- Trim changelog

* Mon Aug 22 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.2-5
- Now use http://yum.postgresql.org as the new repo URL.
