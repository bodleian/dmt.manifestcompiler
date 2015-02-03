from setuptools import find_packages
from setuptools import setup

setup(
    name='dmt.manifestcompiler',
    version='1.0',
    namespace_packages=['dmt',],
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
)

