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

