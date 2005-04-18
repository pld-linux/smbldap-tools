Summary:	User & Group administration tools for Samba-OpenLDAP
Summary(pl):	Narzêdzia do administracji u¿ytkownikami i grupami dla Samby i OpenLDAP
Name:		smbldap-tools
version:	0.8.8
Release:	0.1
Group:		Applications/Networking
License:	GPL
URL:		http://samba.IDEALX.org/
Source0:	http://samba.idealx.org/dist/%{name}-%{version}.tgz
# Source0-md5:	bb5213ee265e9c301796af77a1894001
Patch0:		%{name}-Makefile.patch
Patch1:		%{name}-smbldap_tools.pm.patch
Requires:	perl-Crypt-SmbHash
Requires:	perl-ldap
Requires:	samba
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
%patch1 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	prefix=%{_prefix} \
	sbindir=%{_sbindir} \
	sysconfdir=%{_sysconfdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS COPYING ChangeLog FILES INFRA README INSTALL TODO
%doc smb.conf smbldap.conf smbldap_bind.conf configure.pl doc/html
%verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap.conf
%attr(600,root,root) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/smbldap-tools/smbldap_bind.conf
%attr(755,root,root) %{_sbindir}/*
