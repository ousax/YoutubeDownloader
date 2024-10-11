import requests
import os
import sys
import argparse
import random
import json
import math
import string
import re
import time
from tqdm import tqdm
from string import punctuation
from colorama import Fore, init
from bs4 import BeautifulSoup as bs
init(autoreset=True)
parser = argparse.ArgumentParser()
parser.add_argument("-l", metavar="The link", help="The link of the video.", type=str)
parser.add_argument("-r", metavar="Random UserAgent", help="Using a random UserAgent", type=str, choices=["y","n"], default="y")
parser.add_argument("-pl", metavar="Playlist", help="Youtube Playlist", type=str)
parser.add_argument("-mtype", metavar="Media type", help = "Type [(v)ideo, (a)udio]", choices=['v', 'a'], type=str, default="a")
parser.add_argument("-qlt", metavar="Video/Audio Quality", help="Media quality available choices [0, 1, 2, 3 ]", type=int, default=0)
parser.add_argument("-c", metavar="Move", help="Move the media to another location", type=str, default="n")
args = parser.parse_args()
link = args.l
pl = args.pl
mp3_mp4 = args.mtype
user_format = int(args.qlt) # the quality of the media 1080, 720, 480 ...
c_p = args.c
while not link and not pl:
    link = input(Fore.GREEN+"Enter the youtube link: ")
if link:
    if "youtu.be" in link: # mobile version 
        link = f"https://www.youtube.com/watch?v={link.split('/')[-1]}"
while c_p not in ["n", "stop"] and os.path.exists(c_p) != True:
     print(Fore.RED+f"{c_p} doesn't exitst")
     c_p = input(Fore.GREEN+"Enter the destination path: ")
