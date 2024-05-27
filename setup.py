from setuptools import setup, find_packages
import shutil
import subprocess
import os.path

def build_meson():
    meson = shutil.which('meson')
    builddir = 'meson_builddir'
    if meson is None:
        raise RuntimeError('meson not found in PATH')
    subprocess.run([meson, 'setup', builddir])
    subprocess.run([meson, 'compile', '-C', builddir])
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
    build_meson()

    setup(
        name='pyslsqp',
        packages=find_packages(where="."),
        # package_dir={"": "pyslsqp"},
        # include_package_data=True,
        package_data={'pyslsqp': ['*.so']}, # this is needed to include the shared object file in the build directory in site-pkgs
        # platforms=["Linux, Windows", "Mac OS X", "Unix", "POSIX", "Any"],
    )
