%global pgmajorversion 90
%global pginstdir /usr/pgsql-9.0
%global sname	pgadmin3

Summary:	Graphical client for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	1.14.2
Release:	2%{?dist}
License:	BSD
Group:		Applications/Databases
Source:		ftp://ftp.postgresql.org/pub/pgadmin3/release/v%{version}/src/%{sname}-%{version}.tar.gz
Patch2:		%{sname}-desktop.patch
URL:		http://www.pgadmin.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	wxGTK-devel postgresql%{pgmajorversion}-devel desktop-file-utils openssl-devel libxml2-devel libxslt-devel
Requires:	wxGTK
Requires(post):	%{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

%description
pgAdmin III is a powerful administration and development
platform for the PostgreSQL database, free for any use.
It is designed to answer the needs of all users,
from writing simple SQL queries to developing complex
databases. The graphical interface supports all PostgreSQL
features and makes administration easy.

pgAdmin III is designed to answer the needs of all users, 
from writing simple SQL queries to developing complex databases. 
The graphical interface supports all PostgreSQL features and 
makes administration easy. The application also includes a syntax 
highlighting SQL editor, a server-side code editor, an 
SQL/batch/shell job scheduling agent, support for the Slony-I 
replication engine and much more. No additional drivers are 
required to communicate with the database server.

%package docs
Summary:	Documentation for pgAdmin3
Group:		Applications/Databases
Requires:	%{sname}_%{pgmajorversion} = %{version}

%description docs
This package contains documentation for various languages,
which are in html format.

%prep
%setup -q -n %{sname}-%{version}

# touch to avoid autotools re-run
for f in configure{,.ac} ; do touch -r $f $f.stamp ; done
%patch2 -p0
for f in configure{,.ac} ; do touch -r $f.stamp $f ; done

%build
export LIBS="-lwx_gtk2u_core-2.8"
./configure --disable-debug --disable-dependency-tracking --with-wx-version=2.8 --with-wx=/usr --with-pgsql=%{pginstdir} --prefix=%{pginstdir}
make %{?_smp_mflags} all

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_datadir}/%{name}/
cp -f ./pkg/debian/pgadmin3.xpm %{buildroot}/%{_datadir}/%{name}/%{name}.xpm

mkdir -p %{buildroot}/%{_datadir}/applications

mv ./pkg/%{sname}.desktop ./pkg/%{name}.desktop
desktop-file-install --vendor fedora --dir %{buildroot}/%{_datadir}/applications \
	--add-category X-Fedora\
	--add-category Application\
	--add-category Development\
	./pkg/%{name}.desktop

%clean
rm -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install /usr/bin/%{sname} pgadmin3 %{pginstdir}/bin/%{sname} 900

%preun
%{_sbindir}/update-alternatives --remove pgadmin3 %{pginstdir}/bin/%{sname}

%files
%defattr(-, root, root)
%doc BUGS CHANGELOG LICENSE README
%{pginstdir}/*
%{pginstdir}/share/%{sname}
%{_datadir}/%{name}
%{_datadir}/applications/*

%files docs
%defattr(-,root,root)
%doc docs/*

%changelog
* Wed Jan 23 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.2-2
- Fix %%post and %%postin issues.

* Sun Feb 26 2012 Devrim GUNDUZ <devrim@gunduz.org> 1.14.2-1
- Update to 1.14.2

* Thu Dec 15 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.1-2
-  Re-re-re-fix paths in desktop file path, per Magnus.

* Sun Dec 4 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.14.1-1
- Update to 1.14.1     

* Tue Nov 15 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.0-3
-  Fix paths in desktop file paths, per Stephen Blake. Also bump up the
  alternatives version..

* Mon Oct 31 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 1.14.0-2
-  Fix desktop file. Patch from Kim Bisgaard.

* Fri Sep 9 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.14.0-1
- Update to 1.14.0 Gold

* Fri Apr 15 2011 Devrim GUNDUZ <devrim@gunduz.org> 1.12.3-1
- Update to 1.12.3

* Tue Dec 14 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.2-2
- Update to 1.12.2

* Thu Oct 7 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.1-1
- Update to 1.12.1

* Mon Sep 20 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.12.0-1
- Update to 1.12.0
- Apply multiple postmaster specific changes and patch.
- Trim changelog.

* Tue Mar 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 1.10.2-1
- Update to 1.10.2
- Improve configure line to support new multiple postmaster installation
  feature.

* Sat Dec 5 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.1-1
- Update to 1.10.1

* Mon Jun 29 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0
- Update to 1.10.0 Gold

* Wed Mar 25 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta2
- Update to 1.10.0 beta2

* Fri Mar 13 2009 Devrim GUNDUZ <devrim@gunduz.org> 1.10.0-beta1
- Update to 1.10.0 beta1
- Update patch0

* Tue Jul 15 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-2
- Use $RPM_OPT_FLAGS, build with dependency tracking disabled 
(#229054). Patch from Ville Skyttä

* Thu Jun 5 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.4-1
- Update to 1.8.4

* Tue Jun 3 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.3-1
- Update to 1.8.3

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.2-1
- Update to 1.8.2

* Fri Jan 4 2008 Devrim GUNDUZ <devrim@gunduz.org> 1.8.1-1
- Update to 1.8.1

* Wed Dec 05 2007 Devrim GUNDUZ <devrim@gunduz.org> 1.8.0-2
- Rebuild for openssl bump

