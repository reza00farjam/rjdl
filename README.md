## about rjdl
* with this package you will be able to save **musics**, **videos (music videos & rj-tv shows)**, **podcasts** and **playlists** from *radiojavan website* to your personal computer.   
* *podcasts* will be saved in **192 kbps** quality, *musics* in **256 kbps** quality, and for *videos* you can choose beetwin **lq (480p)**, **hq (720p)** and **hd (1080p)** quality if they are available.  
* this package can be used in 2 ways. a *python madule*, or a *command* in your os console.   

## requirements
this package is powered by two external python library, **requests** and **BeautifulSoup**. make sure you have installed them before using this package. if you don't have installed them yet, you can use following commands in your os terminal:   

`pip install requests`
`pip install bs4`

## usage
### as a madule
* first of all, you have to `import rjdl` in your script to be able to use it.
------
* you can use **music** attribute for downloading musics. it takes *exactly one argument* that is a *url* to your desired song. it returns song info, direct download link if you want to download it with download manager apps, and finally starts to download the song.  
sample code:

```python
>>> import rjdl
>>> rjdl.music('https://www.radiojavan.com/mp3s/mp3/Koorosh-Azin-Manzare-(Ft-Cornellaa)')
```

```
 Name:  Koorosh-Azin-Manzare-(Ft-Cornellaa).mp3
 Size:  4.85 Mb
 Link:  https://host2.rj-mw1.com/media/mp3/mp3-256/Koorosh-Azin-Manzare-(Ft-Cornellaa).mp3
 
 Downloading ...
 |█████████████████---------------------------------|  34% |  148.40 kbps  
```

------

* the **video** attribute can be used to download *music videos* or *rj-tv shows*. it takes *two arguments*. first one is *url* of your video, and the second argument is *quality* of the video that is set to *hq*  by default but you can change it to *lq* or *hd*. it returns video info, direct download link if you want to download it with download manager apps, and at the end starts to download the video.  
sample code:  

```python
>>> import rjdl
>>> rjdl.video('https://www.radiojavan.com/videos/video/gringo-show-season-2-episode-33', 'lq')
```

```
 Name:  gringo-show-season-2-episode-33.mp4
 Size:  189.36 Mb
 Link:  https://host2.rj-mw1.com/media/music_video/lq/gringo-show-season-2-episode-33.mp4
 
 Downloading ...
 |████████------------------------------------------|  16% |  496.75 kbps 
```

------

* the **podcast** attribute is similar to music attribute, but it is for podcasts!  
sample code:

```
>>> import rjdl
>>> rjdl.podcast('https://www.radiojavan.com/podcasts/podcast/RJ-Interview-Donya-Shatranji-Album')
```

```
 Name:  RJ-Interview-Donya-Shatranji-Album.mp3
 Size:  41.22 Mb
 Link:  https://host2.rj-mw1.com/media/podcast/mp3-192/RJ-Interview-Donya-Shatranji-Album.mp3
 
 Downloading ...
 |████████████████----------------------------------|  32% |  232.25 kbps
```
