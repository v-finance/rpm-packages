# MinGW header
%{?mingw_package_header}

# build 32-bit only
%global mingw_build_win64 0

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

%if "%{bundle_name}" == "stable"
# upstream version
%global major_version	5
%global minor_version	13
%global patch_version	2
# RPM package release version
%global release_version	3
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
%global archive_file 	PyQt5-5.13.2.tar.gz
%global archive_url 	https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.2/%{archive_file}
%global archive_dir 	PyQt5-5.13.2
%endif

%if "%{bundle_name}" == "default"
%global archive_file 	PyQt5-5.15.0.tar.gz
%global archive_url 	https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/%{archive_file}
%global archive_dir 	PyQt5-5.15.0
%endif

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

Name: vortex-%{bundle_name}-mingw32-pyqt5
Summary: Python Bindings for Qt5
URL: http://www.riverbankcomputing.com/software/pyqt/intro
License: GPLv3

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: mingw32-gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{bundle_name}-sip
BuildRequires: vortex-%{bundle_name}-mingw32-sip


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
Patch2: pyqt5-5.13.2-configure.patch
Patch3: pyqt5-5.13.2-wswin.patch
%endif

%if "%{version}" == "5.15.0"
Patch0: pyqt5-5.15.0-mingw32.patch
%endif


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-mingw32-sip

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
%patch2 -p1 -b .backup
%patch3 -p1 -b .backup
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
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{host_install_dir}/lib"
%endif

# determine python version (e.g. 3.4)
%global python_version $(%{host_install_dir}/bin/python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')
# determine python short version (e.g. 34)
%global python_short_version $(%{host_install_dir}/bin/python3 -c 'import sys; print("{}{}".format(sys.version_info.major, sys.version_info.minor))')

%if "%{bundle_name}" == "stable"

# create config.txt file
cat > config.txt << EOF
py_platform=win32-g++
py_inc_dir=%{install_dir}/include/python%{python_version}
py_pylib_dir=%{install_dir}/lib
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
%{host_install_dir}/bin/python3 configure.py \
	--verbose \
	--confirm-license \
	--no-dist-info \
	--no-stubs \
	--no-sip-files \
	--disable-feature=sqlmodel \
	--disable=QtSql \
	--target-py-version=%{python_version} \
	--qmake %{qt5_qmake} \
	--sip %{host_install_dir}/bin/sip \
	--configuration=config.txt \
	-b %{install_dir}/bin \
	-d %{install_dir}/lib/python%{python_version}/site-packages \
	QMAKE_CXXFLAGS+=-D_hypot=hypot

%endif

%if "%{bundle_name}" == "default"

# create config.txt file
cat > config.txt << EOF
py_platform=win32
py_inc_dir=%{install_dir}/include/python%{python_version}
py_pylib_dir=%{install_dir}/lib
py_pylib_lib=python%{python_short_version}
qt_shared=True

[Qt 5.15]
EOF

# Configure
PATH=%{host_install_dir}/bin:$PATH %{host_install_dir}/bin/python3 configure.py \
	--verbose \
	--confirm-license \
	--no-dist-info \
	--no-stubs \
	--no-sip-files \
	--qmake %{qt5_qmake} \
	--sip %{host_install_dir}/bin/sip \
	--disable QtSql \
	--disable-feature PyQt_OpenGL \
	--disable-feature PyQt_Desktop_OpenGL \
	--configuration=config.txt \
	-b %{install_dir}/bin \
	-d %{install_dir}/lib/python%{python_version}/site-packages


#PATH=/vortex/i686-w64-mingw32/test/bin:/vortex/x86_64-redhat-linux/test/bin:$PATH /vortex/x86_64-redhat-linux/test/bin/python3 configure.py --verbose --confirm-license --qmake /vortex/i686-w64-mingw32/test/bin/qmake --sip /vortex/x86_64-redhat-linux/test/bin/sip5 --disable-feature PyQt_Desktop_OpenGL --disable-feature PyQt_OpenGL --configuration=config.txt --disable QtSql

%endif

# Build using make
%mingw32_make %{?_smp_mflags}

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
* Wed Jun 17 2020 tim.vandermeersch@vortex-financials.be
- Release 2
- Use mingw32 as package name for consistency
* Tue Jun 16 2020 tim.vandermeersch@vortex-financials.be
- Initial version
