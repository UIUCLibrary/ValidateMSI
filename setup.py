from setuptools import setup
import validate_msi

setup(
    name='CheckRequiredFiles',
    version=validate_msi.__version__,
    url='https://github.com/UIUCLibrary/ValidateMSI',
    license='',
    scripts=['validate_msi.py'],
    install_requires=['PyYAML'],
    author='University of Illinois at Urbana Champaign',
    author_email='hborcher@illinois.edu',
    description='validate msi package'
)
