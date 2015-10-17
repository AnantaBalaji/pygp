from setuptools import setup

import os


def Readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.md'), "r").read()

setup(
    name='pygp',
    packages=['pygp'],
    version='0.0.1',
    description='Not Available',
    long_description = Readme(),
    author='AnantaBalaji',
    author_email='anantanarayanantce@gmail.com',
    url='https://github.com/AnantaBalaji/pygp.git',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers'
    ],
    entry_points={
          'console_scripts': ['pygp=pygp:main'],
    },
    install_requires=['six', 'dpkt'],
    include_package_data=True,
    license='MIT License',
)