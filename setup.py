import os
import sys
import rjdl
from setuptools import setup

read_me = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as file:
    requirements = file.read().splitlines()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rjdl',
    version=rjdl.__version__,
    packages=['rjdl',],
    install_requires=requirements,   
    include_package_data=True,
    license='MIT License',
    description='download musics, videos, podcasts, playlists & albums from www.RadioJavan.com',
    long_description=read_me,
    url='https://github.com/reza00farjam/radio-javan-downloader',
    author='Reza Farjam',
    author_email='reza.farjam78@gmail.com'
)
