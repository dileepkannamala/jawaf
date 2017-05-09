#!/usr/bin/env python3
from setuptools import find_packages, setup

version = __import__('jawaf').__version__

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    author='Dan Pozmanter',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    description='Asynchronous Web Application Framework',    
    entry_points={'console_scripts': [
        'jawaf-admin = jawaf.management:execute_from_command_line',
    ]},
    include_package_data=True,
    keywords='web framework',
    license='BSD',
    long_description=long_description,
    name='Jawaf',
    packages=find_packages(),
    scripts=['jawaf/bin/jawaf-admin.py'],
    url='https://github.com/danpozmanter/jawaf',
    version=version,
    zip_safe=False,
    )