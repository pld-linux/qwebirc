# TODO
# - init service
# - reap out bin/compile from code, we can package final result
# - python deps
# - actual (and secure) web aliases
# - setup instructions: http://www.qwebirc.org/faq
Summary:	Package that uses webapps configuration
Name:		qwebirc
Version:	0.1
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://bitbucket.org/slug/qwebirc/get/stable.tar.bz2#/%{name}-stable.tar.bz2
# Source0-md5:	3d2061a53bda5615dc1ebf1cd35d3b5b
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://www.qwebirc.org/
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires:	python-simplejson
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
qwebirc is a fast, easy to use, free and open source IRC client
designed by and originally just for the QuakeNet IRC network.

%prep
%setup -qn %{name}

rm -rf simplejson

grep -rl /bin/env . | xargs %{__sed} -i -e '1s,^#!.*python,#!%{__python},'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -a . $RPM_BUILD_ROOT%{_appdir}
rm -f $RPM_BUILD_ROOT%{_appdir}/{debug*,AUTHORS,LICENSE,*.example}
ln -s %{_sysconfdir}/config.py $RPM_BUILD_ROOT%{_appdir}

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a config.py.example $RPM_BUILD_ROOT%{_sysconfdir}/config.py
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS config.py.example
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.py
%{_appdir}
