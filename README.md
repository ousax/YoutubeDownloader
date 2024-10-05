# YoutubeDownloader
Simple script to download single videos , playlists from youtube 
using [https://www.y2mate.com] [https://cable.ayra.ch]

# Requirements
requests
bs4 
colorama

# Installation 
git clone https://github.com/ousax/YoutubeDownloader.git ;
cd YoutubeDownloader ; pip install -r Requirements ; chmod +x YtbDownloader.py

# Usage
python YtbDownloader.py -l v -mtype -qlt  0 -r y -c "/copy/to/folder"

python YtbDownloader.py -pl a -mtype -qlt  0 -r y -c "/copy/to/folder"

-l the link of the video [type=str]

-pl the playlist [type=str]

-mtype media type (video, audio), "a" for video (mp4), "v" for (audio) mp3 [type=str]

-qlt Quality of the media [type=int]
0, 1, 3, ... so the highest quality is the small int, it takes 0 as default value [type=int]
for example 
{0:1080, 1:720, 2:480, 3, 360}.
sometimes 0 doesn't work so you may wanna change replace it with 1

-r Random user agent [type=str]

-c move the video/audio to ("/cop/to/folder") if it's a valid path