# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

%if "%{bundle_name}" == "stable"
# upstream version
%global major_version	3
%global minor_version	4
%global patch_version	4
# RPM package release version
%global release_version	2
%endif

%if "%{bundle_name}" == "test"
# upstream version
%global major_version	3
%global minor_version	8
%global patch_version	3
# RPM package release version
%global release_version	1
%endif

%global arch_triplet	%(i686-w64-mingw32-gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================

# Do not try to strip dll/pyd files
%define __strip /bin/true

# ==================
# Top-level metadata
# ==================

Version: 	%{major_version}.%{minor_version}.%{patch_version}
Name:           vortex-%{bundle_name}-mingw32-python3
Summary:        Repackaged python %{version} for mingw
URL: 		https://www.python.org/
License: 	Python

Release: 	%{release_version}%{?dist}

BuildArch:	noarch

# =======================
# Build-time requirements
# =======================

BuildRequires:	unzip

# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: https://github.com/v-finance/rpm-packages/releases/download/python/python-%{version}-win32.zip

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

%description
Repackaged python %{version} for mingw

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%setup -q -c

# ======================================================
# Configuring and building the code:
# ======================================================

%build

# ======================================================
# Installing the built code:
# ======================================================

%install
%global short_version	%{major_version}.%{minor_version}
%global compact_version	%{major_version}%{minor_version}

# binaries & dll files
mkdir -p %{buildroot}%{install_dir}/bin
install python.exe %{buildroot}%{install_dir}/bin
install pythonw.exe %{buildroot}%{install_dir}/bin
install python%{compact_version}.dll %{buildroot}%{install_dir}/bin
install DLLs/sqlite3.dll %{buildroot}%{install_dir}/bin

%if "%{bundle_name}" == "stable"
install DLLs/python3.dll %{buildroot}%{install_dir}/bin
%endif

%if "%{bundle_name}" == "test"
install python3.dll %{buildroot}%{install_dir}/bin
install vcruntime140.dll %{buildroot}%{install_dir}/bin
install DLLs/libcrypto-1_1.dll %{buildroot}%{install_dir}/bin
install DLLs/libffi-7.dll %{buildroot}%{install_dir}/bin
install DLLs/libssl-1_1.dll %{buildroot}%{install_dir}/bin
%endif

# include files
mkdir -p %{buildroot}%{install_dir}/include/python%{short_version}
install -m 644 include/*.h %{buildroot}%{install_dir}/include/python%{short_version}

%if "%{bundle_name}" == "test"
mkdir -p %{buildroot}%{install_dir}/include/python%{short_version}/cpython
mkdir -p %{buildroot}%{install_dir}/include/python%{short_version}/internal
install -m 644 include/cpython/*.h %{buildroot}%{install_dir}/include/python%{short_version}/cpython
install -m 644 include/internal/*.h %{buildroot}%{install_dir}/include/python%{short_version}/internal
%endif

# python modules
mkdir -p %{buildroot}%{install_dir}/lib/python%{short_version}
cp -r Lib/* %{buildroot}%{install_dir}/lib/python%{short_version}
install DLLs/*.pyd %{buildroot}%{install_dir}/lib/python%{short_version}

# lib files
install libs/*.lib %{buildroot}%{install_dir}/lib


%files
%{install_dir}

%changelog
* Wed Jul 06 2020 tim.vandermeersch@vortex-financials.be
- Add support for python 3.8.3
* Wed Jun 17 2020 tim.vandermeersch@vortex-financials.be
- Release 2
- Include sqlite3.dll
- Put .pyd files in lib/python3.4
* Tue Jun 02 2020 tim.vandermeersch@vortex-financials.be
- Initial release
