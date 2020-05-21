# ==================
# Top-level metadata
# ==================

Name: vortex-openssl
Summary: OpenSSL 1.0.x library compatible with python 3.4
URL: https://www.openssl.org/
License: Apache v2

Version: 1.0.2u
Release: 1%{?dist}

%global archivefile OpenSSL_1_0_2u.tar.gz
%global archivedir openssl-OpenSSL_1_0_2u

%global vortexdir /vortex

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: gcc-c++
BuildRequires: glibc-devel
BuildRequires: make
#BuildRequires: perl
BuildRequires: pkgconfig
BuildRequires: tar

# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: https://github.com/openssl/openssl/archive/%{archivefile}

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: glibc 

%description
Custom Vortex OpenSSL build that is compatible with python 3.4.

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
cd %{_topdir}/BUILD
rm -rf %{archivedir}
tar zxvf %{_topdir}/SOURCES/%{archivefile}
cd %{archivedir}

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archivedir}
./config --install_prefix=%{buildroot} --prefix=%{vortexdir}/usr --openssldir=%{vortexdir}/usr/openssl -fPIC
make %{?_smp_mflags}

# ======================================================
# Checks for packaging issues
# ======================================================

%check
cd %{archivedir}
make test


# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archivedir}
# Install the software only (no documentation)
make install_sw


%files
# binaries
%{vortexdir}%{_bindir}/openssl
%{vortexdir}%{_bindir}/c_rehash
# include files
%{vortexdir}%{_includedir}/openssl/*
# libraries
%{vortexdir}/usr/lib/libcrypto.a
%{vortexdir}/usr/lib/libssl.a
%{vortexdir}/usr/lib/pkgconfig/*
# config files
%{vortexdir}/usr/openssl/misc/*
%{vortexdir}/usr/openssl/openssl.cnf


%changelog
* Wed May 13 2020 tim.vandermeersch@vortex-financials.be
- Initial version
