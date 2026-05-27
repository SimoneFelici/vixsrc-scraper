# aether-vix-scraper

Small CLI scraper for downloading movies or TV episodes from a vixsrc-compatible backend.

## Usage

```bash
aether-vix-scraper [-h] [--url URL] --name NAME [--audiolang AUDIOLANG] \
  (--movieid MOVIEID | --showid SHOWID) \
  [--season SEASON [SEASON ...]] \
  [--episode EPISODE [EPISODE ...]]
```

## Options

| Option | Description |
|---|---|
| `--url` | vixsrc backend URL. Defaults to `https://vix.aether.bar/`. |
| `--name` | Movie or TV show name. Used for output folders/files, roughly Jellyfin-style. |
| `--audiolang` | Audio language code, for example `it` or `en`. |
| `--movieid` | Movie ID. Mutually exclusive with `--showid`. |
| `--showid` | TV show ID. Mutually exclusive with `--movieid`. |
| `--season` | One or more season numbers. Required when using `--showid`. |
| `--episode` | One or more episode numbers. Optional. If omitted, the whole season is downloaded. |

## Examples

Download a movie:

```bash
aether-vix-scraper --movieid 12345 --name "Movie Name" --audiolang it
```

Download a full season:

```bash
aether-vix-scraper --showid 1618 --season 1 --name "Justice League" --audiolang it
```

Download multiple seasons:

```bash
aether-vix-scraper --showid 1618 --season 1 2 3 --name "Justice League" --audiolang it
```

Download specific episodes:

```bash
aether-vix-scraper --showid 1618 --season 1 --episode 1 4 25 --name "Justice League" --audiolang it
```

Download the same episode numbers across multiple seasons:

```bash
aether-vix-scraper --showid 1618 --season 1 2 --episode 1 2 --name "Justice League" --audiolang it
```

## Finding IDs

You can get the ID from the Aether URL.

Example:

```text
https://aether.bar/media/tmdb-tv-1618-justice-league/4435/82451
```

In this case, the show ID is:

```text
1618
```
