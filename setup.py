#!/usr/bin/env python

from setuptools import setup

setup(
      name='isi',
      version='0.1-pre1',
      description='',
      author='',
      author_email='',
      packages=['isi'],
#      package_dir={'': ''},
      install_requires=['gevent', 'flask', 'Flask-JSONPages','Gunicorn','setproctitle'],
      entry_points={
          'console_scripts' : [
              'runserver=isi:main',
              ],
      }
)
