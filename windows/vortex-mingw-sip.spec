# MinGW header
%{?mingw_package_header}

# build 32-bit only
%global mingw_build_win64 0

# upstream version
%global major_version	4
%global minor_version	19
%global patch_version	22
# RPM package release version
%global release_version	1

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

Version: %{major_version}.%{minor_version}.%{patch_version}

%global archive_file 	sip-%{version}.tar.gz
%global archive_url 	https://www.riverbankcomputing.com/static/Downloads/sip/%{version}/%{archive_file}
%global archive_dir 	sip-%{version}

%global arch_triplet	%(i686-w64-mingw32-gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

%global host_arch_triplet	%(gcc -dumpmachine)
%global host_install_dir 	/vortex/%{host_arch_triplet}/%{bundle_name}

# path to qmake executable
%global qt5_qmake	%{install_dir}/bin/qmake

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-mingw-sip
Summary: SIP - Python/C++ Bindings Generator
URL: http://www.riverbankcomputing.com/software/sip/intro
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{bundle_name}-mingw32-python3
BuildRequires: vortex-%{bundle_name}-mingw32-qt5
BuildRequires: vortex-%{bundle_name}-mingw32-qt5-tools


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}

Source1: mingw-win32-g++

%if "%{version}" == "4.19.22"
Patch0: sip-4.19.22-configure.patch
%endif

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-mingw32-python3
Requires: vortex-%{bundle_name}-mingw32-qt5

%description
Custom Vortex sip build.

# ======================================================
# The prep phase of the build:
# ======================================================
%prep
cd %{_topdir}/BUILD
rm -rf %{archive_dir}
tar zxvf %{_topdir}/SOURCES/%{archive_file}
cd %{archive_dir}

cp -a %{SOURCE1} specs/mingw-win32-g++

%if "%{version}" == "4.19.22"
%patch0 -p1 -b .backup
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
function genConfig() {
    target=$1
    pyver=$2
    cat > ${target}_${pyver}.host.config <<EOF
py_inc_dir=%{install_dir}/include/python$pyver
py_pylib_dir=%{install_dir}/lib
sip_module_dir=%{install_dir}/bin
EOF
    echo ${target}_${pyver}.host.config
}

cd %{archive_dir}

mkdir build_mingw32
pushd build_mingw32

LD_LIBRARY_PATH=%{host_install_dir}/lib %{host_install_dir}/bin/python3 ../configure.py \
        --use-qmake \
	--no-tools \
	--no-dist-info \
	--no-stubs \
        -p mingw-win32-g++ \
        --configuration=`genConfig %{mingw32_target} 3.4`

%{qt5_qmake}

%mingw32_make %{?_smp_mflags}

popd


# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archive_dir}

pushd build_mingw32
make INSTALL_ROOT=%{buildroot} INSTALL="install -p" install
popd

%files
# include all files for now
%{install_dir}



%changelog
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Wed May 20 2020 tim.vandermeersch@vortex-financials.be
- Initial version
