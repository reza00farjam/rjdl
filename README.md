[![PyPI](https://img.shields.io/badge/pypi-v1.0.1-blue)](https://pypi.org/project/rjdl/) [![Python 3](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue)](https://pypi.org/project/rjdl/) [![Downloads](https://pepy.tech/badge/rjdl)](https://pepy.tech/project/rjdl) [![LICENSE](https://img.shields.io/badge/license-MIT-green)](https://github.com/reza00farjam/rjdl/blob/master/LICENSE) [![Codacy Badge](https://app.codacy.com/project/badge/Grade/ea5df880a3fa4136824c887af12f4f38)](https://www.codacy.com/gh/reza00farjam/rjdl/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=reza00farjam/rjdl&amp;utm_campaign=Badge_Grade) [![Documentation Status](https://readthedocs.org/projects/rjdl/badge/?version=latest)](https://rjdl.readthedocs.io/en/latest/?badge=latest)

* This package can be used in two different ways:  
    * If you want to use it as a downloader only, then you can simply use its CLI.  
    * But if you are a more advanced user and want to use this package in your projects, then you can import it in your project and you're good to go.
* With this package you will be able to save any **Music**, **Video (Music Video & RJ-TV Show)**, **Album**, **Podcast** and **Playlist** from [RadioJavan](https://www.radiojavan.com/) to your personal computer.  
* *Podcasts* will be saved in **192 kbps** quality only, while you can choose between **256 kbps** and **320 kbps** for *Songs (Albums & Playlists as well)*, and **480p**, **720p** and **1080p** for *Videos* if available.  
* If you are currently living in *Iran*, you need to turn on your **VPN** while using this package.

## Installation

* Use `pip install rjdl` to install the latest release of the package. (Of course to be able to use *pip*, you need python to be installed and added to computer's path first)  
* If you want to install the latest version directly from GitHub, then you can use this:  
`pip install git+git://github.com/reza00farjam/rjdl`  

## Usage

### Command Line

The ```rjdl``` as a command, is a well behaved Unix style command line tool that provides you the following optional arguments to use based on the content of your url. You can also list them by running `rjdl -h` or `rjdl --help`:

```text
usage: rjdl [-h] [-p PATH] [-t TRACKS [TRACKS ...]]
            [-m {256,320} | -v {480p,720p,1080p}] [-d] [-r]
            url

Download Music, Video, Album, Podcast & Playlists from www.RadioJavan.com

positional arguments:
  url                   URL of desired media

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  download path (default: current working directory)
  -t TRACKS [TRACKS ...], --tracks TRACKS [TRACKS ...]
                        track(s) of Album/Playlist to be downloaded, separated
                        by white space (default: all tracks)
  -m {256,320}, --music-quality {256,320}
                        download quality on Music, Album and Playlist URLs
                        (default: 320)
  -v {480p,720p,1080p}, --video-quality {480p,720p,1080p}
                        download quality on Video URLs (default: 720p)
  -d, --disable-download
                        disable auto downloading (show info only)
  -r, --rjdl-version    show rjdl version and exit
```

#### How it works

Simply, just pass rjdl a valid url along with your desired options for it and enjoy your download!
[Example](https://github.com/reza00farjam/rjdl/blob/61ffe179a944d196042071e7d2cefb26046c79e9/example.gif?raw=true).

### Script

The rjdl as a package, provides enough class and methods to work with RadioJavan for your
development purposes. For a good understanding of what it does and how it works, you can take a look at
[rjdl documentation](https://rjdl.readthedocs.io/en/latest/).

## Contributing

* Contributions of all sizes are welcomed and precious. You can follow the steps below for this purpose:
    * [Fork](https://github.com/reza00farjam/rjdl/fork) the repository.  
    * Make all the changes you want to see in the original repository.  
    * Push your changes to a new branch in your fork and [create a pull request](https://github.com/reza00farjam/rjdl/compare) along with an explanation of your changes.  
* Also you can help us by [reporting bugs and sharing your ideas](https://github.com/reza00farjam/rjdl/issues/new).  

## Copyright & License

* Copyright (C) 2020-2021 Reza Farjam <<https://github.com/reza00farjam>>  
* Licensed under the terms of the [MIT License](https://github.com/reza00farjam/rjdl/blob/master/LICENSE).  
