# Conventions for PostgreSQL Global Development Group RPM releases:

# Official PostgreSQL Development Group RPMS have a PGDG after the release number.
# Integer releases are stable -- 0.1.x releases are Pre-releases, and x.y are
# test releases.

# Pre-releases are those that are built from CVS snapshots or pre-release
# tarballs from postgresql.org.  Official beta releases are not
# considered pre-releases, nor are release candidates, as their beta or
# release candidate status is reflected in the version of the tarball. Pre-
# releases' versions do not change -- the pre-release tarball of 7.0.3, for
# example, has the same tarball version as the final official release of 7.0.3:
# but the tarball is different.

# Test releases are where PostgreSQL itself is not in beta, but certain parts of
# the RPM packaging (such as the spec file, the initscript, etc) are in beta.

# Pre-release RPM's should not be put up on the public ftp.postgresql.org server
# -- only test releases or full releases should be.
# This is the PostgreSQL Global Development Group Official RPMset spec file,
# or a derivative thereof.
# Copyright 2003-2011 Devrim GÜNDÜZ <devrim@gunduz.org>
# and others listed.

# Major Contributors:
# ---------------
# Lamar Owen
# Tom Lane
# Peter Eisentraut
# Alvaro Herrera
# David Fetter
# Greg Smith
# and others in the Changelog....

# This spec file and ancilliary files are licensed in accordance with
# The PostgreSQL license.

# In this file you can find the default build package list macros.  These can be overridden by defining
# on the rpm command line:
# rpm --define 'packagename 1' .... to force the package to build.
# rpm --define 'packagename 0' .... to force the package NOT to build.
# The base package, the lib package, the devel package, and the server package always get built.

%define beta 0
%{?beta:%define __os_install_post /usr/lib/rpm/brp-compress}

%{!?kerbdir:%define kerbdir "/usr"}

# This is a macro to be used with find_lang and other stuff
%define majorversion 9.0
%define	pgbaseinstdir	/usr/pgsql-%{majorversion}
%define packageversion 90
%define oname postgresql

%{!?test:%define test 1}
%{!?plpython:%define plpython 1}
%{!?pltcl:%define pltcl 1}
%{!?plperl:%define plperl 1}
%{!?ssl:%define ssl 1}
%{!?intdatetimes:%define intdatetimes 1}
%{!?kerberos:%define kerberos 1}
%{!?nls:%define nls 1}
%{!?xml:%define xml 1}
%{!?pam:%define pam 1}
%{!?disablepgfts:%define disablepgfts 0}
%{!?runselftest:%define runselftest 0}
%{!?uuid:%define uuid 1}
%{!?ldap:%define ldap 1}

Summary:	PostgreSQL client programs and libraries
Name:		%{oname}%{packageversion}
Version:	9.0.23
Release:	1PGDG%{?dist}
License:	BSD
Group:		Applications/Databases
Url:		http://www.postgresql.org/

Source0:	ftp://ftp.postgresql.org/pub/source/v%{version}/%{oname}-%{version}.tar.bz2
Source3:	postgresql.init
Source4:	Makefile.regress
Source5:	pg_config.h
Source6:	README.rpm-dist
Source7:	ecpg_config.h
Source9:	postgresql-9.0-libs.conf
Source12:	http://www.postgresql.org/files/documentation/pdf/%{majorversion}/%{oname}-%{majorversion}-A4.pdf
Source14:	postgresql.pam
Source16:	filter-requires-perl-Pg.sh

Patch1:		rpm-pgsql.patch
Patch3:		postgresql-logging.patch
Patch6:		postgresql-perl-rpath.patch
Patch8:		postgresql-prefer-ncurses.patch

BuildRequires:	perl glibc-devel bison flex
Requires:	/sbin/ldconfig initscripts

%if %plpython
BuildRequires:	python-devel
%endif

%if %pltcl
BuildRequires:	tcl-devel
%endif

BuildRequires:	readline-devel
BuildRequires:	zlib-devel >= 1.0.4

%if %ssl
BuildRequires:	openssl-devel
%endif

%if %kerberos
BuildRequires:	krb5-devel
BuildRequires:	e2fsprogs-devel
%endif

%if %nls
BuildRequires:	gettext >= 0.10.35
%endif

%if %xml
BuildRequires:	libxml2-devel libxslt-devel
%endif

%if %pam
BuildRequires:	pam-devel
%endif

%if %uuid
BuildRequires:	uuid-devel
%endif

%if %ldap
BuildRequires:	openldap-devel
%endif

# These are required for -docs subpackage:

BuildRequires:	openjade
BuildRequires:	opensp
BuildRequires:	docbook-dtds
BuildRequires:	docbook-style-dsssl
BuildRequires:	libxslt

Requires:	%{name}-libs = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun):	%{_sbindir}/update-alternatives

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:	postgresql

%description
PostgreSQL is an advanced Object-Relational database management system
(DBMS) that supports almost all SQL constructs (including
transactions, subselects and user-defined types and functions). The
postgresql package includes the client programs and libraries that
you'll need to access a PostgreSQL DBMS server.  These PostgreSQL
client programs are programs that directly manipulate the internal
structure of PostgreSQL databases on a PostgreSQL server. These client
programs can be located on the same machine with the PostgreSQL
server, or may be on a remote machine which accesses a PostgreSQL
server over a network connection. This package contains the command-line
utilities for managing PostgreSQL databases on a PostgreSQL server.

If you want to manipulate a PostgreSQL database on a local or remote PostgreSQL
server, you need this package. You also need to install this package
if you're installing the postgresql90-server package.

%package libs
Summary:	The shared libraries required for any PostgreSQL clients
Group:		Applications/Databases
Provides:	libpq.so
Provides:	postgresql-libs

