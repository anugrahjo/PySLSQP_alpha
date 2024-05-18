from setuptools import setup, find_packages
import shutil
import subprocess
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

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
            if file.endswith('.so'):
                from_path = os.path.join(root, file)
                to_path = os.path.join(target_path, file)
                shutil.copy(from_path, to_path)

if __name__ == "__main__":
    build_meson()

    setup(
        name='pyslsqp',
        version=get_version('pyslsqp/__init__.py'),
        author='Author name',
        author_email='author@gmail.com',
        license='BSD-3-Clause',
        # TODO: Add the correct keywords and license
        keywords='slsqp optimization scipy',
        url='http://github.com/LSDOlab/pyslsqp',
        download_url='http://pypi.python.org/pypi/pyslsqp',
        description="A Python wrapper for the SLSQP optimization algorithm",
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages(where="."),
        # package_dir={"": "pyslsqp"},
        # include_package_data=True,
        package_data={'': ['*.so']},
        python_requires='>=3.7',
        # platforms=["Linux, Windows", "Mac OS X", "Unix", "POSIX", "Any"],
        # TODO: Add the correct classifiers license, platforms, and install_requires version requirements
        install_requires=["numpy>=1.16", "h5py>=2.10", "matplotlib>=3.4"],
                        #   "plotly", "dash", "ipywidgets"],
        classifiers=[
            'Development Status :: 4 - Beta',
            # 'Development Status :: 5 - Production/Stable',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Education',
            'Natural Language :: English',
            'Topic :: Education',
            'Topic :: Education :: Computer Aided Instruction (CAI)',
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Mathematics',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries',
        ],
    )
