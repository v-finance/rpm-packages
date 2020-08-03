# bundle name
%global bundle_name	%{getenv:VORTEX_BUNDLE}
%if "%{bundle_name}" == ""
%global bundle_name	stable
%endif


%if "%{bundle_name}" == "stable"
# upstream version
%global major_version	4
%global minor_version	19
%global patch_version	23
# RPM package release version
%global release_version	1
%endif

%if "%{bundle_name}" == "default"
# upstream version
%global major_version	4
%global minor_version	19
%global patch_version	23
# RPM package release version
%global release_version	1
%endif

Version: %{major_version}.%{minor_version}.%{patch_version}

%global archive_file 	sip-%{version}.tar.gz
%global archive_url 	https://www.riverbankcomputing.com/static/Downloads/sip/%{version}/%{archive_file}
%global archive_dir 	sip-%{version}


%global arch_triplet	%(gcc -dumpmachine)
%global install_dir 	/vortex/%{arch_triplet}/%{bundle_name}

# path to qmake executable
%global qt5_qmake	%{install_dir}/bin/qmake

# ================= IT SHOULD NOT BE NECESSARY TO MAKE CHANGES BELOW ==============================


# ==================
# Top-level metadata
# ==================

Name: vortex-%{bundle_name}-sip
Summary: SIP - Python/C++ Bindings Generator
URL: http://www.riverbankcomputing.com/software/sip/intro
License: GPLv2 or GPLv3 and (GPLv3+ with exceptions)

Release: %{release_version}%{?dist}

# =======================
# Build-time requirements
# =======================

BuildRequires: gcc-c++
BuildRequires: sed
BuildRequires: vortex-%{bundle_name}-python3
BuildRequires: vortex-%{bundle_name}-qt5


# =======================
# Source code and patches
# =======================

%undefine _disable_source_fetch
Source0: %{archive_url}

%if "%{bundle_name}" == "stable"
Patch0: sip-4.19.x-configure-python34.patch
%endif
%if "%{bundle_name}" == "default"
Patch0: sip-4.19.x-configure-python38.patch
%endif

# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

Requires: vortex-%{bundle_name}-python3
Requires: vortex-%{bundle_name}-qt5

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

%patch0 -p1 -b .backup

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
# determine python site-packages directory
%global python_sitedir $(%{install_dir}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')
# determine python include directory
%global python_incdir $(%{install_dir}/bin/python3 -c 'import sysconfig; print(sysconfig.get_paths()["platinclude"])')

# create config.txt file
cat > config.txt << EOF
py_platform=linux-g++
py_inc_dir=%{python_incdir}
py_pylib_dir=%{install_dir}/libs
EOF

echo "config.txt:"
cat config.txt

echo "install_dir:    	%{install_dir}"
echo "python_version: 	%{python_version}"
echo "python_sitedir: 	%{python_sitedir}"
echo "python_incdir: 	%{python_incdir}"

# Configure
%{install_dir}/bin/python3 configure.py \
	--configuration=config.txt \
	--target-py-version=%{python_version} \
	--use-qmake \
	--bindir="%{install_dir}/bin" \
	--destdir="%{python_sitedir}" \
	--incdir="%{python_incdir}" \
	--sipdir="%{install_dir}/share/sip" \
	--stubsdir="%{python_sitedir}" \
	--sip-module=PyQt5.sip \
	--no-dist-info

# Generate makefiles using qmake
%{qt5_qmake}

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
* Wed Jul 29 2020 tim.vandermeersch@vortex-financials.be
- Upgrade stable build to SIP 4.19.23
* Wed Jul 08 2020 tim.vandermeersch@vortex-financials.be
- Add SIP 4.19.23 (bundle_name = test)
* Tue May 26 2020 tim.vandermeersch@vortex-financials.be
- Use bundle name
* Wed May 20 2020 tim.vandermeersch@vortex-financials.be
- Initial version
