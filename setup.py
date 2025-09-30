from setuptools import setup, find_packages


from dslpipe import __version__

setup(
    name = 'dslpipe',
    version = __version__,

    packages = find_packages(),
    scripts = ['scripts/dslpipe'],
    
    install_requires=[
        'numpy',
        'h5py',
        'caput',
        'matplotlib',
    ],

    # metadata for upload to PyPI
    author = "Shifan Zuo",
    author_email = "sfzuo@bao.ac.cn",
    description = "DSL data processing pipeline.",
    license = "GPL v3.0",
    url = "https://github.com/DSL-SDP/dslpipe",
)
