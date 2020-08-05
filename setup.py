import rjdl
from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='rjdl',
    version=rjdl.__version__,
    packages=['rjdl',],
    install_requires=requirements,   
    include_package_data=True,
    license='MIT License',
    description='download musics, videos, podcasts, playlists & albums from www.RadioJavan.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/reza00farjam/radio-javan-downloader',
    author='Reza Farjam',
    author_email='reza.farjam78@gmail.com',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
