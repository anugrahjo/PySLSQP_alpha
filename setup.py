from setuptools import setup, find_packages
import shutil
import subprocess
import os.path
import sys

def build_meson():
    meson = shutil.which('meson')
    builddir = 'meson_builddir'
    if meson is None:
        raise RuntimeError('meson not found in PATH')
    
    # Remove the old build directory if it exists
    if os.path.exists(builddir):
        shutil.rmtree(builddir)
        import time
        # time.sleep(10)

    subprocess.run([meson, 'setup', builddir], check=True)
    subprocess.run([meson, 'compile', '-C', builddir], check=True)
    build_path = os.path.join(os.getcwd(), builddir, 'pyslsqp')
    target_path = os.path.join(os.getcwd(), 'pyslsqp')

    for root, dirs, files in os.walk(build_path):
        for file in files:
            # For windows
            # if file.endswith('.so') or file.endswith(('.dll.a','.pyd')):
            if file.endswith('.so'):
                from_path = os.path.join(root, file)
                to_path = os.path.join(target_path, file)
                shutil.copy(from_path, to_path)
        # For windows
        # for dir in dirs:
        #     if dir.endswith('.pyd.p'):
        #         from_path = os.path.join(root, dir)
        #         to_path = os.path.join(target_path, dir)
        #         if not os.path.exists(to_path):
        #             shutil.copytree(from_path, to_path)

if __name__ == "__main__":
    
    # `build_meson()`` function is only called when the `setup.py`` script is not invoked with the sdist or egg_info command. 
    # This prevents the Fortran compilation using Meson from happening when generating the source distribution.
    # But it will still be executed when installing the package from the source distribution or building the wheel distribution.
    if not ('sdist' in sys.argv or 'egg_info' in sys.argv):
        build_meson()

    setup(
        name='pyslsqp',
        # include_package_data=True,
        package_data={'pyslsqp': ['*.so']}, # this is needed to include the shared object file in the build directory in site-pkgs
        # platforms=["Linux, Windows", "Mac OS X", "Unix", "POSIX", "Any"],
    )
