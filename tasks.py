from invoke import task
import os

def get_specs_dir():
    """
    Helper function to get the SPECS directory.
    """
    # find directory containing the SPEC files
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    specs_dir = os.path.join(script_dir, 'SPECS')
    return specs_dir

def copy_patches():
    """
    Helper function to copy patches to $HOME/rpmbuild/SOURCES.
    """
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    os.system("cp {}/patches/*.patch ~/rpmbuild/SOURCES".format(script_dir))


def get_spec_path(package):
    """
    Helper function to get the path to a SPEC file from a package name.
    """
    return os.path.join(get_specs_dir(), package + '.spec')


def get_packages():
    """
    Helper function to find packages in SPECS directory.
    """
    # find spec files
    packages = []
    for item in os.listdir(get_specs_dir()):
        if item.endswith('.spec'):
            packages.append(item[:-len('.spec')])
    return packages


@task
def list_packages(ctx):
    """
    List the available packages.
    """
    for package in get_packages():
        print(package)

@task
def install_build_deps(ctx, package):
    """
    Install the build dependencies for a package.
    """
    if package not in get_packages():
        print("Package {} not found. Available packages:".format(package))
        list_packages(ctx)
        return

    print("Installing build dependencies for package {}".format(package))
    # FIXME: Get rid of sudo using mock?
    ctx.run("sudo dnf -y builddep {}".format(get_spec_path(package)))


@task
def build_package(ctx, package):
    """
    Build the RPM package.
    """
    if package not in get_packages():
        print("Package {} not found. Available packages:".format(package))
        list_packages(ctx)
        return

    print("Building package: {}".format(package))

    # make sure the $HOME/rpmbuild directories exist
    ctx.run("rpmdev-setuptree")
    copy_patches()
    ctx.run("rpmbuild -bb {}".format(get_spec_path(package)))

@task
def build_source_package(ctx, package):
    """
    Build the RPM source package.
    """
    if package not in get_packages():
        print("Package {} not found. Available packages:".format(package))
        list_packages(ctx)
        return

    print("Building source package: {}".format(package))

    # make sure the $HOME/rpmbuild directories exist
    ctx.run("rpmdev-setuptree")
    copy_patches()
    ctx.run("rpmbuild -bs {}".format(get_spec_path(package)))


def clean_rpm_packages(arch='x86_64'):
    """
    Delete packages from $HOME/rpmbuild/RPMS/<arch> directory.
    """
    os.system("rm {}".format(os.path.join(os.path.join("~/rpmbuild/RPMS", arch), "*.rpm")))

def get_rpm_packages(arch='x86_64'):
    """
    Get a list of RPM packages in the $HOME/rpmbuild/RPMS/<arch> directory.
    """
    packages = []
    rpms_path = os.path.join(os.path.expanduser('~'), os.path.join("rpmbuild/RPMS", arch))
    for item in os.listdir(rpms_path):
        if item.endswith(".rpm"):
            packages.append(os.path.join(rpms_path, item))
    return packages

def find_newly_build_rpm_package(old_rpms, new_rpms):
    """
    Find RPM package in new_rpms that is not in old_rpms list.
    """
    for rpm in new_rpms:
        if rpm not in old_rpms:
            return rpm


@task
def build_all_packages(ctx):
    """
    Build and install all the RPM packages. Installation is needed since there are dependencies between packages.
    """
    # packages in correct (dependency) order
    packages = [
        'vortex-openssl',
        'vortex-python3',
        'vortex-qt5',
        'vortex-sip',
        'vortex-pyqt5'
    ]

    print("Building all packages")

    # remove previously build RPMS
    clean_rpm_packages()

    for package in packages:
        # install build dependencies
        install_build_deps(ctx, package)
        # build the package
        old_rpms = get_rpm_packages()
        build_package(ctx, package)
        new_rpms = get_rpm_packages()
        # install the package
        rpm = find_newly_build_rpm_package(old_rpms, new_rpms)
        if rpm:
            # upgrade is same as install but replaces older versions if needed
            os.system("sudo rpm --upgrade '{}'".format(rpm))


@task
def build_all_source_packages(ctx):
    """
    Build all the RPM source packages.
    """
    # delete sources to ensure we have the latest version
    ctx.run("rm ~/rpmbuild/SOURCES/*")
    # build source RPMs
    for package in get_packages():
        build_source_package(ctx, package)


@task
def mock_build_packages(ctx):
    """
    Build all the RPM packages using mock. This does not require root privileges
    but the user needs to be in the mock group.
    """
    # delete old source RPMs
    ctx.run("rm ~/rpmbuild/SRPMS/*")
    # rebuild all source RPMs
    build_all_source_packages(ctx)
    # create list with source RPMs
    packages = []
    srpms_path = os.path.join(os.path.expanduser('~'), "rpmbuild/SRPMS")
    for item in os.listdir(srpms_path):
        if item.endswith('.src.rpm'):
            packages.append(os.path.join(srpms_path, item))
    # run mock with options:
    #   --chain             build packages that depend on each other
    #   --recurse           retry until all packages build successfully
    #   --enable-network    make sure we can access github
    ctx.run("mock --enable-network --recurse --chain {}".format(" ".join(packages)))

