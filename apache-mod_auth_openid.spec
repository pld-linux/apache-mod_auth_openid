%define		mod_name	auth_openid
%define 	apxs		%{_sbindir}/apxs
Summary:	The Apache OpenID Module
Name:		apache-mod_%{mod_name}
Version:	0.6
Release:	0.1
License:	MIT
Group:		Networking/Daemons/HTTP
Source0:	http://butterfat.net/releases/mod_auth_openid/mod_auth_openid-%{version}.tar.gz
# Source0-md5:	f72c6a716e368f83756b25c062e70666
URL:		http://findingscience.com/mod_auth_openid/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	libopkele-devel >= 2.0
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sqlite3-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_auth_openid is an authentication module for the Apache 2
webserver. It handles the functions of an OpenID consumer as specified
in the OpenID 2.0 specification.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%configure \
	--with-apxs=%{apxs}
%{__make} \
	CC="%{__cc}" \
	APACHE_CFLAGS="%{rpmcflags} -I$(%{apxs} -q INCLUDEDIR) -I$(apr-1-config --includedir) -I$(apu-1-config --includedir)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}
install -p .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

# or, if no directives needed, put just LoadModule line
echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README UPGRADE
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
