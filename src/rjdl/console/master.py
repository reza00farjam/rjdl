import sys

import click
from rjdl import __version__
from rjdl.console.errors import CLIConnectionError
from rjdl.console.types import URLType
from rjdl.downloader import downloader
from rjdl.models import Album, Music, Playlist, Podcast, Video


def download(url: str, path: str):
    try:
        downloader(url, path)
    except (BrokenPipeError, ConnectionError):
        raise CLIConnectionError()
    except FileExistsError:
        click.ClickException("file already exists").show()


@click.command(no_args_is_help=True)
@click.version_option(__version__)
@click.argument("url",
                type=URLType(),
                required=True)
@click.option("-p",
              "--path",
              type=click.Path(file_okay=False),
              default="",
              help="Download path",
              show_default="current working directory")
@click.option("-m",
              "--music-quality",
              type=click.Choice(["256", "320"]),
              default="320",
              help="Download quality on Music, Album and Playlist URLs",
              show_default=True
              )
@click.option("-v",
              "--video-quality",
              type=click.Choice(["480", "720", "1080"]),
              default="720",
              help="Download quality on Video URLs",
              show_default=True)
@click.option("-d",
              "--disable-download",
              is_flag=True,
              help="Disable auto downloading (show info only)")
def cli(url: str, path: str, music_quality, video_quality, disable_download):
    """Download Music, Video, Album, Podcast & Playlists
    from Radio Javan

    URL: Link of desired media
    """

    try:
        if url.startswith("https://www.radiojavan.com/mp3s/mp3/"):
            music = Music(url, music_quality)
            download_link = music.download_link

            print("Artist     ", music.artist)
            print("Name       ", music.name)
            print("Likes      ", music.likes)
            print("Plays      ", music.plays)
            print("Date Added ", music.date_added)
            print("Quality    ", music.quality + " kbps")
            print("Size       ", music.size + " mb")
            print("DL Link    ", download_link)
        elif url.startswith("https://www.radiojavan.com/videos/video/"):
            video = Video(url, video_quality)
            download_link = video.download_link

            print("Artist     ", video.artist)
            print("Name       ", video.name)
            print("Likes      ", video.likes)
            print("Plays      ", video.plays)
            print("Date Added ", video.date_added)
            if video.director:
                print("Director   ", video.director)
            print("Quality    ", video.quality)
            print("Size       ", video.size + " mb")
            print("DL Link    ", download_link)
        elif url.startswith("https://www.radiojavan.com/podcasts/podcast/"):
            podcast = Podcast(url)
            download_link = podcast.download_link

            print("Artist     ", podcast.artist)
            print("Name       ", podcast.name)
            print("Likes      ", podcast.likes)
            print("Plays      ", podcast.plays)
            print("Date Added ", podcast.date_added)
            print("Quality    ", podcast.quality + " kbps")
            print("Size       ", podcast.size + " mb")
            print("DL Link    ", download_link)
        elif url.startswith("https://www.radiojavan.com/mp3s/album/"):
            album = Album(url, music_quality)
            tracks = list(range(album.length))

            print(
                f"{album.artist} | {album.name} | {album.date_added} | {album.quality} "
                "kbps"
            )

            for index in tracks:
                track = album.track(index)

                print("\nTrack     {:02d}".format(index + 1))
                print("Artist   ", track.artist)
                print("Name     ", track.name)
                print("Likes    ", track.likes)
                print("Plays    ", track.plays)
                print("Size     ", track.size + " mb")
                print("DL Link  ", track.download_link)

                if disable_download:
                    print("\nDownloading ...")
                    download(track.download_link, path)
            sys.exit()
        elif url.startswith("https://www.radiojavan.com/playlists/playlist/"):
            playlist = Playlist(url, music_quality)
            tracks = list(range(playlist.length))

            print(f"{playlist.creator} | {playlist.name} | {playlist.quality} kbps")

            for index in tracks:
                track = playlist.track(index)

                print("\nTrack     {:02d}".format(index + 1))
                print("Artist   ", track.artist)
                print("Name     ", track.name)
                print("Likes    ", track.likes)
                print("Plays    ", track.plays)
                print("Size     ", track.size + " mb")
                print("DL Link  ", track.download_link)

                if disable_download:
                    print("\nDownloading ...")
                    download(track.download_link, path)
            sys.exit()
        else:
            raise click.ClickException("invalid url")

        if disable_download:
            print("\nDownloading ...")
            download(download_link, path)

    except Exception as e:
        raise click.ClickException(e)