%description libs
The postgresql90-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package server
Summary:	The programs needed to create and run a PostgreSQL server
Group:		Applications/Databases
Requires:	/usr/sbin/useradd /sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Provides:	postgresql-server

%description server
The postgresql90-server package includes the programs needed to create
and run a PostgreSQL server, which will in turn allow you to create
and maintain PostgreSQL databases.  PostgreSQL is an advanced
Object-Relational database management system (DBMS) that supports
almost all SQL constructs (including transactions, subselects and
user-defined types and functions). You should install
postgresql90-server if you want to create and maintain your own
PostgreSQL databases and/or your own PostgreSQL server. You also need
to install the postgresql package.

%package docs
Summary:	Extra documentation for PostgreSQL
Group:		Applications/Databases
Provides:	postgresql-docs

%description docs
The postgresql90-docs package includes the SGML source for the documentation
as well as the documentation in PDF format and some extra documentation.
Install this package if you want to help with the PostgreSQL documentation
project, or if you want to generate printed documentation. This package also
includes HTML version of the documentation.

%package contrib
Summary:	Contributed source and binaries distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name} = %{version}
Provides:	postgresql-contrib

%description contrib
The postgresql90-contrib package contains contributed packages that are
included in the PostgreSQL distribution.

%package devel
Summary:	PostgreSQL development header files and libraries
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	postgresql-devel

%description devel
The postgresql90-devel package contains the header files and libraries
needed to compile C or C++ applications which will directly interact
with a PostgreSQL database management server and the ecpg Embedded C
Postgres preprocessor. You need to install this package if you want to
develop applications which will interact with a PostgreSQL server.

%if %plperl
%package plperl
Summary:	The Perl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server = %{version}-%{release}
%ifarch ppc ppc64
BuildRequires:  perl-devel
%endif
Obsoletes:	postgresql-pl
Provides:	postgresql-plperl

%description plperl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql90-plperl package contains the PL/Perl language
for the backend.
%endif

%if %plpython
%package plpython
Summary:	The Python procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	postgresql-pl
Provides:	postgresql-plpython

%description plpython
PostgreSQL is an advanced Object-Relational database management
system. The postgresql90-plpython package contains the PL/Python language
for the backend.
%endif

%if %pltcl
%package pltcl
Summary:	The Tcl procedural language for PostgreSQL
Group:		Applications/Databases
Requires:	%{name} = %{version}
Requires:	%{name}-server = %{version}
Obsoletes:	postgresql-pl
Provides:	postgresql-pltcl

%description pltcl
PostgreSQL is an advanced Object-Relational database management
system. The postgresql90-pltcl package contains the PL/Tcl language
for the backend.
%endif

%if %test
%package test
Summary:	The test suite distributed with PostgreSQL
Group:		Applications/Databases
Requires:	%{name}-server = %{version}-%{release}
Provides:	postgresql-test

%description test
PostgreSQL is an advanced Object-Relational database management
system. The postgresql-test package includes the sources and pre-built
binaries of various tests for the PostgreSQL database management
system, including regression tests and benchmarks.
%endif

%define __perl_requires %{SOURCE16}

%prep
%setup -q -n %{oname}-%{version}
%patch1 -p1
%patch3 -p1
# patch5 is applied later
%patch6 -p1
%patch8 -p1

cp -p %{SOURCE12} .

%build

CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS
%if %kerberos
CPPFLAGS="${CPPFLAGS} -I%{_includedir}/et" ; export CPPFLAGS
CFLAGS="${CFLAGS} -I%{_includedir}/et" ; export CFLAGS
%endif

# Strip out -ffast-math from CFLAGS....
CFLAGS=`echo $CFLAGS|xargs -n 1|grep -v ffast-math|xargs -n 100`
# Add LINUX_OOM_ADJ=0 to ensure child processes reset postmaster's oom_adj
CFLAGS="$CFLAGS -DLINUX_OOM_ADJ=0"

export LIBNAME=%{_lib}
./configure --disable-rpath \
	--prefix=%{pgbaseinstdir} \
	--includedir=%{pgbaseinstdir}/include \
	--mandir=%{pgbaseinstdir}/share/man \
	--datadir=%{pgbaseinstdir}/share \
%if %beta
	--enable-debug \
	--enable-cassert \
%endif
%if %plperl
	--with-perl \
%endif
%if %plpython
	--with-python \
%endif
%if %pltcl
	--with-tcl \
	--with-tclconfig=%{_libdir} \
%endif
%if %ssl
	--with-openssl \
%endif
%if %pam
	--with-pam \
%endif
%if %kerberos
	--with-krb5 \
	--with-gssapi \
	--with-includes=%{kerbdir}/include \
	--with-libraries=%{kerbdir}/%{_lib} \
%endif
%if %nls
	--enable-nls \
%endif
%if !%intdatetimes
	--disable-integer-datetimes \
%endif
%if %disablepgfts
	--disable-thread-safety \
%endif
%if %uuid
	--with-ossp-uuid \
%endif
%if %xml
	--with-libxml \
	--with-libxslt \
%endif
%if %ldap
	--with-ldap \
%endif
	--with-system-tzdata=%{_datadir}/zoneinfo \
	--sysconfdir=/etc/sysconfig/pgsql \
	--docdir=%{_docdir}

make %{?_smp_mflags} all
make %{?_smp_mflags} -C contrib all
%if %uuid
make %{?_smp_mflags} -C contrib/uuid-ossp all
%endif

# Have to hack makefile to put correct path into tutorial scripts
sed "s|C=\`pwd\`;|C=%{pgbaseinstdir}/lib/tutorial;|" < src/tutorial/Makefile > src/tutorial/GNUmakefile
make %{?_smp_mflags} -C src/tutorial NO_PGXS=1 all
rm -f src/tutorial/GNUmakefile

