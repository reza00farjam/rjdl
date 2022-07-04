import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), "README.md")) as file:
    long_description = file.read()


# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="rjdl",
    version="1.1.0",
    include_package_data=True,
    license="MIT License",
    description="Download Music, Video, Album, Podcast & Playlists from \
        www.RadioJavan.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/reza00farjam/rjdl",
    author="Reza Farjam",
    author_email="reza.farjam78@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "rjdl = rjdl.console:cli",
        ]
    },
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=["click>=8.1.3", "requests>=2.22.0", "beautifulsoup4>=4.9.1"],
    extras_require={
        "dev": ["pylint", "tox", "mypy", "flake8", "black"],
        "test": ["pytest"]
    },
)
