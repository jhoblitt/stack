%global scl_name_prefix lsst
%global scl_name_base stack
%global scl_name_version 1

%global scl %{scl_name_prefix}-%{scl_name_base}%{scl_name_version}

%global _scl_prefix /opt/%{scl_name_prefix}
%scl_package %scl

# Defaults for the values for the python27 Software Collection. These
# will be used when python27-scldevel is not in the buildroot
%{!?scl_python:%global scl_python python27}
%{!?scl_prefix_python:%global scl_prefix_python %{scl_python}-}

# Only for this build, we need to override default __os_install_post, because
# the default one would find /opt/.../lib/python2.7/ and rpmbuild would
# try to bytecompile with the system /usr/bin/python2.7 (which doesn't exist)
%global __os_install_post %{%{scl_python}_os_install_post}
# Similarly, override __python_requires for automatic dependency generator
%global __python_requires %{%{scl_python}_python_requires}

# The directory for site packages for this Software Collection
# python27python_sitelib is provided by python27-python-devel
%global _scl_sitelib %(echo %{python27python_sitelib} | sed 's|%{scl_python}|%{scl}|')

Summary: Package that installs %scl
Name: %scl_name
Version: 9
Release: 1%{?dist}
License: GPLv2+
#Requires: /opt/rh/devtoolset-3/enable
#Requires: /opt/rh/python27/enable
BuildRequires: scl-utils-build
BuildRequires: %{scl_prefix_python}scldevel
# Require python27-python-devel, we will need macros from that package
BuildRequires: %{scl_prefix_python}python-devel
Requires: %{scl_prefix_python}python-versiontools


Requires: bison
Requires: curl
Requires: blas
Requires: bzip2-devel
Requires: bzip2
Requires: flex
Requires: fontconfig
Requires: freetype-devel
Requires: devtoolset-3-gcc-gfortran >= 4.9
Requires: devtoolset-3-gcc-c++ >= 4.9
Requires: gcc-gfortran
Requires: devtoolset-3-git >= 1.9
Requires: libuuid-devel
Requires: libXext
Requires: libXrender
Requires: libXt-devel
Requires: make
Requires: openssl-devel
Requires: patch
Requires: perl
Requires: readline-devel
Requires: zlib-devel
Requires: ncurses-devel
Requires: cmake
Requires: glib2-devel
Requires: gettext
Requires: libcurl-devel
Requires: perl-ExtUtils-MakeMaker
Requires: java-1.7.0-openjdk

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils
Requires: %{scl_prefix_python}runtime
Requires: devtoolset-3-runtime


%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build
Requires: %{scl_prefix_python}scldevel
# devtoolset-3 does not have a -scldevel package
Requires: devtoolset-3-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

# This is only needed when you want to provide an optional scldevel subpackage
%package scldevel
Summary: Package shipping development files for %scl
Requires: %{name}-build   = %{version}-%{release}

%description scldevel
Package shipping development files, especially useful for development of
packages depending on %scl Software Collection.

%prep
%setup -c -T

%build
%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
. scl_source enable %{scl_python}
. scl_source enable devtoolset-3

export PYTHONPATH=%{_scl_sitelib}${PYTHONPATH:+:${PYTHONPATH}}
export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\$MANPATH
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

mkdir -p %{buildroot}%{_scl_sitelib}

cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config << EOF
%%scl_package_override() %%{expand:%{?python27_os_install_post:%%global __os_install_post %%python27_os_install_post}
%%global __python_requires %%python27_python_requires
%%global __python_provides %%python27_python_provides
%%global __python %python27__python
%%global __python2 %python27__python
%%global python_sitelib %_scl_sitelib
%%global python2_sitelib %_scl_sitelib
}
EOF

# This is only needed when you want to provide an optional scldevel subpackage
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

%files

%files runtime -f filelist
%scl_files
%_scl_sitelib

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Thu Jul 23 2015 Joshua Hoblitt <josh@hoblitt.com> 9-1
- 

* Thu Jul 23 2015 Joshua Hoblitt <josh@hoblitt.com> 8-1
- 

* Thu Jul 23 2015 Joshua Hoblitt <josh@hoblitt.com> 7-1
- 

* Thu Jul 23 2015 Joshua Hoblitt <josh@hoblitt.com> 6-1
- 

* Thu Jul 23 2015 Joshua Hoblitt <josh@hoblitt.com> 5-1
- 

* Wed Jul 22 2015 Joshua Hoblitt <josh@hoblitt.com> 4-1
- new package built with tito