%if %runselftest
	pushd src/test/regress
	make all
	cp ../../../contrib/spi/refint.so .
	cp ../../../contrib/spi/autoinc.so .
	make MAX_CONNECTIONS=5 check
	make clean
	popd
%endif

%if %test
	pushd src/test/regress
	make all
	popd
%endif

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install
make -C contrib DESTDIR=%{buildroot} install
%if %uuid
make -C contrib/uuid-ossp DESTDIR=%{buildroot} install
%endif

# multilib header hack; note pg_config.h is installed in two places!
# we only apply this to known Red Hat multilib arches, per bug #177564
case `uname -i` in
	i386 | x86_64 | ppc | ppc64 | s390 | s390x)
		mv %{buildroot}%{pgbaseinstdir}/include/pg_config.h %{buildroot}%{pgbaseinstdir}/include/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/
		mv %{buildroot}%{pgbaseinstdir}/include/server/pg_config.h %{buildroot}%{pgbaseinstdir}/include/server/pg_config_`uname -i`.h
		install -m 644 %{SOURCE5} %{buildroot}%{pgbaseinstdir}/include/server/
		mv %{buildroot}%{pgbaseinstdir}/include/ecpg_config.h %{buildroot}%{pgbaseinstdir}/include/ecpg_config_`uname -i`.h
		install -m 644 %{SOURCE7} %{buildroot}%{pgbaseinstdir}/include/
		;;
	*)
	;;
esac

install -d %{buildroot}/etc/rc.d/init.d
sed 's/^PGVERSION=.*$/PGVERSION=%{version}/' <%{SOURCE3} > postgresql.init
install -m 755 postgresql.init %{buildroot}/etc/rc.d/init.d/postgresql-%{majorversion}

%if %pam
install -d %{buildroot}/etc/pam.d
install -m 644 %{SOURCE14} %{buildroot}/etc/pam.d/postgresql%{packageversion}
%endif

# PGDATA needs removal of group and world permissions due to pg_pwd hole.
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/data

# backups of data go here...
install -d -m 700 %{buildroot}/var/lib/pgsql/%{majorversion}/backups

# Create the multiple postmaster startup directory
install -d -m 700 %{buildroot}/etc/sysconfig/pgsql/%{majorversion}

# Install linker conf file under postgresql installation directory.
# We will install the latest version via alternatives.
install -d -m 755 %{buildroot}%{pgbaseinstdir}/share/
install -m 700 %{SOURCE9} %{buildroot}%{pgbaseinstdir}/share/

%if %test
	# tests. There are many files included here that are unnecessary,
	# but include them anyway for completeness.  We replace the original
	# Makefiles, however.
	mkdir -p %{buildroot}%{pgbaseinstdir}/lib/test
	cp -a src/test/regress %{buildroot}%{pgbaseinstdir}/lib/test
	install -m 0755 contrib/spi/refint.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	install -m 0755 contrib/spi/autoinc.so %{buildroot}%{pgbaseinstdir}/lib/test/regress
	pushd  %{buildroot}%{pgbaseinstdir}/lib/test/regress
	strip *.so
	rm -f GNUmakefile Makefile *.o
	popd
	cp %{SOURCE4} %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
	chmod 0644 %{buildroot}%{pgbaseinstdir}/lib/test/regress/Makefile
%endif

# Fix some more documentation
# gzip doc/internals.ps
cp %{SOURCE6} README.rpm-dist
mkdir -p %{buildroot}%{pgbaseinstdir}/share/doc/html
mv doc/src/sgml/html doc
mkdir -p %{buildroot}%{pgbaseinstdir}/share/man/
mv doc/src/sgml/man1 doc/src/sgml/man3 doc/src/sgml/man7  %{buildroot}%{pgbaseinstdir}/share/man/
rm -rf %{buildroot}%{_docdir}/pgsql

# initialize file lists
cp /dev/null main.lst
cp /dev/null libs.lst
cp /dev/null server.lst
cp /dev/null devel.lst
cp /dev/null plperl.lst
cp /dev/null pltcl.lst
cp /dev/null plpython.lst

%if %nls
%find_lang ecpg-%{majorversion}
%find_lang ecpglib6-%{majorversion}
%find_lang initdb-%{majorversion}
%find_lang libpq5-%{majorversion}
%find_lang pg_config-%{majorversion}
%find_lang pg_controldata-%{majorversion}
%find_lang pg_ctl-%{majorversion}
%find_lang pg_dump-%{majorversion}
%find_lang pg_resetxlog-%{majorversion}
%find_lang pgscripts-%{majorversion}
%if %plperl
%find_lang plperl-%{majorversion}
cat plperl-%{majorversion}.lang > pg_plperl.lst
%endif
%find_lang plpgsql-%{majorversion}
%if %plpython
%find_lang plpython-%{majorversion}
cat plpython-%{majorversion}.lang > pg_plpython.lst
%endif
%if %pltcl
%find_lang pltcl-%{majorversion}
cat pltcl-%{majorversion}.lang > pg_pltcl.lst
%endif
%find_lang postgres-%{majorversion}
%find_lang psql-%{majorversion}
%endif

cat libpq5-%{majorversion}.lang > pg_libpq5.lst
cat pg_config-%{majorversion}.lang ecpg-%{majorversion}.lang ecpglib6-%{majorversion}.lang > pg_devel.lst
cat initdb-%{majorversion}.lang pg_ctl-%{majorversion}.lang psql-%{majorversion}.lang pg_dump-%{majorversion}.lang pgscripts-%{majorversion}.lang > pg_main.lst
cat postgres-%{majorversion}.lang pg_resetxlog-%{majorversion}.lang pg_controldata-%{majorversion}.lang plpgsql-%{majorversion}.lang > pg_server.lst

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%pre server
groupadd -g 26 -o -r postgres >/dev/null 2>&1 || :
useradd -M -n -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
	-c "PostgreSQL Server" -u 26 postgres >/dev/null 2>&1 || :

