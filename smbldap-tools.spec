#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define		_name	smbldap_tools
%include	/usr/lib/rpm/macros.perl
Summary:	User & Group administration tools for Samba-OpenLDAP
Summary(pl):	Narzêdzia do administracji u¿ytkownikami i grupami dla Samby i OpenLDAP
Name:		smbldap-tools
Version:	0.9.1
Release:	3
License:	GPL
Group:		Applications/Networking
URL:		http://samba.idealx.org/
Source0:	http://samba.idealx.org/dist/%{name}-%{version}.tgz
# Source0-md5:	12ddaf6393420ee24c4af94152e9ee2e
Patch0:		%{name}-Makefile.patch
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

%description -l pl
W po³±czeniu z OpenLDAP i serwerami Samba-LDAP ten zestaw narzêdzi
jest u¿yteczny przy dodawaniu, modyfikowaniu i usuwaniu u¿ytkowników i
grup oraz zmianie hase³ w Uniksie i Sambie. W tym zastosowaniu mog±
zast±piæ narzêdzia systemowe do zarz±dzania u¿ytkownikami, grupami i
has³ami.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	prefix=%{_prefix} \
	sbindir=%{_sbindir} \
	sysconfdir=%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT

rm -f  $RPM_BUILD_ROOT%{_sbindir}/%{name}.spec
install -d $RPM_BUILD_ROOT%{perl_vendorlib}
mv -f $RPM_BUILD_ROOT%{_sbindir}/%{_name}.pm $RPM_BUILD_ROOT%{perl_vendorlib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS COPYING ChangeLog FILES INFRA README INSTALL TODO
%doc smb.conf smbldap.conf smbldap_bind.conf configure.pl doc/html doc/smbldap*
%dir %{_sysconfdir}/smbldap-tools
%verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%{perl_vendorlib}/%{_name}.pm
%attr(600,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(755,root,root) %{_sbindir}/*
