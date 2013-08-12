%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%define pecl_name gearman
%define php_base php53u

Name:           %{php_base}-pecl-gearman
Version:        1.1.1
Release:        2.ius%{?dist}
Summary:        PECL package for gearmand

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/gearman
Source0:        http://pecl.php.net/get/gearman-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  automake %{php_base}-devel %{php_base}-pear
BuildRequires:  libgearman-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Provides:       php-pecl(Gearman) = %{version}

%if 0%{?php_zend_api}
Requires:       %{php_base}(zend-abi) = %{php_zend_api}
Requires:       %{php_base}(api) = %{php_core_api}
%else
Requires:       %{php_base}-api = %{php_apiver}
%endif

%description
The Gearman extension uses libgearman library to provide API for communicating
with gearmand, and writing clients and workers.

%prep
%setup -qcn %{pecl_name}-%{version}
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pecl_name}-%{version}/%{pecl_name}.xml
cd %{pecl_name}-%{version}

%build
cd %{pecl_name}-%{version}
phpize
%configure --enable-%{pecl_name}
%{__make}

%install
cd %{pecl_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__make} install INSTALL_ROOT=$RPM_BUILD_ROOT

# install config file
install -d $RPM_BUILD_ROOT%{_sysconfdir}/php.d
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

# install doc files
install -d docs
install -pm 644 CREDITS LICENSE README docs

# Install XML package description
install -d $RPM_BUILD_ROOT%{pecl_xmldir}
install -pm 644 %{pecl_name}.xml $RPM_BUILD_ROOT%{pecl_xmldir}/%{name}.xml


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/docs/*
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Mon Jul 29 2013 Ben Harper <ben.harper@rackspace.com> - 1.1.1-2
- ported from https://github.com/BlakeGardner/php53u-pecl-gearman

* Mon Jul 22 2013 Blake Gardner <blakegardner@cox.net> 1.1.1-1
- Upgraded to version 1.1.1

* Mon Jul 22 2013 Blake Gardner <blakegardner@cox.net> 0.8.0-1
- Upgraded to version 0.8.0

* Mon Sep 27 2010 Andy Thompson <athompson@ibuildings.com> 0.7.0-1
- Initial release
