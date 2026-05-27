from scrapling.fetchers import Fetcher
import argparse
import json
import base64
from pathlib import Path
import yt_dlp
from yt_dlp.utils import DownloadError

HEADERS = {
    'Referer': 'https://aether.bar/media/idkidk123-test/12345/12345',
}

def run_ytdlp(video: str, output: Path) -> bool:
    if output.exists():
        print(f'Already exists: {output}')
        return True

    ydl_opts = {
        'concurrent_fragment_downloads': 5,
        'fragment_retries': 20,
        'skip_unavailable_fragments': False,
        'http_headers': HEADERS,
        'merge_output_format': 'mkv',
        'remuxvideo': 'mkv',
        'outtmpl': str(output.with_suffix('.%(ext)s')),
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([video])
    except DownloadError:
        print(f'yt-dlp failed: {output}')
        return False

    if result != 0:
        print(f'yt-dlp failed: {output}')
        return False

    print(f'Completed: {output}')
    return True

def get_page(url: str):
    return Fetcher.get(
        url,
        headers=HEADERS,
        stealthy_headers=False,
    )

def build_movie_path(name: str) -> Path:
    folder = Path(name)
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f'{name}.mkv'


def build_episode_path(name: str, season: int, ep: int) -> Path:
    season_str = f'Season {season:02d}'
    ep_str = f'S{season:02d}E{ep:02d}'

    folder = Path(name) / season_str
    folder.mkdir(parents=True, exist_ok=True)

    return folder / f'{name} {ep_str}.mkv'

def change_lang(video: str, urlang: str) -> str:
    video, encoded = video.rsplit('/', 1)
    padding = '=' * (-len(encoded) % 4)
    decoded = base64.urlsafe_b64decode(encoded + padding).decode()
    decoded = decoded.replace('lang=en', f'lang={urlang}')
    encoded = base64.urlsafe_b64encode(decoded.encode()).decode().rstrip('=')
    return video + '/' + encoded

def fetch_video_url(endpoint_url: str, lang: str | None = None) -> str | None:
    page = get_page(endpoint_url)

    if page.status != 200:
        print(f'Error fetching {endpoint_url}: HTTP {page.status}')
        return None

    try:
        res = json.loads(page.body)
    except json.JSONDecodeError as exc:
        print(f'Error parsing JSON from {endpoint_url}: {exc}')
        return None

    if 'error' in res:
        print(f'API error for {endpoint_url}: {res["error"]}')
        return None

    video = res.get('streamUrl')
    if not video:
        print(f'No streamUrl found for {endpoint_url}')
        return None

    if lang:
        video = change_lang(video, lang)

    return video

def fetch_episode(base_url: str, show: str, season: int, ep: int, lang: str | None, name: str) -> bool:
    endpoint_url = f'{base_url.rstrip("/")}/tv/{show}/{season}/{ep}'
    video = fetch_video_url(endpoint_url, lang)

    if not video:
        return False

    output = build_episode_path(name=name, season=season, ep=ep)
    return run_ytdlp(video, output)

def scraper() -> None:
    parser = argparse.ArgumentParser(prog='aether-vix-scraper')
    parser.add_argument('--url', default='https://vix.aether.bar/')
    parser.add_argument('--name', required=True)
    parser.add_argument('--audiolang')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--movieid')
    group.add_argument('--showid')

    parser.add_argument(
        '--season',
        type=int,
        nargs='+',
        help='One or more seasons, e.g. --season 1 or --season 1 2 3',
    )

    parser.add_argument(
        '--episode',
        type=int,
        nargs='+',
        help='One or more episodes, e.g. --episode 1 or --episode 1 2 3',
    )

    args = parser.parse_args()

    if args.movieid:
        if args.season or args.episode:
            parser.error('--season/--episode can only be used with --showid')
    
        endpoint_url = f'{args.url.rstrip("/")}/movie/{args.movieid}'
        video = fetch_video_url(endpoint_url, args.audiolang)
    
        if not video:
            print('Error fetching movie')
            raise SystemExit(1)
    
        output = build_movie_path(args.name)
    
        if not run_ytdlp(video, output):
            raise SystemExit(1)
    
        return

    if not args.season:
        parser.error('--season is required when using --showid')

    seasons: list[int] = args.season
    episodes: list[int] | None = args.episode

    failed: list[str] = []

    for season in seasons:
        if episodes:
            for ep in episodes:
                label = f'S{season:02d}E{ep:02d}'
                print(f'--- {label} ---')

                ok = fetch_episode(
                    base_url=args.url,
                    show=args.showid,
                    season=season,
                    ep=ep,
                    lang=args.audiolang,
                    name=args.name,
                )

                if not ok:
                    print(f'Failed: {label}')
                    failed.append(label)

            continue

        ep = 1
        downloaded = 0

        print(f'--- Season {season:02d} ---')

        while fetch_episode(
            base_url=args.url,
            show=args.showid,
            season=season,
            ep=ep,
            lang=args.audiolang,
            name=args.name,
        ):
            downloaded += 1
            ep += 1

        if downloaded == 0:
            print(f'No episodes downloaded for season {season}')
            failed.append(f'S{season:02d}')
        else:
            print(f'Season {season} done - {downloaded} episodes downloaded')

    if failed:
        print('Failed items:')
        for item in failed:
            print(f'  {item}')
        raise SystemExit(1)
