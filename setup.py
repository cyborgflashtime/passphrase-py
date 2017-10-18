#!/usr/bin/env python3
from setuptools import setup


def readme():
    with open('README.rst') as rst:
        return rst.read()


setup(name='passphrase',
      version='0.4.1',
      description='Generates cryptographically secure passphrases and '
                  'passwords',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.2',
        'Topic :: Security :: Cryptography',
        'Topic :: Utilities'
      ],
      platforms=[
        'POSIX :: Linux'
      ],
      keywords='cryptography passphrase password security',
      url='http://github.com/hackancuba/passphrase-py',
      author='HacKan',
      author_email='hackan@gmail.com',
      license='GNU GPL 3.0+',
      packages=['passphrase'],
      python_requires='~=3.2',
      package_data={
        '': ['wordlist.json'],
      },
      install_requires=[
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={
          'console_scripts': ['passphrase=passphrase.__main__:main'],
      },
      zip_safe=False)