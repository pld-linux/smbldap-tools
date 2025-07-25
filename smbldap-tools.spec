#
# Conditional build:
%bcond_with	autodeps	# don't BR packages needed only for resolving deps

Summary:	User & Group administration tools for Samba-OpenLDAP
Summary(pl.UTF-8):	Narzędzia do administracji użytkownikami i grupami dla Samby i OpenLDAP
Name:		smbldap-tools
Version:	0.9.10
Release:	1
License:	GPL
Group:		Applications/Networking
Source0:	http://download.gna.org/smbldap-tools/sources/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	f52a626637c468d66a4e71f30c174873
URL:		https://gna.org/projects/smbldap-tools/
Patch0:		%{name}-configure.patch
Patch1:		%{name}-krb5.patch
Patch2:		%{name}-no-client-cert.patch
Patch3:		%{name}-podchecker.patch
BuildRequires:	perl-tools-pod
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
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/smbldap-tools
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p smbldap.conf smbldap_bind.conf $RPM_BUILD_ROOT%{_sysconfdir}/smbldap-tools
install -p smbldap-config.cmd $RPM_BUILD_ROOT%{_sbindir}/smbldap-config
install -p smbldap-upgrade-0.9.6.cmd $RPM_BUILD_ROOT%{_sbindir}/smbldap-upgrade-0.9.6.pl

%clean
rm -rf $RPM_BUILD_ROOT

%triggerpostun -- %{name} < 0.9.7-0
if [ "$1" -eq "2" ]; then ## Upgrade
	%{_sbindir}/smbldap-upgrade-0.9.6.pl || :
fi

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS ChangeLog FILES INFRA README INSTALL TODO
%doc doc/*.example doc/smbldap-tools.* doc/migration_scripts
%dir %{_sysconfdir}/smbldap-tools
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(755,root,root) %{_sbindir}/smbldap-config
%attr(755,root,root) %{_sbindir}/smbldap-groupadd
%attr(755,root,root) %{_sbindir}/smbldap-groupdel
%attr(755,root,root) %{_sbindir}/smbldap-grouplist
%attr(755,root,root) %{_sbindir}/smbldap-groupmod
%attr(755,root,root) %{_sbindir}/smbldap-groupshow
%attr(755,root,root) %{_sbindir}/smbldap-passwd
%attr(755,root,root) %{_sbindir}/smbldap-populate
%attr(755,root,root) %{_sbindir}/smbldap-useradd
%attr(755,root,root) %{_sbindir}/smbldap-userdel
%attr(755,root,root) %{_sbindir}/smbldap-userinfo
%attr(755,root,root) %{_sbindir}/smbldap-userlist
%attr(755,root,root) %{_sbindir}/smbldap-usermod
%attr(755,root,root) %{_sbindir}/smbldap-usershow
%attr(755,root,root) %{_sbindir}/smbldap-upgrade-0.9.6.pl
%{perl_vendorlib}/smbldap_tools.pm
