#!/usr/bin/env python3
from setuptools import setup

setup(
    author='Dan Pozmanter',
    description='Test Package & App for Jawaf',    
    include_package_data=True,
    license='BSD',
    name='Jawaf Example App',
    packages=['jawaf_example_app.app', 'jawaf_example_app.app.management.commands'],
    version='0.0.0',
    zip_safe=False,
    )