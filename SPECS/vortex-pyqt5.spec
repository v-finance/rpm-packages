# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

%if "%{bundle_name}" == "stable"
# upstream version
%global major_version	5
%global minor_version	15
%global patch_version	0
# RPM package release version
%global release_version	2
%endif

%if "%{bundle_name}" == "default"
# upstream version
%global major_version	5
%global minor_version	15
%global patch_version	0
# RPM package release version
%global release_version	1
%endif

Version: %{major_version}.%{minor_version}.%{patch_version}

%if "%{bundle_name}" == "stable"
%global archive_file 	PyQt5-5.15.0.tar.gz
%global archive_url 	https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/%{archive_file}
%global archive_dir 	PyQt5-5.15.0
%endif

%if "%{bundle_name}" == "default"
%global archive_file 	PyQt5-5.15.0.tar.gz
%global archive_url 	https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/%{archive_file}
%global archive_dir 	PyQt5-5.15.0
%endif

%global arch_triplet	%(gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

# path to qmake executable
%global qt5_qmake	%{install_dir}/bin/qmake

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-pyqt5
Summary: Python Bindings for Qt5
URL: http://www.riverbankcomputing.com/software/pyqt/intro
License: GPLv3

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{bundle_name}-sip


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}

# Qt 5.15.0 methods:
# - void setDocumentXmpMetadata(const QByteArray &xmpMetadata);
# - QByteArray documentXmpMetadata() const;
# - void addFileAttachment(const QString &fileName, const QByteArray &data, const QString &mimeType = QString());
%if "%{version}" == "5.13.2"
Patch0: pyqt5-5.13.2-qcoremod.patch
Patch1: pyqt5-5.13.2-qpdfwriter.patch
%endif

%if "%{version}" == "5.15.0"
Patch0: pyqt5-5.15.0-linux.patch
%endif

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-sip

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

%if "%{version}" == "5.13.2"
%patch0 -p0 -b .backup
%patch1 -p1 -b .backup
%endif

%if "%{version}" == "5.15.0"
%patch0 -p1 -b .backup
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
cd %{archive_dir}

%if "%{bundle_name}" == "stable"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{install_dir}/lib"
%endif

# determine python version (e.g. 3.4)
%global python_version $(%{install_dir}/bin/python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python short version (e.g. 34)
%global python_short_version $(%{install_dir}/bin/python3 -c 'import sys; print("{}{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python site-packages directory
%global python_sitedir $(%{install_dir}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
# determine python include directory
%global python_incdir $(%{install_dir}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["platinclude"])')

# create config.txt file
#
# qt_static=False --> qt_shared=True
# pyqt_modules = QAxContainer --> removed, windows only
cat > config.txt << EOF
py_platform=linux-g++
py_inc_dir=%{python_incdir}
py_pylib_dir=%{install_dir}/libs
py_pylib_lib=python%{python_short_version}
qt_shared=True

[Qt 5.15]
EOF


echo "config.txt:"
cat config.txt

echo "install_dir:    	%{install_dir}"
echo "python_version: 	%{python_version}"
echo "python_sitedir: 	%{python_sitedir}"
echo "python_incdir: 	%{python_incdir}"

# Configure
%{install_dir}/bin/python3 configure.py \
	--verbose \
	--confirm-license \
	--target-py-version=%{python_version} \
	--qmake %{qt5_qmake} \
	--sip %{install_dir}/bin/sip \
	--configuration=config.txt \
	--no-dist-info


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
%{install_dir}



%changelog
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Wed May 20 2020 tim.vandermeersch@vortex-financials.be
- Initial version
