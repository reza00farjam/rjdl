import sys

import click
from click import echo
from . import __version__
from .downloader import DownloadManager, DownloadCallback
from .models import Album, Music, Playlist, Podcast, Video


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]), no_args_is_help=True
)  # If no arguments are given, show the help message.
@click.version_option(__version__)
@click.argument(
    "urls", type=click.STRING, nargs=-1, required=True  # Allow multiple URLs.
)
@click.option(
    "-p",
    "--path",
    type=click.Path(file_okay=False),
    default="",
    help="Download path",
    show_default="current working directory",
)
@click.option(
    "-m",
    "--music-quality",
    type=click.Choice(["256", "320"]),
    default="320",
    help="Download quality on Music, Album and Playlist URLs",
    show_default=True,
)
@click.option(
    "-v",
    "--video-quality",
    type=click.Choice(["480", "720", "1080"]),
    default="720",
    help="Download quality on Video URLs",
    show_default=True,
)
@click.option("-i", "--info", is_flag=True, help="Only show info about the URL")
def cli(urls: list[str], path: str, music_quality, video_quality, info: bool):
    """Download Music, Video, Album, Podcast & Playlists
    from Radio Javan

    URLs: Links of desired media.
    """

    dm = DownloadManager(urls, path, music_quality, video_quality, info)

    dm.add_callback(_Callback())
    dm.start()


class _Callback(DownloadCallback):
    def on_fetching(self, url: str):
        echo(f"Fetching: {url}")

    def on_fetched(self, data):
        if isinstance(data, Album):
            echo(f"{data.artist} | {data.name} | {data.date_added}")
        elif isinstance(data, Music):
            echo("Artist     " + data.artist)
            echo("Name       " + data.name)
            echo("Likes      " + data.likes)
            echo("Plays      " + data.plays)
            echo("Date Added " + data.date_added)
        elif isinstance(data, Playlist):
            echo(f"{data.creator} | {data.name}")
        elif isinstance(data, Podcast):
            echo("Artist     " + data.artist)
            echo("Name       " + data.name)
            echo("Likes      " + data.likes)
            echo("Plays      " + data.plays)
            echo("Date Added " + data.date_added)
        elif isinstance(data, Video):
            echo("Artist     " + data.artist)
            echo("Name       " + data.name)
            echo("Likes      " + data.likes)
            echo("Plays      " + data.plays)
            echo("Date Added " + data.date_added)
            if data.director:
                echo("Director   " + data.director)

    def on_downloading(self, dl_url: str, dl_size: int):
        echo(f"Downloading: {dl_url} ({dl_size / (1024 * 1024):.2f} MB)")

    def on_progress(self, progress: float, speed: float):
        sys.stdout.write(
            "\r|{}{}| {:3.2f}% | {:7.2f} kbps ".format(
                "\U00002588" * int(progress / 2),
                "-" * int((100 - progress) / 2),
                progress,
                speed / 1024,
            )
        )
        sys.stdout.flush()

    def on_downloaded(self, path: str):
        echo(f"\nDownloaded: {path}")
