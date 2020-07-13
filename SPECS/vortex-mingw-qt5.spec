# MinGW header
%{?mingw_package_header}

# build 32-bit only
%global mingw_build_win64 0

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

# upstream version
%global major_version	5
%global minor_version	15
%global patch_version	0
# RPM package release version
%if "%{bundle_name}" == "stable"
%global release_version	2
%endif
%if "%{bundle_name}" == "default"
%global release_version	3
%endif


# github repository
%global	github_repo	https://github.com/qt/qt5.git
# branch name on github
%global branch_name	v5.15.0

# Use this to compile from tar.gz
#%%undefine _disable_source_fetch
#Source0:        qt5-%{version}.tar.gz

%global arch_triplet	%(i686-w64-mingw32-gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

%if "%{bundle_name}" == "stable"
%global	module_subset	qtbase,qtimageformats,qttools,qttranslations
%endif

%if "%{bundle_name}" == "default"
%global	module_subset	qtbase,qtimageformats,qttools,qttranslations,qtdeclarative,qtactiveqt
%endif

# uncomment these to build examples and/or tests
#%%global examples 1
#%%global tests 1


# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================

# Avoid duplicate build-id files between bundles
%global _build_id_links none

# ==================
# Top-level metadata
# ==================

Name:           vortex-%{bundle_name}-mingw-qt5
Summary:        Custom Vortex Qt5 build for windows using MinGW
URL:            https://www.qt.io
License:        LGPL

Version: %{major_version}.%{minor_version}.%{patch_version}
Release: %{release_version}%{?dist}


# =======================
# Build-time requirements
# =======================

BuildRequires:	which
BuildRequires:	perl
BuildRequires:	git

BuildRequires:  mingw32-filesystem >= 110
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-openssl

# =======================
# Source code and patches
# =======================

%if "%{bundle_name}" == "default"
Patch0: qt5-5.15.0-qtdeclarative.patch
Patch1: qt5-5.15.0-qtactiveqt.patch
%endif

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

%description
Custom Vortex Qt5 build for windows using MinGW.

# Win32
%package -n vortex-%{bundle_name}-mingw32-qt5
Summary:	MinGW compiled Qt5 library for the Win32 target
BuildArch:      noarch

%description -n vortex-%{bundle_name}-mingw32-qt5
MinGW compiled Qt5 library for the Win32 target.

# Tools (qmake, ...)
%package -n vortex-%{bundle_name}-mingw32-qt5-tools
Summary:       	Tools for MinGW compiled Qt5 library for the Win32 target
Requires:	vortex-%{bundle_name}-mingw32-qt5

%description -n vortex-%{bundle_name}-mingw32-qt5-tools
Tools for MinGW compiled Qt5 library for the Win32 target.

# ======================================================
# The prep phase of the build:
# ======================================================

# This is required to supress rpmbuild error for files section
%global debug_package %{nil}

%prep
echo "bundle: %{bundle_name}"
cd %{_topdir}/BUILD
# remove old directories
rm -rf qt5-mingw qt5-mingw-build
# checkout git repository
git clone %{github_repo} qt5-mingw
cd qt5-mingw
# checkout the correct branch
git checkout %{branch_name}
# initialize git submodules
./init-repository --module-subset=%{module_subset}

%if "%{bundle_name}" == "default"
cd qtdeclarative
%patch0 -p1 -b .backup
cd ../qtactiveqt
%patch1 -p1 -b .backup
%endif

# ======================================================
# Configuring and building the code:
# ======================================================

%build
%global install_datadir		%{install_dir}/share/qt5
%global install_archdatadir	%{install_dir}/lib/qt5


cd qt5-mingw # needed when compiling from git

mkdir build_win32
pushd build_win32

%if "%{bundle_name}" == "stable"
../configure -verbose \
	-opensource \
	-confirm-license \
	-release \
	-xplatform win32-g++ \
	-device-option CROSS_COMPILE=i686-w64-mingw32- \
	-nomake examples \
	-nomake tests \
	-prefix %{install_dir} \
	-archdatadir %{install_archdatadir} \
	-datadir %{install_datadir} \
	-opengl desktop \
	-no-feature-sqlmodel \
	-no-sql-sqlite \
	-no-sql-odbc
%endif

%if "%{bundle_name}" == "default"
../configure -verbose \
	-opensource \
	-confirm-license \
	-release \
	-xplatform win32-g++ \
	-device-option CROSS_COMPILE=i686-w64-mingw32- \
	-nomake examples \
	-nomake tests \
	-prefix %{install_dir} \
	-archdatadir %{install_archdatadir} \
	-datadir %{install_datadir} \
	-no-opengl \
	-no-feature-sqlmodel \
	-no-sql-sqlite \
	-no-sql-odbc
%endif

popd

alias python=python3
%mingw_make %{?_smp_mflags}

# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT ; cd qt5-mingw # needed when compiling from git

%mingw_make install INSTALL_ROOT=%{buildroot}

sed -i "s|#\!/usr/bin/python|#\!/usr/bin/python3|g" %{buildroot}%{install_archdatadir}/mkspecs/features/uikit/devices.py


%files -n vortex-%{bundle_name}-mingw32-qt5
%dir %{install_dir}/bin
%{install_dir}/bin/Qt5Concurrent.dll
%{install_dir}/bin/Qt5Core.dll
%{install_dir}/bin/Qt5DBus.dll
%{install_dir}/bin/Qt5Gui.dll
%{install_dir}/bin/Qt5Help.dll
%{install_dir}/bin/Qt5Network.dll
%{install_dir}/bin/Qt5PrintSupport.dll
%{install_dir}/bin/Qt5Sql.dll
%{install_dir}/bin/Qt5Test.dll
%{install_dir}/bin/Qt5Widgets.dll
%{install_dir}/bin/Qt5Xml.dll
%if "%{bundle_name}" == "stable"
%{install_dir}/bin/Qt5OpenGL.dll
%endif
%if "%{bundle_name}" == "default"
%{install_dir}/bin/Qt5Qml.dll
%{install_dir}/bin/Qt5QmlModels.dll
%{install_dir}/bin/Qt5QmlWorkerScript.dll
%{install_dir}/bin/Qt5Quick.dll
%{install_dir}/bin/Qt5QuickShapes.dll
%{install_dir}/bin/Qt5QuickTest.dll
%{install_dir}/bin/Qt5QuickWidgets.dll
%endif
%{install_dir}/include
%{install_dir}/lib
%{install_dir}/share






%files -n vortex-%{bundle_name}-mingw32-qt5-tools
%dir %{install_dir}/bin
%{install_dir}/bin/fixqt4headers.pl
%{install_dir}/bin/lconvert
%{install_dir}/bin/lprodump
%{install_dir}/bin/lrelease
%{install_dir}/bin/lrelease-pro
%{install_dir}/bin/lupdate
%{install_dir}/bin/lupdate-pro
%{install_dir}/bin/moc
%{install_dir}/bin/qdbus.exe
%{install_dir}/bin/qdbuscpp2xml
%{install_dir}/bin/qdbusviewer.exe
%{install_dir}/bin/qdbusxml2cpp
%{install_dir}/bin/qlalr
%{install_dir}/bin/qmake
%{install_dir}/bin/qtattributionsscanner
%{install_dir}/bin/qtdiag.exe
%{install_dir}/bin/qtpaths.exe
%{install_dir}/bin/qtplugininfo.exe
%{install_dir}/bin/qvkgen
%{install_dir}/bin/rcc
%{install_dir}/bin/syncqt.pl
%{install_dir}/bin/tracegen
%{install_dir}/bin/uic
%{install_dir}/bin/windeployqt
%if "%{bundle_name}" == "default"
%{install_dir}/bin/qml.exe
%{install_dir}/bin/qmlcachegen
%{install_dir}/bin/qmlformat
%{install_dir}/bin/qmlimportscanner
%{install_dir}/bin/qmllint
%{install_dir}/bin/qmlmin
%{install_dir}/bin/qmlpreview.exe
%{install_dir}/bin/qmlscene.exe
%{install_dir}/bin/qmltestrunner.exe
%{install_dir}/bin/qmltyperegistrar
%{install_dir}/bin/dumpcpp.exe
%{install_dir}/bin/dumpdoc.exe
%endif

%changelog
* Tue Jul 07 2020 tim.vandermeersch@vortex-financials.be
- Add qtdeclarative module and -no-opengl (bundle_name = test)
* Wed Jun 17 2020 tim.vandermeersch@vortex-financials.be
- Release 2
- Include qttools & qttranslations
* Tue Jun 02 2020 tim.vandermeersch@vortex-financials.be
- Initial release
