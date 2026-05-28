# vixsrc_scraper

Small scraper for VixSrc movies and TV

## Usage

### Movie

```bash
vixsrc_scraper -t movie -id MOVIE_ID --name "Movie Name" --year 2019
```


## TV

```bash
vixsrc_scraper -t tv -id SERIES_ID --name "Series Name" --year 2010 --season 1 -ep 3
```

## Examples

```bash
for ep in {1..10}; do vixsrc_scraper -t tv -id SERIES_ID --name "Series Name" --year 2010 --season 1 -ep "$ep"; done
```

## Options
```bash
-t, --type       Content type: movie or tv
-id              Movie or series ID
--name           Movie or series name
--year           Movie or series year
--season         Season number, default: 1
-ep              Episode number, default: 1
--audiolang      Optional audio language
--sublang        Optional subtitle language
```
