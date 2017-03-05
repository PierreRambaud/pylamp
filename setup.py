#!/usr/bin/env python

from setuptools import setup

setup(
    name='PyLamp',
    version='1.0',
    description='WebMail Notifier python script',
    author='Pierre Rambaud (GoT)',
    author_email='pierre.rambaud86@gmail.com',
    url='https://github.com/PierreRambaud/pylamp',
    license='GPLv3',
    scripts=['scripts/pylamp'],
    packages=['pylamp'],
    requires=['pyusb (>= 1.0.0b1)'],
    install_requires=['pyusb>=1.0.0b1'],
    tests_require=[
        'coverage',
        'pep8',
        'flake8',
        'nose',
        'mock'
    ],
)