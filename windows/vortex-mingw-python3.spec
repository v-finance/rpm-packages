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

%global arch_triplet	%(i686-w64-mingw32-gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}



# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================

# Do not try to strip dll/pyd files
%define __strip /bin/true

# ==================
# Top-level metadata
# ==================

Name:           vortex-%{bundle_name}-mingw32-python3
Summary:        Repackaged python 3.4.4 for mingw
URL: 		https://www.python.org/
License: 	Python

Version: 	%{major_version}.%{minor_version}.%{patch_version}
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
Source0: https://s3-eu-west-1.amazonaws.com/v-repositories/images/python-3.4.4-win32.zip

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

%description
Repackaged python 3.4.4 for mingw

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
mkdir -p %{buildroot}%{install_dir}/bin
install python34.dll %{buildroot}%{install_dir}/bin
install python.exe %{buildroot}%{install_dir}/bin
install pythonw.exe %{buildroot}%{install_dir}/bin
install DLLs/python3.dll %{buildroot}%{install_dir}/bin
install DLLs/*.pyd %{buildroot}%{install_dir}/bin

mkdir -p %{buildroot}%{install_dir}/include/python3.4
install -m 644 include/*.h %{buildroot}%{install_dir}/include/python3.4

mkdir -p %{buildroot}%{install_dir}/lib/python3.4
cp -r Lib/* %{buildroot}%{install_dir}/lib/python3.4

install libs/*.lib %{buildroot}%{install_dir}/lib




%files
%{install_dir}

%changelog
* Tue Jun 02 2020 tim.vandermeersch@vortex-financials.be
- Initial release
