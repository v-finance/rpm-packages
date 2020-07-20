# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif


# upstream version
%global major_version	4
%global minor_version	2
%global patch_version	4
# RPM package release version
%global release_version	1


Version: %{major_version}.%{minor_version}.%{patch_version}

%global archive_file 	lxml-%{version}.tar.gz
%global archive_url 	https://files.pythonhosted.org/packages/ca/63/139b710671c1655aed3b20c1e6776118c62e9f9311152f4c6031e12a0554/%{archive_file}
%global archive_dir 	lxml-%{version}


%global arch_triplet	%(i686-w64-mingw32-gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

%global host_arch_triplet	%(gcc -dumpmachine)
%global host_install_dir 	/vortex/%{host_arch_triplet}/%{bundle_name}

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-ming32-python3-lxml
Summary: The lxml python module
URL: http://lxml.de/
License: BSD

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildArch:      noarch

BuildRequires:  mingw32-filesystem >= 110
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-gettext

BuildRequires:  mingw32-libxml2
BuildRequires:  mingw32-libxslt
BuildRequires:  mingw32-libgcrypt
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-libgpg-error


BuildRequires:  vortex-%{bundle_name}-mingw32-python3


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}

Source1: mingw-toolchain.cmake
Source2: lxml-4.2.4-CMakeLists.txt

Patch0: lxml-4.2.4-setup.patch

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-mingw32-python3

%description
Custom Vortex lxml python module build.

# ======================================================
# The prep phase of the build:
# ======================================================
%prep
cd %{_topdir}/BUILD
rm -rf %{archive_dir}
tar zxvf %{_topdir}/SOURCES/%{archive_file}
cd %{archive_dir}

%patch0 -p1 -b .backup

cp %{SOURCE1} .
cp %{SOURCE2} CMakeLists.txt

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archive_dir}

%if "%{bundle_name}" == "stable"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{host_install_dir}/lib"
%endif

%{host_install_dir}/bin/python3 setup.py bdist_wheel \
    -- \
    -DCMAKE_TOOLCHAIN_FILE=%{SOURCE1} \
    -DLIBXML2_INCLUDE_DIR=/usr/i686-w64-mingw32/sys-root/mingw/include/libxml2 \
    -DLIBXML2_LIBRARY=/usr/i686-w64-mingw32/sys-root/mingw/bin/libxml2-2.dll \
    -DLIBXSLT_INCLUDE_DIR=/usr/i686-w64-mingw32/sys-root/mingw/include/libxslt \
    -DLIBXSLT_LIBRARIES=/usr/i686-w64-mingw32/sys-root/mingw/bin/libxslt-1.dll \
    -DLIBXSLT_EXSLT_LIBRARY=/usr/i686-w64-mingw32/sys-root/mingw/bin/libexslt-0.dll \
    -DPYTHON_INCLUDE_DIR=/vortex/i686-w64-mingw32/default/include/python3.8 \
    -DPYTHON_LIBRARY=/vortex/i686-w64-mingw32/default/bin/python38.dll \
    -- \
    VERBOSE=1



# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archive_dir}

# determine python version (e.g. 3.4)
%global python_version $(%{host_install_dir}/bin/python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')

mkdir -p %{buildroot}%{install_dir}/lib/python%{python_version}
unzip dist/lxml-%{version}-cp38-cp38-linux_x86_64.whl -d %{buildroot}%{install_dir}/lib/python%{python_version}


%files
# include all files for now
%{install_dir}


%changelog
* Mon Jul 20 2020 tim.vandermeersch@vortex-financials.be
- Initial version
