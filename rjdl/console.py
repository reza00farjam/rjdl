import sys
import argparse
import requests
from rjdl.objMusic import Music
from rjdl.objVideo import Video
from rjdl.objAlbum import Album
from rjdl.objPodcast import Podcast
from rjdl.objPlaylist import Playlist
from rjdl.downloader import downloader


def parse_args():
    parser = argparse.ArgumentParser(prog="rjdl",
                                     fromfile_prefix_chars='@',
                                     description="Download Music, Video, Album, Podcast & Playlists from www.RadioJavan.com"
                                     )
    parser.version = "1.0.0"
    group = parser.add_mutually_exclusive_group(required=False)

    parser.add_argument("url",
                        type=str,
                        help="URL of desired media"
                        )
    parser.add_argument("-p",
                        "--path",
                        type=str,
                        default='',
                        help="download path (default: current working directory)"
                        )
    parser.add_argument("-t",
                        "--tracks",
                        type=str,
                        nargs='+',
                        default="all",
                        help="track(s) of Album/Playlist to be downloaded, separated by white space (default: all tracks)"
                        )
    group.add_argument("-m",
                       "--music",
                       type=str,
                       default="320",
                       choices=["256", "320"],
                       help="download quality on Music, Album and Playlist URLs (default: 320)"
                       )
    group.add_argument("-v",
                       "--video",
                       type=str,
                       default="720p",
                       choices=["480p", "720p", "1080p"],
                       help="download quality on Video URLs (default: 720p)"
                       )
    parser.add_argument("-d",
                        "--download",
                        action="store_false",
                        help="disable downloading (show info only)"
                        )
    parser.add_argument("-r",
                        "--rjdl",
                        action="version",
                        help="show rjdl version and exit"
                        )

    return parser


def main():
    parser = parse_args()
    args = parser.parse_args()

    if not args.url.startswith("https://"):
        args.url = "https://" + args.url

    try:
        args.url = requests.get(args.url, allow_redirects=True).url
    except requests.exceptions.ConnectionError:
        parser.error("check your connection")
    except:
        parser.error("invalid url")

    def download(url: str, path: str = ''):
        try:
            downloader(url, path)
        except FileNotFoundError:
            parser.error("path doesn't exist")
        except BrokenPipeError:
            print("\n")
            parser.error("connection has been broken")
        except ConnectionError:
            parser.error("check your connection")
        except FileExistsError:
            parser.error("file already exists")

    try:
        if args.url.startswith("https://www.radiojavan.com/mp3s/mp3/"):
            music = Music(args.url, args.music)
            download_link = music.download_link

            print("Artist     ", music.artist)
            print("Name       ", music.name)
            print("Likes      ", music.likes)
            print("Plays      ", music.plays)
            print("Date Added ", music.date_added)
            print("Quality    ", music.quality + " kbps")
            print("Size       ", music.size + " mb")
            print("DL Link    ", download_link)
        elif args.url.startswith("https://www.radiojavan.com/videos/video/"):
            video = Video(args.url, args.video)
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
        elif args.url.startswith("https://www.radiojavan.com/podcasts/podcast/"):
            podcast = Podcast(args.url)
            download_link = podcast.download_link

            print("Artist     ", podcast.artist)
            print("Name       ", podcast.name)
            print("Likes      ", podcast.likes)
            print("Plays      ", podcast.plays)
            print("Date Added ", podcast.date_added)
            print("Quality    ", podcast.quality + " kbps")
            print("Size       ", podcast.size + " mb")
            print("DL Link    ", download_link)
        elif args.url.startswith("https://www.radiojavan.com/mp3s/album/"):
            album = Album(args.url, args.music)

            if "all" == args.tracks:
                tracks = list(range(album.length))
            else:
                tracks = []
                for num in args.tracks:
                    if not num.isdigit():
                        parser.error("invalid track number(s)")
                    elif 0 < int(num) <= album.length:
                        tracks.append(int(num) - 1)
                    else:
                        parser.error(f"{num} is out of range, there is only {album.length} tracks")

                tracks = sorted(set(tracks))

            print(f"{album.artist} | {album.name} | {album.date_added} | {album.quality} kbps")

            for index in tracks:
                track = album.track(index)

                print("\nTrack     {:02d}".format(index + 1))
                print("Artist   ", track.artist)
                print("Name     ", track.name)
                print("Likes    ", track.likes)
                print("Plays    ", track.plays)
                print("Size     ", track.size + " mb")
                print("DL Link  ", track.download_link)

                if args.download:
                    print("\nDownloading ...")
                    download(track.download_link, args.path)
            sys.exit()
        elif args.url.startswith("https://www.radiojavan.com/playlists/playlist/"):
            playlist = Playlist(args.url, args.music)

            if "all" == args.tracks:
                tracks = list(range(playlist.length))
            else:
                tracks = []
                for num in args.tracks:
                    if not num.isdigit():
                        parser.error("invalid track number(s)")
                    elif 0 < int(num) <= playlist.length:
                        tracks.append(int(num) - 1)
                    else:
                        parser.error(f"{num} is out of range, there is only {playlist.length} tracks")

                tracks = sorted(set(tracks))

            print(f"{playlist.creator} | {playlist.name} | {playlist.quality} kbps")

            for index in tracks:
                track = playlist.track(index)

                print("\nTrack     {:02d}".format(index+1))
                print("Artist   ", track.artist)
                print("Name     ", track.name)
                print("Likes    ", track.likes)
                print("Plays    ", track.plays)
                print("Size     ", track.size + " mb")
                print("DL Link  ", track.download_link)

                if args.download:
                    print("\nDownloading ...")
                    download(track.download_link, args.path)
            sys.exit()
        else:
            parser.error("invalid url")

        if args.download:
            print("\nDownloading ...")
            download(download_link, args.path)
    except ConnectionError:
        parser.error("check your connection")
    except ValueError:
        parser.error("this quality isn't available")
    except KeyboardInterrupt:
        print("\n")
        parser.error("keyboard interrupt")
