import sys as __sys
import time as __time
import os as __os
import requests as __requests
from platform import system as __system
from getpass import getuser as __getuser
from bs4 import BeautifulSoup as __bs

__version__ = '0.1.1'
__link = []
__console = False
__flag = True

def __downloader(url):
    hdr = __requests.head(url, allow_redirects=True)
    
    name = hdr.headers['Content-Disposition']
    name = name[name.find('"')+1: -1]
    
    if __system() == 'Windows':
        directory = "C:\\Users\\{}\\Music\\".format(__getuser()) if '.mp3' in name else "C:\\Users\\{}\\Videos\\".format(__getuser())
        if not __os.path.isdir(directory):
            directory = ''
    else:
        directory = ''
    
    if __os.path.isfile(directory + name):
        if __console:
            return print("--> File Already Exists!")
        raise FileExistsError("File Already Exists!")
    else:
        print("Name:  {}".format(name))
        print("Size:  {} Mb".format(round(int(hdr.headers['Content-Length']) / 1048675.44, 2)))
        print("Link:  {}".format(url))
        print("\nDownloading ...")
        
        with open(directory + name, "wb") as file:
            response = __requests.get(url, allow_redirects=True, stream=True)
            
            total_length = response.headers.get('content-length')
            if total_length is None:
                file.write(response.content)
            else:
                dl = 0
                start = __time.perf_counter()
                total_length = int(total_length.strip())
                try:
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        file.write(data)
                        done = int(50 * dl / total_length)
                        __sys.stdout.write("\r|{}{}| {:3}% | {:7.2f} kbps ".format('█' * done, '-' * (50 - done), 2 * done, round((dl / (__time.perf_counter() - start)) / 1000, 2)))    
                        __sys.stdout.flush()
                    print('')
                except:
                    file.close()
                    __os.remove(directory + name)
                    
                    if __console:
                        return print("\n\n--> Connection Has Broken!")
                    raise ConnectionError("Connection Has Broken!")

def album(url):
    if 'https://www.radiojavan.com/mp3s/album' not in url:
        raise FileNotFoundError("Wrong URL!")
    
    if '?' in url:
        url = url.split('?')[0]
    
    try:
        content = __requests.get(url).content
    except:
        if __console:
            return print("--> Check Your Connection!")
        raise ConnectionError("Check Your Connection!")
    
    soup = __bs(content, features="html.parser")
    data = soup.findAll('div', href=False, attrs={'class': 'songInfo'})
    
    if __flag:
        try:
            print("{} | {}\n-----".format(data[0].text.strip().split('\n')[0], data[0].text.strip().split('\n')[1]))
        except:
            if __console:
                return print("--> Wrong URL!")
            raise FileNotFoundError("Wrong URL!")
    
    flag = True if __flag else False
    
    for i in range(1, len(data)):
        artist, song = data[i].text.strip().split('\n')
        url = "https://www.radiojavan.com/mp3s/mp3/{}-{}".format(artist.replace('+', '').replace(':', '').replace('!', '').replace(',', '').replace('& ', '').replace('\'', '').replace(' ', '-'), song.replace('+', '').replace(':', '').replace('!', '').replace(',', '').replace('& ', '').replace('\'', '').replace(' ', '-'))
        globals()['__flag'] = False
        music(url)
        if flag:
            print("Song:\t{}".format(song))
            print("Link:\t{}\n-----".format(__link[-1]))

def link(url, quality='hq'):
    global __link
    __link.clear()
    globals()['__flag'] = False
    
    if 'https://www.radiojavan.com/mp3s/album' in url:
        album(url)
    elif 'https://www.radiojavan.com/mp3s/mp3' in url:
        music(url)
    elif 'https://www.radiojavan.com/playlists' in url:
        playlist(url)
    elif 'https://www.radiojavan.com/podcasts' in url:
        podcast(url)
    elif 'https://www.radiojavan.com/videos' in url:
        video(url, quality)
    else:
        globals()['__flag'] = True
        raise FileNotFoundError("Wrong URL!")
    
    return __link

def music(url):
    if 'https://www.radiojavan.com/mp3s/mp3' not in url:
        raise FileNotFoundError("Wrong URL!")
    
    if '?' in url:
        url = url.split('?')[0]
    
    name = url.split('/')[-1]
    
    try:
        resp = __requests.post("https://www.radiojavan.com/mp3s/mp3_host", params={'id': name})
    except:
        if __console:
            return print("--> Check Your Connection!")
        raise ConnectionError("Check Your Connection!")
    
    if __flag:
        __downloader("{}/media/mp3/mp3-256/{}.mp3".format(resp.json()["host"], name))
    else:
        __link.append("{}/media/mp3/mp3-256/{}.mp3".format(resp.json()["host"], name))
        globals()['__flag'] = True

