from setuptools import setup

setup(
    name='CheckRequiredFiles',
    version='0.0.1',
    url='https://github.com/UIUCLibrary/ValidateMSI',
    license='',
    scripts=['validate_msi.py'],
    install_requires=['PyYAML'],
    author='University of Illinois at Urbana Champaign',
    author_email='hborcher@illinois.edu',
    description='validate msi package'
)
