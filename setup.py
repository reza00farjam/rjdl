import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as file:
    long_description = file.read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as file:
    requirements = file.read().splitlines()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="rjdl",
    version="1.0.1",
    packages=["rjdl"],
    install_requires=requirements,
    include_package_data=True,
    license="MIT License",
    description="Download Music, Video, Album, Podcast & Playlists from www.RadioJavan.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reza00farjam/rjdl",
    author="Reza Farjam",
    author_email="reza.farjam78@gmail.com",
    entry_points={
        "console_scripts": [
            "rjdl = rjdl.console:main",
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
