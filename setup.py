#!/usr/bin/env python

from setuptools import setup

setup(
    name='PyLamp',
    version='2.0',
    description='WebMail Notifier python script',
    author='Pierre Rambaud (GoT)',
    author_email='pierre.rambaud86@gmail.com',
    url='https://github.com/PierreRambaud/pylamp',
    license='GPLv3',
    scripts=['bin/pylamp'],
    packages=['pylamp'],
    requires=['pyusb (>= 1.0.0)'],
    install_requires=['pyusb>=1.0.0'],
    tests_require=[
        'coverage',
        'pep8',
        'flake8',
        'nose',
        'mock'
    ],
)
