# upstream version
%global major_version	3
%global minor_version	4
%global patch_version	4
# RPM package release version
%global release_version	1

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

# branch name on github (e.g. https://github.com/v-finance/cpython/<branch_name>)
%global branch_name	3.4.4-vortex

%global install_dir	/vortex/%{bundle_name}

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-python3
Summary: Interpreter of the Python programming language
URL: https://www.python.org/
License: Python

Version: %{major_version}.%{minor_version}.%{patch_version}
Release: %{release_version}%{?dist}

%global archive_file %{branch_name}.tar.gz
%global archive_dir cpython-%{branch_name}


# ==================================
# Conditionals controlling the build
# ==================================

# =====================
# General global macros
# =====================

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf
#BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel
#BuildRequires: desktop-file-utils
BuildRequires: expat-devel

BuildRequires: findutils
BuildRequires: gcc-c++
#%%if %%{with gdbm}
#BuildRequires: gdbm-devel >= 1:1.13
#%endif
BuildRequires: gdbm-devel
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libappstream-glib
BuildRequires: libffi-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
#BuildRequires: libGL-devel
#BuildRequires: libX11-devel
BuildRequires: ncurses-devel

#BuildRequires: openssl-devel	replaced by vortex-openssl
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel
BuildRequires: gdb

BuildRequires: tar
#BuildRequires: tcl-devel
#BuildRequires: tix-devel
#BuildRequires: tk-devel

#%%if %%{with valgrind}
#BuildRequires: valgrind-devel
#%endif

BuildRequires: xz-devel
BuildRequires: zlib-devel

BuildRequires: /usr/bin/dtrace

# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: /usr/sbin/ifconfig

BuildRequires: vortex-%{bundle_name}-openssl

#%%if %%{with rewheel}
#BuildRequires: python3-setuptools
#BuildRequires: python3-pip

# Verify that the BuildRoot includes python36.
# Not actually needed for build.
#BuildRequires: python36-devel
#%endif

# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
# FIXME
#Source0: https://github.com/v-finance/cpython/archive/%%{archive_file}
Source0: https://github.com/tim-vdm/cpython/archive/%{archive_file}

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-openssl

Provides: %{install_dir}/bin/python

%description
Custom Vortex python build.

# ======================================================
# The prep phase of the build:
# ======================================================
%prep
cd %{_topdir}/BUILD
rm -rf %{archive_dir}
tar zxvf %{_topdir}/SOURCES/%{archive_file}
cd %{archive_dir}

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archive_dir}
export VORTEX_BUNDLE_ROOT=%{install_dir}

./configure \
  --prefix=%{install_dir} \
  --enable-ipv6 \
  --enable-shared \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --with-dtrace \
  --with-lto \
  --with-ssl-default-suites=openssl

%make_build

# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archive_dir}
export VORTEX_BUNDLE_ROOT=%{install_dir}

make DESTDIR=%{buildroot} INSTALL="install -p" install

%global pybasever %{major_version}.%{minor_version}
# Make sure the BUILDROOT is not part of any file (for buildrpm's check-buildroot)
sed -i "s|%{buildroot}||g" %{buildroot}%{install_dir}/lib/python%{pybasever}/site-packages/setuptools-18.2.dist-info/RECORD
sed -i "s|%{buildroot}||g" %{buildroot}%{install_dir}/lib/python%{pybasever}/site-packages/pip-7.1.2.dist-info/RECORD

# Fix shebangs before buildrpm's brp-mangle-shebangs changes them to the system's python
find %{buildroot} -type f -exec sed -i "s|#\!/usr/bin/env python3|#\!%{install_dir}/bin/python3|g" {} \;
find %{buildroot} -type f -exec sed -i "s|#\! /usr/bin/env python3|#\!%{install_dir}/bin/python3|g" {} \;
find %{buildroot} -type f -exec sed -i "s|#\! /usr/local/bin/python|#\!%{install_dir}/bin/python|g" {} \;
sed -i "s|#\!/usr/bin/env python|#\!%{install_dir}/bin/python3|g" %{buildroot}%{install_dir}/lib/python%{pybasever}/encodings/rot_13.py
sed -i "s|#\!/usr/bin/env python|#\!%{install_dir}/bin/python3|g" %{buildroot}%{install_dir}/lib/python%{pybasever}/lib2to3/tests/data/different_encoding.py
sed -i "s|#\!/usr/bin/env python|#\!%{install_dir}/bin/python3|g" %{buildroot}%{install_dir}/lib/python%{pybasever}/lib2to3/tests/data/false_encoding.py


%postun
# remove all files in the installation dir (e.g. installed pip packages etc.)
rm -rf %{install_dir}


%files
# include all files for now
%{install_dir}


%changelog
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Tue May 19 2020 tim.vandermeersch@vortex-financials.be
- Initial version
