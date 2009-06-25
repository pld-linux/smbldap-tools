#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define		_name	smbldap_tools
%include	/usr/lib/rpm/macros.perl
Summary:	User & Group administration tools for Samba-OpenLDAP
Summary(pl.UTF-8):	Narzędzia do administracji użytkownikami i grupami dla Samby i OpenLDAP
Name:		smbldap-tools
Version:	0.9.6
# Despite name-ver file this is REALLY a pre1 release
Release:	0.pre1.3
License:	GPL
Group:		Applications/Networking
URL:		https://gna.org/projects/smbldap-tools/
#Source0:	http://download.gna.org/smbldap-tools/packages/pre-release/%{name}-%{version}.tgz
Source0:	http://www.iallanis.info/smbldap-tools/development_release/%{name}-%{version}.tgz
# Source0-md5:	250e51102fe8731dfcb32d4da29c02d7
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-configure.patch
Patch2:		%{name}-nscd.patch
Patch3:		%{name}-krb5.patch
Patch4:		%{name}-no-client-cert.patch
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with autodeps}
BuildRequires:	perl-Crypt-SmbHash
BuildRequires:	perl-Digest-SHA1
BuildRequires:	perl-ldap
%endif
Requires:	openldap
Requires:	samba
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
In settings with OpenLDAP and Samba-LDAP servers, this collection is
useful to add, modify and delete users and groups, and to change Unix
and Samba passwords. In those context they replace the system tools to
manage users, groups and passwords.

%description -l pl.UTF-8
W połączeniu z OpenLDAP i serwerami Samba-LDAP ten zestaw narzędzi
jest użyteczny przy dodawaniu, modyfikowaniu i usuwaniu użytkowników i
grup oraz zmianie haseł w Uniksie i Sambie. W tym zastosowaniu mogą
zastąpić narzędzia systemowe do zarządzania użytkownikami, grupami i
hasłami.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	prefix=%{_prefix} \
	sbindir=%{_sbindir} \
	sysconfdir=%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{perl_vendorlib}
mv -f $RPM_BUILD_ROOT%{_sbindir}/%{_name}.pm $RPM_BUILD_ROOT%{perl_vendorlib}
install configure.pl $RPM_BUILD_ROOT%{_sbindir}/smbldap-configure

rm -f $RPM_BUILD_ROOT%{_sbindir}/*.{orig,spec}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog FILES INFRA README INSTALL TODO
%doc doc/smb.conf smbldap.conf smbldap_bind.conf doc/smbldap* doc/migration_scripts/smbldap-migrate-*
%dir %{_sysconfdir}/smbldap-tools
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(755,root,root) %{_sbindir}/*
%{perl_vendorlib}/%{_name}.pm
