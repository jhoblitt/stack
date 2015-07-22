%global scl_name_prefix lsst
%global scl_name_base stack
%global scl_name_version 1

%global scl %{scl_name_prefix}-%{scl_name_base}%{scl_name_version}

# Optional but recommended: define nfsmountable
%global nfsmountable 1

%global _scl_prefix /opt/%{scl_name_prefix}
%scl_package %scl

Summary: Package that installs %scl
Name: %scl_name
Version: 3
Release: 1%{?dist}
License: GPLv2+
#Requires: %scl_require devtoolset-3
#Requires: %scl_require python27
Requires: /opt/rh/devtoolset-3/enable
Requires: /opt/rh/python27/enable
BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build
Requires: %{name}-scldevel = %{version}-%{release}

%description build
Package shipping essential configuration macros to build %scl Software Collection.

# This is only needed when you want to provide an optional scldevel subpackage
%package scldevel
Summary: Package shipping development files for %scl
Requires: python27-scldevel
# devtoolset-3 does not have a -scldevel package
Requires: devtoolset-3-build
Requires: %{name}-runtime = %{version}-%{release}

%description scldevel
Package shipping development files, especially useful for development of
packages depending on %scl Software Collection.

%prep
%setup -c -T

%install
%scl_install

cat >> %{buildroot}%{_scl_scripts}/enable << EOF
. scl_source enable devtoolset-3
. scl_source enable python27

export PATH=%{_bindir}\${PATH:+:\${PATH}}
export LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}
export MANPATH=%{_mandir}:\$MANPATH
export PKG_CONFIG_PATH=%{_libdir}/pkgconfig\${PKG_CONFIG_PATH:+:\${PKG_CONFIG_PATH}}
EOF

# This is only needed when you want to provide an optional scldevel subpackage
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install the generated man page
#mkdir -p %{buildroot}%{_mandir}/man7/
#install -p -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/

%files

%files runtime -f filelist
%scl_files

%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog