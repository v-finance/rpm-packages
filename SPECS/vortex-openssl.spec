# upstream version
%global major_version	1
%global minor_version	0
%global patch_version	2u
# RPM package release version
%global release_version	1

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

%global archive_file 	OpenSSL_1_0_2u.tar.gz
%global archive_dir 	openssl-OpenSSL_1_0_2u

%global install_dir 	/vortex/%{bundle_name}

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================

# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-openssl
Summary: OpenSSL 1.0.x library compatible with python 3.4
URL: https://www.openssl.org/
License: Apache v2

Version: %{major_version}.%{minor_version}.%{patch_version}
Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: gcc-c++
BuildRequires: glibc-devel
BuildRequires: make
BuildRequires: perl
BuildRequires: pkgconfig
BuildRequires: tar

# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: https://github.com/openssl/openssl/archive/%{archive_file}

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
rm -rf %{archive_dir}
tar zxvf %{_topdir}/SOURCES/%{archive_file}
cd %{archive_dir}

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archive_dir}
./config --install_prefix=%{buildroot} --prefix=%{install_dir} --openssldir=%{install_dir}/share/openssl -fPIC
%make_build

# ======================================================
# Checks for packaging issues
# ======================================================

%check
cd %{archive_dir}
make test


# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archive_dir}
# Install the software only (no documentation)
make install_sw


%files
%{install_dir}


%changelog
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Wed May 13 2020 tim.vandermeersch@vortex-financials.be
- Initial version