%post server
chkconfig --add postgresql-9.0
/sbin/ldconfig
# postgres' .bash_profile.
# We now don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
# so that package manager will be happy during upgrade to new major version.
echo "[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/%{majorversion}/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile" >  /var/lib/pgsql/.bash_profile
chown postgres: /var/lib/pgsql/.bash_profile
chmod 700 /var/lib/pgsql/.bash_profile

%preun server
if [ $1 = 0 ] ; then
	/sbin/service postgresql-9.0 condstop >/dev/null 2>&1
	chkconfig --del postgresql-9.0
fi

%postun server
/sbin/ldconfig
if [ $1 -ge 1 ]; then
  /sbin/service postgresql-9.0 condrestart >/dev/null 2>&1
fi

%if %plperl
%post 	-p /sbin/ldconfig	plperl
%postun	-p /sbin/ldconfig 	plperl
%endif

%if %plpython
%post 	-p /sbin/ldconfig	plpython
%postun	-p /sbin/ldconfig 	plpython
%endif

%if %pltcl
%post 	-p /sbin/ldconfig	pltcl
%postun	-p /sbin/ldconfig 	pltcl
%endif

%if %test
%post test
chown -R postgres:postgres /usr/share/pgsql/test >/dev/null 2>&1 || :
%endif

# Create alternatives entries for common binaries and man files
%post
%{_sbindir}/update-alternatives --install /usr/bin/psql pgsql-psql %{pgbaseinstdir}/bin/psql 900
%{_sbindir}/update-alternatives --install /usr/bin/clusterdb  pgsql-clusterdb  %{pgbaseinstdir}/bin/clusterdb 900
%{_sbindir}/update-alternatives --install /usr/bin/createdb   pgsql-createdb   %{pgbaseinstdir}/bin/createdb 900
%{_sbindir}/update-alternatives --install /usr/bin/createlang pgsql-createlang %{pgbaseinstdir}/bin/createlang 900
%{_sbindir}/update-alternatives --install /usr/bin/createuser pgsql-createuser %{pgbaseinstdir}/bin/createuser 900
%{_sbindir}/update-alternatives --install /usr/bin/dropdb     pgsql-dropdb     %{pgbaseinstdir}/bin/dropdb 900
%{_sbindir}/update-alternatives --install /usr/bin/droplang   pgsql-droplang   %{pgbaseinstdir}/bin/droplang 900
%{_sbindir}/update-alternatives --install /usr/bin/dropuser   pgsql-dropuser   %{pgbaseinstdir}/bin/dropuser 900
%{_sbindir}/update-alternatives --install /usr/bin/pg_dump    pgsql-pg_dump    %{pgbaseinstdir}/bin/pg_dump 900
%{_sbindir}/update-alternatives --install /usr/bin/pg_dumpall pgsql-pg_dumpall %{pgbaseinstdir}/bin/pg_dumpall 900
%{_sbindir}/update-alternatives --install /usr/bin/pg_restore pgsql-pg_restore %{pgbaseinstdir}/bin/pg_restore 900
%{_sbindir}/update-alternatives --install /usr/bin/reindexdb  pgsql-reindexdb  %{pgbaseinstdir}/bin/reindexdb 900
%{_sbindir}/update-alternatives --install /usr/bin/vacuumdb   pgsql-vacuumdb   %{pgbaseinstdir}/bin/vacuumdb 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/clusterdb.1  pgsql-clusterdbman     %{pgbaseinstdir}/share/man/man1/clusterdb.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createdb.1   pgsql-createdbman	  %{pgbaseinstdir}/share/man/man1/createdb.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createlang.1 pgsql-createlangman    %{pgbaseinstdir}/share/man/man1/createlang.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/createuser.1 pgsql-createuserman    %{pgbaseinstdir}/share/man/man1/createuser.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropdb.1     pgsql-dropdbman        %{pgbaseinstdir}/share/man/man1/dropdb.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/droplang.1   pgsql-droplangman	  %{pgbaseinstdir}/share/man/man1/droplang.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/dropuser.1   pgsql-dropuserman	  %{pgbaseinstdir}/share/man/man1/dropuser.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dump.1    pgsql-pg_dumpman	  %{pgbaseinstdir}/share/man/man1/pg_dump.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_dumpall.1 pgsql-pg_dumpallman    %{pgbaseinstdir}/share/man/man1/pg_dumpall.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/pg_restore.1 pgsql-pg_restoreman    %{pgbaseinstdir}/share/man/man1/pg_restore.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/psql.1	   pgsql-psqlman          %{pgbaseinstdir}/share/man/man1/psql.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/reindexdb.1  pgsql-reindexdbman     %{pgbaseinstdir}/share/man/man1/reindexdb.1 900
%{_sbindir}/update-alternatives --install /usr/share/man/man1/vacuumdb.1   pgsql-vacuumdbman	  %{pgbaseinstdir}/share/man/man1/vacuumdb.1 900
%{_sbindir}/update-alternatives --install /etc/ld.so.conf.d/postgresql-pgdg-libs.conf   pgsql-ld-conf        %{pgbaseinstdir}/share/postgresql-9.0-libs.conf 900

