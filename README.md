[about rjdl](#about-rjdl)  
[installation](#installation)  
[usage - in console](#in-console)  
[usage - in script](#in-script)  

---
# about rjdl

* with this package you will be able to save **musics**, **videos (music videos & rj-tv shows)**, **podcasts**, **playlists** and **albums** from *radiojavan website* to your personal computer.   
* *podcasts* will be saved in **192 kbps** quality, *musics* in **256 kbps** quality, and for *videos* you can choose between **lq (480p)**, **hq (720p)** and **hd (1080p)** quality if they are available.  
* for *windows* systems *mp3s* will be saved in **"C:\Users\\\<your-username>\Music"**, and *videos* will be saved in **"C:\Users\\\<your-username>\Videos"**. and for *non windows* systems saving path will be **current working directory**.
* if you live in *iran*, you need to turn on your **vpn** while using this package.
* this package can be used in 2 ways. a *python madule*, or a *command* in your os console.   

---

# installation

use `pip install rjdl` in command line for installing package. (of course for being able to use *pip* command, you need to have python installed and added to your *computer's path* first)

---

# usage

### in console

* for downloading *musics*, *podcasts*, *playlists* & *albums*, use following pattern:   
`rjdl "<url>"`  

* and for downloading *music videos* & *rj-tv shows*, use same pattern with an extra optional argument for quality *(it is set to hd by default)*:  
`rjdl "<url>" "<quality>"`  

example in windows's console *(cmd)*:  

<img src="http://www.mediafire.com/convkey/e8ce/hzvygnnurpbn9oezg.jpg" width="600">

### in script

* first of all, you have to `import rjdl` in your script to be able to use it.

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
 |████████████████████████████████████████████------|  88% |  506.05 kbps 
```

* the **video** attribute can be used to download *music videos* or *rj-tv shows*. it takes *two arguments*, first one is *url* of your video and the second argument is *quality* of the video that is set to *hq*  by default but you can change it to *lq* or *hd*. it returns video info, direct download link if you want to download it with download manager apps, and finally starts to download the video.  
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
 |█████████████████████████-------------------------|  50% |  496.75 kbps 
```

* the **podcast** attribute is similar to *music* attribute.  
sample code:

```python
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

* the **playlist** attribute scrapes *playlist's name* along with its included *songs info*, and return them with *direct download link* of each song. it takes only *one argument* that is url of desired playlist. this attribute, unlike previous attributes, *dosen't download files*.  
sample code:

```python
>>> import rjdl
>>> rjdl.playlist('https://www.radiojavan.com/playlists/playlist/mp3/854b87855624')
```

```
 Today's Top Hits | 30 Songs
 -----
 Artist:  Garsha Rezaei
 Song:    Darya Darya
 Link:    https://host2.rj-mw1.com/media/mp3/mp3-256/Garsha-Rezaei-Darya-Darya.mp3
 -----
 Artist:  Hamid Hiraad & Ragheb
 Song:    Jazzab
 Link:    https://host2.rj-mw1.com/media/mp3/mp3-256/Hamid-Hiraad-Ragheb-Jazzab.mp3
 -----
 Artist:  Donya
 Song:    Siah Sefid
 Link:    https://host2.rj-mw1.com/media/mp3/mp3-256/Donya-Siah-Sefid.mp3
 -----
 Artist:  Donya
 Song:    Mese Man
 Link:    https://host2.rj-mw1.com/media/mp3/mp3-256/Donya-Mese-Man.mp3
 -----
 Artist:  Poobon
 Song:    Blue Dream
 Link:    https://host2.rj-mw1.com/media/mp3/mp3-256/Poobon-Blue-Dream.mp3
 -----
 ...
 ...
 ...
```

* the **album** attribute is similar to *playlist* attribute.  
sample code:

```python
>>> import rjdl
>>> rjdl.album('https://www.radiojavan.com/mp3s/album/Shayea-Injaneb')
```

```
Shayea | Injaneb
-----
Song:	Intro (Injaneb)
Link:	https://host2.rj-mw1.com/media/mp3/mp3-256/Shayea-Intro-(Injaneb).mp3
-----
Song:	Injaneb
Link:	https://host2.rj-mw1.com/media/mp3/mp3-256/Shayea-Injaneb.mp3
-----
Song:	Ahle Naa Ahli
Link:	https://host2.rj-mw1.com/media/mp3/mp3-256/Shayea-Ahle-Naa-Ahli.mp3
-----
Song:	Ehtiaj Daram
Link:	https://host2.rj-mw1.com/media/mp3/mp3-256/Shayea-Ehtiaj-Daram.mp3
-----
Song:	Manam Oon Ke Maghroor
Link:	https://host2.rj-mw1.com/media/mp3/mp3-256/Shayea-Manam-Oon-Ke-Maghroor.mp3
-----
...
...
...
```

* the **link** attribute is like an *all in one* for other attributes! this attribute gets one argument that is a url of desired *music*, *video*, *podcast*, *playlist* or *album* *(video urls can have a seceond argument for quality)*. it returns a list of direct download links of desired files in that url.  
sample code:

```python
>>> import rjdl
>>> rjdl.link('https://www.radiojavan.com/mp3s/album/Mohsen-Chavoshi-Amire-Bi-Gazand')
```

```
['https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Amire-Bi-Gazand.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Dele-Man.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Changiz.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-In-Kist-In.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Jangzadeh.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Sheydaei.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Shah-Maghsood.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Parishan.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Sharmsari.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Akharin-Otobus.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Teryagh.mp3', 'https://host1.rj-mw1.com/media/mp3/mp3-256/Mohsen-Chavoshi-Motasel.mp3']
```