def playlist(url):
    if 'https://www.radiojavan.com/playlists' not in url:
        raise FileNotFoundError("Wrong URL!")
    
    try:
        content = __requests.get(url).content
    except:
        if __console:
            return print("--> Check Your Connection!")
        raise ConnectionError("Check Your Connection!")
    
    soup = __bs(content, features="html.parser")
    data = soup.findAll('div', href=False, attrs={'class': 'songInfo'})
    
    if __flag:
        try:
            print("{} | {}\n-----".format(data[0].text.strip().split('\n')[0], data[0].text.strip().split('|')[1].strip().title()))
        except:
            if __console:
                return print("--> Wrong URL!")
            raise FileNotFoundError("Wrong URL!")
    
    flag = True if __flag else False
    
    for i in range(1, len(data)):
        artist, song = data[i].text.strip().split('\n')
        url = "https://www.radiojavan.com/mp3s/mp3/{}-{}".format(artist.replace('+', '').replace(':', '').replace('!', '').replace(',', '').replace('& ', '').replace('\'', '').replace(' ', '-'), song.replace('+', '').replace(':', '').replace('!', '').replace(',', '').replace('& ', '').replace('\'', '').replace(' ', '-'))
        globals()['__flag'] = False
        music(url)
        if flag:
            print("Artist:  {}\nSong:    {}".format(artist, song))
            print("Link:    {}\n-----".format(__link[-1]))

def podcast(url):
    if 'https://www.radiojavan.com/podcasts' not in url:
        raise FileNotFoundError("Wrong URL!")
    
    if '?' in url:
        url = url.split('?')[0]
    
    name = url.split('/')[-1]
    
    try:
        resp = __requests.post("https://www.radiojavan.com/podcasts/podcast_host", params={'id': name})
    except:
        if __console:
            return print("--> Check Your Connection!")
        raise ConnectionError("Check Your Connection!")
    
    if __flag:
        __downloader("{}/media/podcast/mp3-192/{}.mp3".format(resp.json()["host"], name))
    else:
        __link.append("{}/media/podcast/mp3-192/{}.mp3".format(resp.json()["host"], name))
        globals()['__flag'] = True

def video(url, quality='hq'):
    if 'https://www.radiojavan.com/videos' not in url:
        raise FileNotFoundError("Wrong URL!")
    
    if quality not in ['lq', 'hq', 'hd']:
        raise Exception("Wrong Quality!")
    
    name = url.split('/')[-1]
    
    try:
        resp = __requests.post("https://www.radiojavan.com/videos/video_host", params={'id': name})
        try:
            if __flag:
                __downloader("{}/media/music_video/{}/{}.mp4".format(resp.json()["host"], quality, name))
            else:
                __link.append("{}/media/music_video/{}/{}.mp4".format(resp.json()["host"], quality, name))
                globals()['__flag'] = True
        except:
            if __console:
                return print("--> {} Quality Isn't Available!".format(quality.upper()))
            raise Exception("{} Quality Isn't Available!".format(quality.upper()))
    except:
        if __console:
            return print("--> Check Your Connection!")
        raise ConnectionError("Check Your Connection!")

def __main():
    globals()['__console'] = True
    
    if len(__sys.argv) == 1:
        print("--> Arguments Can't Be Empty!")
    elif len(__sys.argv) > 3:
        print("--> Too Much Argument!")
    else:
        url = str(__sys.argv[1])
        
        if 'https://www.radiojavan.com/mp3s/album' in url:
            if len(__sys.argv) == 3:
                return print("--> Albums Take Only One Argument!")
            album(url)
        elif 'https://www.radiojavan.com/mp3s/mp3' in url:
            if len(__sys.argv) == 3:
                return print("--> Musics Take Only One Argument!")
            music(url)
        elif 'https://www.radiojavan.com/playlists' in url:
            if len(__sys.argv) == 3:
                return print("--> Playlists Take Only One Argument!")
            playlist(url)
        elif 'https://www.radiojavan.com/podcasts' in url:
            if len(__sys.argv) == 3:
                return print("--> Podcasts Take Only One Argument!")
            podcast(url)
        elif 'https://www.radiojavan.com/videos' in url:
            if len(__sys.argv) == 3:
                if __sys.argv[2].lower().strip() in ['lq', 'hq', 'hd']:
                    video(url, __sys.argv[2].lower().strip())
                else:
                    print("--> Wrong Quality!")
            else:
                video(url)
        else:
            print("--> Wrong URL!")
