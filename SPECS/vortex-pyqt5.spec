# PyQt5 version
%global major_version	5
%global minor_version	13
%global patch_version	2
# RPM package release version
%global release_version	1

Version: %{major_version}.%{minor_version}.%{patch_version}

# Qt/PyQt 5.15.0 is not released yet, use dev version for now
#%%global archive_file 	PyQt5-5.15.0.dev2005181617.tar.gz
#%%global archive_url 	https://www.riverbankcomputing.com/static/Downloads/PyQt5/%{archive_file}
#%%global archive_dir 	PyQt5-5.15.0.dev2005181617
# use version 5.13.2 for now...
%global archive_file 	PyQt5-5.13.2.tar.gz
%global archive_url 	https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.2/%{archive_file}
%global archive_dir 	PyQt5-5.13.2

# python package to use (e.g. python-3.4.4-default for vortex-python-3.4.4-default...rpm)
%global python_package	%{getenv:VORTEX_PYTHON_PACKAGE}
%global python_root 	/vortex/%{python_package}

%global qt5_root	/vortex/Qt-5.15.0

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{python_package}-pyqt5
Summary: Python Bindings for Qt5
URL: http://www.riverbankcomputing.com/software/pyqt/intro
License: GPLv3

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{python_package}-sip


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{python_package}-sip

%description
Custom Vortex PyQt5 build.

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

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{python_root}/lib:%{qt5_root}/lib"
# determine python version (e.g. 3.4)
%global python_version $(%{python_root}/bin/python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python short version (e.g. 34)
%global python_short_version $(%{python_root}/bin/python3 -c 'import sys; print("{}{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python site-packages directory
%global python_sitedir $(%{python_root}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
# determine python include directory
%global python_incdir $(%{python_root}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["platinclude"])')

# create config.txt file
#
# qt_static=False --> qt_shared=True
# pyqt_modules = QAxContainer --> removed, windows only
cat > config.txt << EOF
py_platform=linux-g++
py_inc_dir=%{python_incdir}
py_pylib_dir=%{python_root}/libs
py_pylib_lib=python%{python_short_version}
qt_shared=True

[Qt 5.15]
EOF


echo "config.txt:"
cat config.txt

echo "python_root:    	%{python_root}"
echo "python_version: 	%{python_version}"
echo "python_sitedir: 	%{python_sitedir}"
echo "python_incdir: 	%{python_incdir}"

# Configure
%{python_root}/bin/python3 configure.py \
	--verbose \
	--confirm-license \
	--target-py-version=%{python_version} \
	--qmake %{qt5_root}/bin/qmake \
	--sip %{python_root}/bin/sip \
	--configuration=config.txt \
	--no-dist-info


# Generate makefiles using qmake
#%%{qt5_root}/bin/qmake

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
