# upstream version
%global major_version	5
%global minor_version	15
%global patch_version	0
# RPM package release version
%global release_version	1

# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif

# github repository
%global	github_repo	https://github.com/qt/qt5.git
# branch name on github
%global branch_name	5.15

%global arch_triplet	%(gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

# available submodules to build:
#
# SUBMODULE		STATUS
# qtbase		included
# qtsvg			compiles
# qtdeclarative		compiles
# qtactiveqt		compiles
# qtscript		compiles
# qtmultimedia
# qttools
# qtxmlpatterns
# qttranslations
# qtdoc
# qtrepotools
# qtqa
# qtlocation
# qtsensors
# qtsystems
# qtfeedback
# qtdocgallery
# qtpim
# qtconnectivity
# qtwayland
# qt3d
# qtimageformats	included
# qtgraphicaleffects
# qtquickcontrols
# qtserialbus
# qtserialport
# qtx11extras
# qtmacextras
# qtwinextras
# qtandroidextras
# qtwebsockets
# qtwebchannel
# qtwebengine
# qtcanvas3d
# qtwebview
# qtquickcontrols2
# qtpurchasing
# qtcharts
# qtdatavis3d
# qtvirtualkeyboard
# qtgamepad
# qtscxml
# qtspeech
# qtnetworkauth
# qtremoteobjects
# qtwebglplugin
# qtlottie
# qtquicktimeline
# qtquick3d
%global	module_subset	qtbase,qtimageformats

# uncomment these to build examples and/or tests
#%%global examples 1
#%%global tests 1


# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-qt5
Summary: Custom Vortex Qt5 build
URL: https://www.qt.io/
License: LGPL

Version: %{major_version}.%{minor_version}.%{patch_version}
Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: git

%global journald -journald
BuildRequires: pkgconfig(libsystemd)
#BuildRequires: cmake
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
#BuildRequires: pkgconfig(alsa)
# required for -accessibility
#BuildRequires: pkgconfig(atspi-2)
# http://bugzilla.redhat.com/1196359
%global dbus -dbus-linked
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libproxy-1.0)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
%global openssl -openssl-linked
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%global xkbcommon -system-xkbcommon
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires: pkgconfig(xkeyboard-config)
%global egl 1
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(glesv2)
%global sqlite -system-sqlite
BuildRequires: pkgconfig(sqlite3) >= 3.7
BuildRequires: pkgconfig(libpcre2-posix) >= 10.20
BuildRequires: pkgconfig(libpcre) >= 8.0
%global pcre -system-pcre
BuildRequires: pkgconfig(xcb-xkb)
BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires: pkgconfig(zlib)


# =======================
# Source code and patches
# =======================

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

%if 0%{?egl}
Requires: pkgconfig(egl)
%endif
Requires: pkgconfig(gl)
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
Requires: pkgconfig(libinput)
Requires: pkgconfig(xkbcommon)
Requires: pkgconfig(zlib)
Requires: glx-utils

%description
Custom Vortex Qt5 build.

# ======================================================
# The prep phase of the build:
# ======================================================
%prep
cd %{_topdir}/BUILD
# remove old directories
rm -rf qt5 qt5-build
# checkout git repository
git clone %{github_repo} qt5
cd qt5
# checkout the correct branch
git checkout %{branch_name}
# initialize git submodules
./init-repository --module-subset=%{module_subset}


# ======================================================
# Configuring and building the code:
# ======================================================

%build
# create build directory (outside source directory)
mkdir qt5-build
cd qt5-build

%global install_datadir		%{install_dir}/share/qt5
%global install_archdatadir	%{install_dir}/lib/qt5

# configure
../qt5/configure -verbose \
	-opensource \
	-confirm-license \
	-release \
  	-platform linux-g++ \
	-shared \
	-prefix %{install_dir} \
	-archdatadir %{install_archdatadir} \
	-datadir %{install_datadir} \
  	%{!?examples:-nomake examples} \
  	%{!?tests:-nomake tests} \
  	-fontconfig \
	-glib \
	-gtk \
  	-icu \
  	%{?dbus}%{!?dbus:-dbus-runtime} \
	%{?journald} \
	%{?openssl} \
	%{?sqlite} \
	%{?pcre} \
  	-no-pch \
	-no-rpath \
	-no-separate-debug-info \
	-no-strip \
	-system-libjpeg \
	-system-libpng \
	-system-zlib \
	-no-directfb

%make_build

# ======================================================
# Installing the built code:
# ======================================================

%install
rm -rf $RPM_BUILD_ROOT
cd qt5-build
make install INSTALL_ROOT=%{buildroot}

sed -i "s|#\!/usr/bin/python|#\!/usr/bin/python3|g" %{buildroot}%{install_archdatadir}/mkspecs/features/uikit/devices.py

%files
# include all files for now
%{install_dir}



%changelog
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Tue May 19 2020 tim.vandermeersch@vortex-financials.be
- Initial version
- Only building qtbase and qtimageformats
- Still using official Qt github repo, need to change this to our own
