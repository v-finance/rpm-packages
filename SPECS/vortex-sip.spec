# sip version
%global major_version	4
%global minor_version	19
%global patch_version	22
# RPM package release version
%global release_version	1

Version: %{major_version}.%{minor_version}.%{patch_version}

%global archive_file sip-%{version}.tar.gz
%global archive_url https://www.riverbankcomputing.com/static/Downloads/sip/%{version}/%{archive_file}
%global archive_dir sip-%{version}

# python package to use (e.g. python-3.4.4-default for vortex-python-3.4.4-default...rpm)
%global python_package	%{getenv:VORTEX_PYTHON_PACKAGE}
%global python_root 	/vortex/%{python_package}

%global qt5_root	/vortex/Qt-5.15.0

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{python_package}-sip
Summary: SIP - Python/C++ Bindings Generator
URL: http://www.riverbankcomputing.com/software/sip/intro
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{python_package}
BuildRequires: vortex-qt5


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}

%if "%{version}" == "4.19.22"
Patch0: sip-4.19.22-configure.patch
%endif

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{python_package}
Requires: vortex-qt5

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

%if "%{version}" == "4.19.22"
%patch0 -p1 -b .backup
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archive_dir}

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{python_root}/lib"
# determine python version (e.g. 3.4)
%global python_version $(%{python_root}/bin/python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python site-packages directory
%global python_sitedir $(%{python_root}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
# determine python include directory
%global python_incdir $(%{python_root}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["platinclude"])')

# create config.txt file
cat > config.txt << EOF
py_platform=linux-g++
py_inc_dir=%{python_incdir}
py_pylib_dir=%{python_root}/libs
EOF

echo "config.txt:"
cat config.txt

echo "python_root:    	%{python_root}"
echo "python_version: 	%{python_version}"
echo "python_sitedir: 	%{python_sitedir}"
echo "python_incdir: 	%{python_incdir}"
echo
echo
echo

# Configure
%{python_root}/bin/python3 configure.py \
	--configuration=config.txt \
	--target-py-version=%{python_version} \
	--use-qmake \
	--bindir="%{python_root}/bin" \
	--destdir="%{python_sitedir}" \
	--incdir="%{python_incdir}" \
	--sipdir="%{python_root}/share/sip" \
	--stubsdir="%{python_sitedir}" \
	--sip-module=PyQt5.sip \
	--no-dist-info

# Generate makefiles using qmake
%{qt5_root}/bin/qmake

# Build using make
%make_build

# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd %{archive_dir}
make INSTALL_ROOT=%{buildroot} INSTALL="install -p" install


%files
# include all files for now
%{python_root}



%changelog
* Wed May 20 2020 tim.vandermeersch@vortex-financials.be
- Initial version
