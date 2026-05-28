from pathlib import Path
from scrapling.fetchers import Fetcher
import json
import argparse
import yt_dlp

root = "https://vixsrc.to/"

def scraper():
    # Args
    parser = argparse.ArgumentParser(prog='vixsrc_scraper')
    parser.add_argument('-t', '--type', required=True, choices=['movie', 'tv'])
    parser.add_argument('-id', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--year', default=None)
    parser.add_argument('--season', default=1, type=int)
    parser.add_argument('-ep', default=1, type=int)
    parser.add_argument('--audiolang', default=None)
    parser.add_argument('--sublang', default=None)
    parser.add_argument('--fragments', default=4, type=int)

    args = parser.parse_args()

    # Video fetcher
    if args.type == "movie":
        url = root + "/api/movie/" + str(args.id)
    else:
        url = root + "/api/tv/" + str(args.id) + '/' + str(args.season) + '/' + str(args.ep) + '?lang=it'

    print(url)
    page = Fetcher.get(url)
    resp = json.loads(page.body)
    url = root[:-1] + resp['src']
    print(url)
    page = Fetcher.get(url)
    script = page.css("script::text").get()
    token   = script.split("'token': '")[1].split("'")[0]
    expires = script.split("'expires': '")[1].split("'")[0]
    url     = script.split("masterPlaylist = {")[1].split("url: '")[1].split("'")[0]
    print(url, token, expires)
    url = url + "?token=" + token + "&expires=" + expires + "&h=1&lang=it"
    page = Fetcher.get(url)

    # Output
    if args.year:
        title = f"{args.name} ({args.year})"
    else:
        title = args.name
    
    if args.type == "movie":
        folder = Path(title)
        output = folder / f"{title}.%(ext)s"
    else:
        folder = Path(title) / f"Season {args.season:02d}"
        output = folder / f"{args.name} S{args.season:02d}E{args.ep:02d}.%(ext)s"

    # Download
    audio_format = f'bestaudio[language={args.audiolang}]' if args.audiolang else 'bestaudio'

    ydl_opts = {
        'format': f'bestvideo+{audio_format}/best',
        'concurrent_fragment_downloads': args.fragments,
        'merge_output_format': 'mkv',
        'outtmpl': str(output),
    }

    if args.sublang:
        ydl_opts['writesubtitles'] = True
        ydl_opts['subtitleslangs'] = [args.sublang]
        ydl_opts['subtitlesformat'] = 'srt'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