# Drop alternatives entries for common binaries and man files
if [ "$1" -eq 0 ]
  then
	# Only remove these links if the package is completely removed from the system (vs.just being upgraded)
	%{_sbindir}/update-alternatives --remove pgsql-psql		  %{pgbaseinstdir}/bin/psql
	%{_sbindir}/update-alternatives --remove pgsql-clusterdb 	  %{pgbaseinstdir}/bin/clusterdb
	%{_sbindir}/update-alternatives --remove pgsql-clusterdbman	  %{pgbaseinstdir}/share/man/man1/clusterdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createdb		  %{pgbaseinstdir}/bin/createdb
	%{_sbindir}/update-alternatives --remove pgsql-createdbman	  %{pgbaseinstdir}/share/man/man1/createdb.1
	%{_sbindir}/update-alternatives --remove pgsql-createlang 	  %{pgbaseinstdir}/bin/createlang
	%{_sbindir}/update-alternatives --remove pgsql-createlangman	  %{pgbaseinstdir}/share/man/man1/createlang.1
	%{_sbindir}/update-alternatives --remove pgsql-createuser	  %{pgbaseinstdir}/bin/createuser
	%{_sbindir}/update-alternatives --remove pgsql-createuserman 	  %{pgbaseinstdir}/share/man/man1/createuser.1
	%{_sbindir}/update-alternatives --remove pgsql-dropdb		  %{pgbaseinstdir}/bin/dropdb
	%{_sbindir}/update-alternatives --remove pgsql-dropdbman	  %{pgbaseinstdir}/share/man/man1/dropdb.1
	%{_sbindir}/update-alternatives --remove pgsql-droplang		  %{pgbaseinstdir}/bin/droplang
	%{_sbindir}/update-alternatives --remove pgsql-droplangman	  %{pgbaseinstdir}/share/man/man1/droplang.1
	%{_sbindir}/update-alternatives --remove pgsql-dropuser		  %{pgbaseinstdir}/bin/dropuser
	%{_sbindir}/update-alternatives --remove pgsql-dropuserman	  %{pgbaseinstdir}/share/man/man1/dropuser.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dump		  %{pgbaseinstdir}/bin/pg_dump
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpall	  %{pgbaseinstdir}/bin/pg_dumpall
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpallman	  %{pgbaseinstdir}/share/man/man1/pg_dumpall.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_dumpman	  %{pgbaseinstdir}/share/man/man1/pg_dump.1
	%{_sbindir}/update-alternatives --remove pgsql-pg_restore	  %{pgbaseinstdir}/bin/pg_restore
	%{_sbindir}/update-alternatives --remove pgsql-pg_restoreman 	  %{pgbaseinstdir}/share/man/man1/pg_restore.1
	%{_sbindir}/update-alternatives --remove pgsql-psqlman		  %{pgbaseinstdir}/share/man/man1/psql.1
	%{_sbindir}/update-alternatives --remove pgsql-reindexdb 	  %{pgbaseinstdir}/bin/reindexdb
	%{_sbindir}/update-alternatives --remove pgsql-reindexdbman	  %{pgbaseinstdir}/share/man/man1/reindexdb.1
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdb		  %{pgbaseinstdir}/bin/vacuumdb
	%{_sbindir}/update-alternatives --remove pgsql-vacuumdbman	  %{pgbaseinstdir}/share/man/man1/vacuumdb.1
	%{_sbindir}/update-alternatives --remove pgsql-ld-conf		  %{pgbaseinstdir}/share/postgresql-9.0-libs.conf
fi

%clean
rm -rf %{buildroot}

# FILES section.