class SocialMediaDownloader:
    """
    Youtube downloader
    twitter: @0lifeizalie
    """
    if pl:
        plname = f"PlayList_{''.join(random.sample(string.ascii_letters+string.digits, 8))}"
        try:
            os.mkdir(plname)
        except FileExistsError:
            pass
        except Exception as ErrorCreatingPlaylist:
            print(Fore.RED,f"ErrorCreatingPlaylist: {ErrorCreatingPlaylist}")
            pass
        try:
            os.chdir(plname)
        except:
            pass
    global Youtube, YTBConverter, YTBConverter, Facebook, Tiktok, Instagram, Twitter, useragent, AjaxReq
    Youtube = "https://www.y2mate.com/en858/download-youtube"
    YTBConverter = "https://www.y2mate.com/en858/conver-youtube" 
    YTB2MP3 = "https://www.y2mate.com/en858/youtube-mp3"
    Instagram =  "https://www.y2mate.com/en/instagram-downloader"
    Facebook = "https://www.y2mate.com/en/facebook-downloader"
    Tiktok = "https://www.y2mate.com/en/tiktok-downloader"
    Twitter = "https://www.y2mate.com/en/twitter-downloader"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    if args.r != "n":
        # random user agent
        ua = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20130401 Firefox/61.3",
                "Mozilla/5.0 (Windows NT 10.3; WOW64; en-US) AppleWebKit/602.40 (KHTML, like Gecko) Chrome/51.0.2327.172 Safari/600.9 Edge/13.51427",
                "Mozilla/5.0 (Linux; Linux x86_64) Gecko/20130401 Firefox/67.2",
                "Mozilla/5.0 (Linux; U; Linux i676 x86_64; en-US) AppleWebKit/603.4 (KHTML, like Gecko) Chrome/55.0.2370.117 Safari/600",
                "Mozilla/5.0 (compatible; MSIE 8.0; Windows; U; Windows NT 6.2; Win64; x64; en-US Trident/4.0)",
                "Mozilla/5.0 (Linux; U; Android 6.0; Nexus 6 Build/MMB29V) AppleWebKit/603.8 (KHTML, like Gecko)  Chrome/55.0.1155.212 Mobile Safari/601.1",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 8_2_2; en-US) Gecko/20100101 Firefox/48.9",
                "Mozilla/5.0 (Linux; Android 5.1; SAMSUNG SM-G9350M Build/LMY47X) AppleWebKit/536.47 (KHTML, like Gecko)  Chrome/54.0.1636.173 Mobile Safari/536.6"
            ]
        useragent = random.choice(ua)
    def Extractor():
        Link = []
        def Twitter():
            try:
                twitterJson = json.loads(AjaxReq.text)
                title = twitterJson["title"]
                title  = title.replace('|', '').replace('\\', '').replace('/', '').replace('*', '').replace(':', '').replace('>', '').replace('<', '').replace('|', '_').replace(")", "_").replace("(", "_").replace(' ', '_')
                title = title+".mp4"
                qlty = [_ for _ in twitterJson['links']['video']][-1]
                try:
                    finalUrl = qlty['url']
                    file_size = int(requests.head(finalUrl).headers['Content-Length'])
                    with requests.get(finalUrl, stream=True) as response:
                        response.raise_for_status()
                        with open(title, 'wb') as file:
                            with tqdm(total=file_size, unit='B', unit_scale=True, desc=f'{Fore.GREEN}Downloading ... ') as bar:
                                for chunk in response.iter_content(chunk_size=8192):
                                    file.write(chunk)
                                    bar.update(len(chunk))
                            if sys.platform == "linux" and c_p not in ["n", 'stop']:
                                os.system(f"mv {title} {c_p if c_p not in ['n', 'stop'] and os.path.exists(c_p) else '/sdcard' if os.path.exists('/sdcard') else '../'}")
                                print("Done !")
                except Exception as E:
                    print(Fore.RED, f"DownloadException: {E}")
                    exit()
            except Exception as TwitterE:
                print(Fore.RED+f"TwitterE: {TwitterE}")
            exit()
        def PlayList_():
            links_ = []
            playlist = f"https://cable.ayra.ch/ytdl/playlist.php?url={pl}&API=1"
            PlayHeaders = {
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                #"Accept-Encoding":"gzip, deflate, br, zstd",
                "Accept-Language":"fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
                "Host":"cable.ayra.ch",
                "Referer":"https://cable.ayra.ch/ytdl/playlist.php",
                "User-Agent":useragent
            }
            getPlaylist = requests.get(playlist, headers=PlayHeaders, timeout=5)
            if getPlaylist.status_code == 200:
                link = getPlaylist.text
                links_ = [_.replace("\ufeff", "").strip() for _ in link.split('\n')]
            if not getPlaylist.ok:
                print(Fore.red+getPlaylist.status_code)
            print(Fore.CYAN, f"Extracted {len(links_)} link(s)")
            return links_
        if pl:
            Link = PlayList_()
            if not len(Link) != 0:
                print(Fore.RED, f"The playlist is empty", Fore.RED)
                exit(f"Exiting ")
        else:
            Link.append(args.l)

        for item_number, item in enumerate(Link):# start the for loop from here
            if item_number > 0 and args.l:
                break
            link = item
            ajax = "https://www.y2mate.com/mates/en948/analyzeV2/ajax" 
            ajaxHeaders = {
                "Accept":"*/*",
                "Accept-Language":"en,us;q=0.9",
                "UserAgent":useragent,
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Origin":"https://www.y2mate.com",
                "Referer":"https://www.y2mate.com/en948" #if not twitter_re else "https://www.y2mate.com/en/twitter-downloader" 
            }
            #print("Link: ", link)
            payload = {
                "k_query":link,
                "k_page":"home",# if not twitter_re else "Twitter",
                "hl":"en",
                "q_auto":0
            }
            AjaxReq = requests.post(ajax, data=payload, headers=ajaxHeaders, timeout=4) # get informations about the video
            # twitter links "https://x.com/i/status/1808526518320255017"
            twitter_re = re.match(r"https://(x|twitter)\.com/[i|a-zA-Z0-9_.]+/status/[0-9]{19}", Link[0])
            if twitter_re:
                Twitter()
            headers = {
                "UserAgent":useragent
            }
            LoadYoutube = json.loads(AjaxReq.text)
            vid = LoadYoutube['vid']
            title = LoadYoutube["title"]
            mp3_mp4 = args.mtype
            user_format = int(args.qlt)
            racine_mp4 = LoadYoutube["links"]['mp4']
            racine_mp3 = LoadYoutube["links"]['mp3']
            available_formats = [[racine_mp4[_]['q'], racine_mp4[_]['k']] for _ in LoadYoutube["links"]['mp4']] if mp3_mp4 == "v" else [[racine_mp3[_]['q'], racine_mp3[_]['k']] for _ in racine_mp3]
            def Display(): 
                for i, x in enumerate(available_formats):
                    print("ID: ", Fore.GREEN, i, Fore.BLUE, x[0])
            #if not pl:
             #   display()
              #  user_format = int(input("Enter the ID for the video: "))
            while math.fabs(user_format) > len(available_formats):
                Display()
                user_format = int(input("Enter the ID for the video: "))
            #print(AjaxReq.text) # twitter videos
            #print(AjaxReq.text[''])
            #exit()
            converterUrl = "https://www.y2mate.com/mates/convertV2/index"
            payload_converter = {
                "vid":vid,
                "k":available_formats[user_format][1]
            }
            convertHeaders = {
                "UserAgent":useragent,
                "Referer":f"https://www.y2mate.com/youtube/{vid}",
                "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
                "Origin":"https://www.y2mate.com"
            }
            ConverterReq = requests.post(converterUrl, headers=convertHeaders, data=payload_converter)
            if ConverterReq.status_code == 200:
                LoadFinalUrl = json.loads(ConverterReq.text)
                finalUrl = LoadFinalUrl['dlink']
                title = title+".mp4" if LoadFinalUrl['ftype'] == "mp4" else title+".mp3"
                title  = title.replace('|', '').replace('\\', '').replace('/', '').replace('*', '').replace(':', '').replace('>', '').replace('<', '').replace('|', '_').replace(")", "_").replace("(", "_").replace(' ', '_')
                file_size = int(requests.head(finalUrl).headers['Content-Length'])
                with requests.get(finalUrl, stream=True) as response:
                    response.raise_for_status()
                    with open(title, 'wb') as file:
                        with tqdm(total=file_size, unit='B', unit_scale=True, desc=f'{Fore.GREEN}Downloading [{item_number}]... ') as bar:
                            for chunk in response.iter_content(chunk_size=8192):
                                file.write(chunk)
                                bar.update(len(chunk))
                if args.l and c_p not in ['n', 'stop'] or args.c == None:
                    try:
                        if sys.platform == "linux":
                            os.system(f"mv {title} {c_p if c_p not in ['n', 'stop'] and os.path.exists(c_p) else '/sdcard' if os.path.exists('/sdcard') else '../'}")
                            print("Done !")
                        else:
                            os.system(f"move {title} {c_p if c_p not in ['n', 'stop'] else '..'}")
                            print("Done !")
                    except Exception as ErrorMoving:
                         print(Fore.RED+f"ErrorMoving: {ErrorMoving}")
        if args.pl and c_p not in ['n', 'stop'] or args.c == None:
            try:
                plname = os.getcwd().split('/')[-1] if sys.platform == 'linux' else os.getcwd().split('\\')[-1]
                print(Fore.GREEN+f"Playlist [{plname}] has been downloaded successfully")
                if sys.platform == "linux":
                    dest = '/sdcard' if os.path.exists('/sdcard') and c_p in ['n', 'stop'] else c_p if os.path.exists(c_p) else '../'
                    os.system(f"cd ../ ; mv {plname} {dest}")
                else:
                        os.chdir("..")
                        dest = c_p if os.path.exists(c_p) else ".."
                        os.system(f"move {plname} {dest}")
            except Exception as plnameExp:
                        print(Fore.RED+f"plnameExp: {plnameExp}")         
        extractor = json.loads(AjaxReq.text)['extractor']
try:
    SocialMediaDownloader.Extractor()
except KeyboardInterrupt:
    print(Fore.YELLOW,"\nCanceled by the user")
    exit(0)
except Exception as ErrorOccured:
    exit(f"{Fore.RED} ErrorOccured: {ErrorOccured}")
