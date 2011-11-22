#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define		_name	smbldap_tools
%include	/usr/lib/rpm/macros.perl
Summary:	User & Group administration tools for Samba-OpenLDAP
Summary(pl.UTF-8):	Narzędzia do administracji użytkownikami i grupami dla Samby i OpenLDAP
Name:		smbldap-tools
Version:	0.9.7
Release:	0.1
License:	GPL
Group:		Applications/Networking
Source0:	http://download.gna.org/smbldap-tools/sources/0.9.7/%{name}-%{version}.tar.gz
# Source0-md5:	d9f169a77b527672778e4307091bec36
URL:		https://gna.org/projects/smbldap-tools/
Patch0:		%{name}-configure.patch
Patch1:		%{name}-krb5.patch
Patch2:		%{name}-no-client-cert.patch
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/smbldap-tools

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p smbldap.conf smbldap_bind.conf $RPM_BUILD_ROOT%{_sysconfdir}/smbldap-tools
install -p smbldap-config.cmd $RPM_BUILD_ROOT%{_sbindir}/smbldap-config

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog FILES INFRA README INSTALL TODO
%doc doc/*.example doc/smbldap-tools.* doc/migration_scripts
%dir %{_sysconfdir}/smbldap-tools
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(755,root,root) %{_sbindir}/*
%{perl_vendorlib}/%{_name}.pm