%files -f pg_main.lst
%defattr(-,root,root)
%doc doc/KNOWN_BUGS doc/MISSING_FEATURES doc/README*
%doc COPYRIGHT README doc/bug.template
%doc README.rpm-dist
%{pgbaseinstdir}/bin/clusterdb
%{pgbaseinstdir}/bin/createdb
%{pgbaseinstdir}/bin/createlang
%{pgbaseinstdir}/bin/createuser
%{pgbaseinstdir}/bin/dropdb
%{pgbaseinstdir}/bin/droplang
%{pgbaseinstdir}/bin/dropuser
%{pgbaseinstdir}/bin/pg_dump
%{pgbaseinstdir}/bin/pg_dumpall
%{pgbaseinstdir}/bin/pg_restore
%{pgbaseinstdir}/bin/psql
%{pgbaseinstdir}/bin/reindexdb
%{pgbaseinstdir}/bin/vacuumdb
%{pgbaseinstdir}/share/man/man1/clusterdb.*
%{pgbaseinstdir}/share/man/man1/createdb.*
%{pgbaseinstdir}/share/man/man1/createlang.*
%{pgbaseinstdir}/share/man/man1/createuser.*
%{pgbaseinstdir}/share/man/man1/dropdb.*
%{pgbaseinstdir}/share/man/man1/droplang.*
%{pgbaseinstdir}/share/man/man1/dropuser.*
%{pgbaseinstdir}/share/man/man1/pg_dump.*
%{pgbaseinstdir}/share/man/man1/pg_dumpall.*
%{pgbaseinstdir}/share/man/man1/pg_restore.*
%{pgbaseinstdir}/share/man/man1/psql.*
%{pgbaseinstdir}/share/man/man1/reindexdb.*
%{pgbaseinstdir}/share/man/man1/vacuumdb.*
%{pgbaseinstdir}/share/man/man3/*
%{pgbaseinstdir}/share/man/man7/*

%files docs
%defattr(-,root,root)
%doc doc/src/*
%doc *-A4.pdf
%doc src/tutorial
%doc doc/html

%files contrib
%defattr(-,root,root)
%{pgbaseinstdir}/lib/_int.so
%{pgbaseinstdir}/lib/adminpack.so
%{pgbaseinstdir}/lib/autoinc.so
%{pgbaseinstdir}/lib/auto_explain.so
%{pgbaseinstdir}/lib/btree_gin.so
%{pgbaseinstdir}/lib/btree_gist.so
%{pgbaseinstdir}/lib/chkpass.so
%{pgbaseinstdir}/lib/citext.so
%{pgbaseinstdir}/lib/cube.so
%{pgbaseinstdir}/lib/dblink.so
%{pgbaseinstdir}/lib/earthdistance.so
%{pgbaseinstdir}/lib/fuzzystrmatch.so
%{pgbaseinstdir}/lib/insert_username.so
%{pgbaseinstdir}/lib/isn.so
%{pgbaseinstdir}/lib/hstore.so
%{pgbaseinstdir}/lib/passwordcheck.so
%{pgbaseinstdir}/lib/pg_freespacemap.so
%{pgbaseinstdir}/lib/pg_stat_statements.so
%{pgbaseinstdir}/lib/pgrowlocks.so
%if %ssl
%{pgbaseinstdir}/lib/sslinfo.so
%endif
%{pgbaseinstdir}/lib/lo.so
%{pgbaseinstdir}/lib/ltree.so
%{pgbaseinstdir}/lib/moddatetime.so
%{pgbaseinstdir}/lib/pageinspect.so
%{pgbaseinstdir}/lib/pgcrypto.so
%{pgbaseinstdir}/lib/pgstattuple.so
%{pgbaseinstdir}/lib/pg_buffercache.so
%{pgbaseinstdir}/lib/pg_trgm.so
%{pgbaseinstdir}/lib/pg_upgrade_support.so
%{pgbaseinstdir}/lib/refint.so
%{pgbaseinstdir}/lib/seg.so
%{pgbaseinstdir}/lib/tablefunc.so
%{pgbaseinstdir}/lib/timetravel.so
%{pgbaseinstdir}/lib/unaccent.so
%if %xml
%{pgbaseinstdir}/lib/pgxml.so
%endif
%if %uuid
%{pgbaseinstdir}/lib/uuid-ossp.so
%endif
%{pgbaseinstdir}/share/contrib/
%{pgbaseinstdir}/bin/oid2name
%{pgbaseinstdir}/bin/pgbench
%{pgbaseinstdir}/bin/vacuumlo
%{pgbaseinstdir}/bin/pg_archivecleanup
%{pgbaseinstdir}/bin/pg_standby
%{pgbaseinstdir}/bin/pg_upgrade

%files libs -f pg_libpq5.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/libpq.so.*
%{pgbaseinstdir}/lib/libecpg.so*
%{pgbaseinstdir}/lib/libpgtypes.so.*
%{pgbaseinstdir}/lib/libecpg_compat.so.*
%{pgbaseinstdir}/lib/libpqwalreceiver.so
%config(noreplace) %attr (644,root,root) %{pgbaseinstdir}/share/postgresql-9.0-libs.conf

%files server -f pg_server.lst
%defattr(-,root,root)
/etc/rc.d/init.d/postgresql-%{majorversion}
%if %pam
%config(noreplace) /etc/pam.d/postgresql%{packageversion}
%endif
%attr (755,root,root) %dir /etc/sysconfig/pgsql
%{pgbaseinstdir}/bin/initdb
%{pgbaseinstdir}/bin/pg_controldata
%{pgbaseinstdir}/bin/pg_ctl
%{pgbaseinstdir}/bin/pg_resetxlog
%{pgbaseinstdir}/bin/postgres
%{pgbaseinstdir}/bin/postmaster
%{pgbaseinstdir}/share/man/man1/initdb.*
%{pgbaseinstdir}/share/man/man1/pg_controldata.*
%{pgbaseinstdir}/share/man/man1/pg_ctl.*
%{pgbaseinstdir}/share/man/man1/pg_resetxlog.*
%{pgbaseinstdir}/share/man/man1/postgres.*
%{pgbaseinstdir}/share/man/man1/postmaster.*
%{pgbaseinstdir}/share/postgres.bki
%{pgbaseinstdir}/share/postgres.description
%{pgbaseinstdir}/share/postgres.shdescription
%{pgbaseinstdir}/share/system_views.sql
%{pgbaseinstdir}/share/*.sample
%{pgbaseinstdir}/share/timezonesets/*
%{pgbaseinstdir}/share/tsearch_data/*.affix
%{pgbaseinstdir}/share/tsearch_data/*.dict
%{pgbaseinstdir}/share/tsearch_data/*.ths
%{pgbaseinstdir}/share/tsearch_data/*.rules
%{pgbaseinstdir}/share/tsearch_data/*.stop
%{pgbaseinstdir}/share/tsearch_data/*.syn
%{pgbaseinstdir}/lib/dict_int.so
%{pgbaseinstdir}/lib/dict_snowball.so
%{pgbaseinstdir}/lib/dict_xsyn.so
%{pgbaseinstdir}/lib/euc2004_sjis2004.so
%{pgbaseinstdir}/lib/plpgsql.so
%{pgbaseinstdir}/lib/test_parser.so
%{pgbaseinstdir}/lib/tsearch2.so

%dir %{pgbaseinstdir}/lib
%dir %{pgbaseinstdir}/share
%attr(700,postgres,postgres) %dir /var/lib/pgsql
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/data
%attr(700,postgres,postgres) %dir /var/lib/pgsql/%{majorversion}/backups
%{pgbaseinstdir}/lib/*_and_*.so
%{pgbaseinstdir}/share/conversion_create.sql
%{pgbaseinstdir}/share/information_schema.sql
%{pgbaseinstdir}/share/snowball_create.sql
%{pgbaseinstdir}/share/sql_features.txt

%files devel -f pg_devel.lst
%defattr(-,root,root)
%{pgbaseinstdir}/include/*
%{pgbaseinstdir}/bin/ecpg
%{pgbaseinstdir}/bin/pg_config
%{pgbaseinstdir}/lib/libpq.so
%{pgbaseinstdir}/lib/libecpg.so
%{pgbaseinstdir}/lib/libpq.a
%{pgbaseinstdir}/lib/libecpg.a
%{pgbaseinstdir}/lib/libecpg_compat.so
%{pgbaseinstdir}/lib/libecpg_compat.a
%{pgbaseinstdir}/lib/libpgport.a
%{pgbaseinstdir}/lib/libpgtypes.so
%{pgbaseinstdir}/lib/libpgtypes.a
%{pgbaseinstdir}/lib/pgxs/*
%{pgbaseinstdir}/share/man/man1/ecpg.*
%{pgbaseinstdir}/share/man/man1/pg_config.*

%if %plperl
%files plperl -f pg_plperl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plperl.so
%endif

%if %pltcl
%files pltcl -f pg_pltcl.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/pltcl.so
%{pgbaseinstdir}/bin/pltcl_delmod
%{pgbaseinstdir}/bin/pltcl_listmod
%{pgbaseinstdir}/bin/pltcl_loadmod
%{pgbaseinstdir}/share/unknown.pltcl
%endif

%if %plpython
%files plpython -f pg_plpython.lst
%defattr(-,root,root)
%{pgbaseinstdir}/lib/plpython.so
%{pgbaseinstdir}/lib/plpython2.so
%endif

%if %test
%files test
%defattr(-,postgres,postgres)
%attr(-,postgres,postgres) %{pgbaseinstdir}/lib/test/*
%attr(-,postgres,postgres) %dir %{pgbaseinstdir}/lib/test
%endif

%changelog
* Tue Oct 6 2015 Jeff Frost <jeff@pgexperts.com> 9.0.23-1PGDG
- Update to 9.0.23, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-23.html

* Thu Jun 11 2015 Devrim GUNDUZ <devrim@gunduz.org> 9.0.22-1PGDG
- Update to 9.0.22, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-22.html

* Thu Jun 4 2015 Devrim GUNDUZ <devrim@gunduz.org> 9.0.21-1PGDG
- Update to 9.0.21, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-21.html

* Tue May 19 2015 Devrim GUNDUZ <devrim@gunduz.org> 9.0.20-1PGDG
- Update to 9.0.20, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-20.html

* Wed Feb 11 2015 Strahinja Kustudic <strahinjak@nordeus.com> - 9.0.19-2PGDG
- Remove obsolete /var/log/pgsql

* Tue Feb 3 2015 Devrim GUNDUZ <devrim@gunduz.org> 9.0.19-1PGDG
- Update to 9.0.19, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-19.html
- Improve .bash_profile, and let users specify their own
  environmental settings by sourcing an external file, called
  ~/.pgsql_profile. Per request from various users, and final
  suggestion from Martin Gudmundsson.

* Tue Jul 22 2014 Devrim GUNDUZ <devrim@gunduz.org> 9.0.18-1PGDG
- Update to 9.0.18, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-18.html

* Tue Feb 18 2014 Devrim GUNDUZ <devrim@gunduz.org> 9.0.17-1PGDG
- Update to 9.0.17, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-17.html
- Fix permissions of postgresql-90-libs.conf, per Christoph Berg.

* Tue Feb 18 2014 Jeff Frost <jeff@pgexperts.com> - 9.0.16-1PGDG
- Update to 9.0.16, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-16.html

* Wed Dec 04 2013 Devrim GUNDUZ <devrim@gunduz.org> 9.0.15-1PGDG
- Update to 9.0.15, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-15.html

* Wed Oct 9 2013 Devrim GUNDUZ <devrim@gunduz.org> 9.0.14-1PGDG
- Update to 9.0.14, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-14.html

* Wed Apr 17 2013 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.13-2PGDG
- Fix pid file name in init script, so that it is more suitable for multiple
  postmasters. Per suggestion from Andrew Dunstan. Fixes #92.

* Tue Apr 02 2013 Jeff Frost <jeff@pgexperts.com> - 9.0.13-1PGDG
- Update to 9.0.13, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-13.html
  which also includes fixes for CVE-2013-1899 and CVE-2013-1900.

* Wed Feb 6 2013 Devrim GUNDUZ <devrim@gunduz.org> 9.0.12-1PGDG
- Update to 9.0.12, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-12.html

* Wed Dec 5 2012 Devrim GUNDUZ <devrim@gunduz.org> 9.0.11-1PGDG
- Update to 9.0.11, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-11.html

* Sun Sep 23 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.10-1PGDG
- Update to 9.0.10, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-10.html

* Sun Sep 02 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.9-3PGDG
- Fix incorrect pg libs version, per report from Roy Hocknull.

* Tue Aug 28 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.9-2PGDG
- Install linker conf file with alternatives, so that the latest
  version will always be used. Fixes #77.

* Wed Aug 15 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.9-1PGDG
- Update to 9.0.9, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-9.html
  which also includes fixes for CVE-2012-3489 and CVE-2012-3488.

* Wed Jun 06 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.8-2PGDG
- Disable runselftest. We have buildfarm coverage already.

* Mon Jun 4 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.8-1PGDG
- Update to 9.0.8, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-8.html
  which also includes fixes for CVE-2012-2143, CVE-2012-2655.

* Wed May 30 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.7-2PGDG
- Fix output message when initdb is missing -- add version number. Per Josh
  Berkus.

* Sun Feb 26 2012 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.7-1PGDG
- Update to 9.0.7, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-7.html
  which also includes fixes for CVE-2012-0866, CVE-2012-0867 and
  CVE-2012-0868 .

* Sun Dec 4 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.6-1PGDG
- Update to 9.0.6, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-6.html
- Fix some of the nls related build issues.

* Tue Oct 18 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.5-2PGDG
- Move doc directory only once. Per Alex Tkachenko.

* Fri Sep 23 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.5-1PGDG
- Update to 9.0.5, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-5.html

* Tue Aug 16 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.4-2PGDG
- Revert changes in init script, which breaks stop process.

* Mon Apr 18 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.4-1PGDG
- Update to 9.0.4, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-4.html
- Put pltcl, plperl and	plpython's find_lang blocks into if block,
  so that our macros will really work. Patch from Manuel Sugawara.

* Fri Jan 28 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.3-1PGDG
- Update to 9.0.3, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-3.html

* Fri Jan 7 2011 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.2-2PGDG
- Explicitly Provide: versionless postgresql*, to satisfy dependencies
  in OS packages. Already did it in -jdbc package, and it worked.
- Add LINUX_OOM_ADJ=0 to ensure child processes reset postmaster's oom_adj,
  per Noah Misch .
- Remove Conflicts for pre 7.4

* Tue Dec 14 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.2-1PGDG
- Update to 9.0.2, per changes described at:
  http://www.postgresql.org/docs/9.0/static/release-9-0-2.html

* Tue Dec 7 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-6PGDG
- Fix a major issue: Keep alternatives links during an upgrade.	In
  previous releases, all links were gone during	an upgrade. Per	report
  and fix from Richard A Karhuse.

* Wed Nov 17 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-5PGDG
- postgres user needs to own .bash_profile
- Revert postun->postun change. I hope this will fix the issue that prevents
  postgresql90 package to be removed completely.

* Thu Nov 11 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-4PGDG
- Fix an oversight in .bash_profile generation, per report from Ger Timmens.

* Thu Nov 11 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-3PGDG
- Fix status line in init script, per report from Jeff Mace in -bugs list, #5746
- Remove hardcoded major version numbers in init script, and substitute PGMAJORVERSION
  instead.

* Fri Oct 8 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-2PGDG
- Re-enable thread safety. I probably missed it while working on migration.
- Append PGPORT to pid filename in init script. Per report from Carlos Sotto Maior.
- Properly fix .bash_profile issue, by moving it to %%post server, and not owning
  the file.
- Add PGPORT to lockfile variable in init script.

* Fri Oct 1 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.1-1PGDG
- Update to 9.0.1, per changes described at:
  http://www.postgresql.org/docs/current/static/release-9-0-1.html,
  which	also fixes CVE-2010-3433.
- Change pam file name, per bug report from Michael Best.
- Move plpython2.so file into correct subpackage, per report from Damon Hart.
- Don't install .bash_profile as we used to in pre 9.0. Instead, use cat,
  so that package manager will be happy during upgrade to new major version.
  Per report from Christian V R Lopez.
- Arrange for the postmaster, but not any of its child processes, to be run
  with oom_adj -17.  This compensates for the OOM killer not being smart about
  accounting for shared memory usage.

* Fri Sep 17 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0.0-1PGDG
- Update to PostgreSQL 9.0.0

* Fri Sep 10 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-rc1_2PGDG
- Finally, renamed package from postgresql to postgresql90, in order to
  *really* fix parallel RPM installation. Previous versions were installable
  via rpm command itself, but per some testing with 9.1 packages, I figured
  that is is not possible with yum.

* Mon Sep 06 2010 Devrim GÜNDÜZ <devrim@gunduz.org> - 9.0-rc1_1PGDG.1
- Use better/consistent name for psql alternatives section. Per 9.1 RPM tests.

* Tue Aug 31 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0rc1-1PGDG
- Update to 9.0 rc1
- Update (fix) .bash_profile so that it contains correct $PGDATA.

* Mon Aug 2 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta4-1PGDG
- Update to 9.0 beta4

* Fri Jul 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta3-1PGDG
- Update to 9.0 beta3

* Thu Jul 1 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta2-3PGDG
- Re-enable uuid support.

* Wed Jun 9 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta2-2PGDG
- Apply more improvements on alternatives section, per Konstantin
  Pelepelin. While passing, improve and	fix drop alternatives part,
  too. Use preun instead of postun.
- Trim changelog.

* Sun Jun 6 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta2-1PGDG
- Update to 9.0 Beta2
- Fix docdir configure option

* Fri Apr 30 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0beta1-1PGDG
- Update to 9.0 Beta1

* Thu Apr 1 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0alpha5-1PGDG
- Update to 9.0 Alpha5
- Add a few lines for installing html and man pages.

* Mon Mar 22 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0alpha4-2PGDG
- Move euc2004_sjis2004.so into	server package.	This explains why
  initdb is broken when	-contrib is not	installed. Fixes #11.
- Improve/fix alternatives section

* Sun Feb 21 2010 Devrim GUNDUZ <devrim@gunduz.org> 9.0alpha4-1PGDG
- Update to 9.0 Alpha4
- Update README.rpm-dist to reflect latest changes
- Rename pgfts macro to disablepgfts to match 9.0 behaviour.
- Fix service name in spec file.
- Update init script for LSB compilance	issues (as much	as possible).
- Install a file under /etc/ld.so.conf.d, so libs can be detected easily.

* Mon Dec 21 2009 Devrim GUNDUZ <devrim@gunduz.org> 8.5alpha3-1PGDG
- Update to 8.5	Alpha3

* Wed Oct 28 2009 Devrim GUNDUZ <devrim@gunduz.org> 8.5alpha2-1PGDG
- Update to 8.5	Alpha2

* Tue Aug 25 2009 Devrim GUNDUZ <devrim@gunduz.org> 8.5alpha1-2PGDG
- More fixes for multiple version installation.

* Mon Aug 24 2009 Devrim GUNDUZ <devrim@gunduz.org> 8.5alpha1-1PGDG
- Initial cut for 8.5 Alpha 1, which supports multiple version installation.
  WARNING: This is for testing only.
