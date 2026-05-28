# vixsrc_scraper

Small scraper for VixSrc

## Usage

### Movie

```bash
vixsrc-scraper -t movie -id MOVIE_ID --name "Movie Name" --year 2019
```

## TV

```bash
vixsrc-scraper -t tv -id SERIES_ID --name "Series Name" --year 2010 --season 1 -ep 3
```

## Examples

Download episodes 1 to 10 from season 1:
```bash
for ep in {1..10}; do vixsrc-scraper -t tv -id SERIES_ID --name "Series Name" --year 2010 --season 1 -ep "$ep"; done
```

## Options

```bash
-t, --type       Content type: movie or tv
-id              TMDB ID (https://www.themoviedb.org/)
--name           Output name
--year           Optional output year
--season         Season number, default: 1
-ep              Episode number, default: 1
--audiolang      Optional audio language, ex: (ita, eng)
--sublang        Optional subtitle language
```
