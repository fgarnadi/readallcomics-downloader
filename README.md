# readallcomics-downloader

Scrapy spider to download comics from ReadAllComics

## Usage

Install the requirements (virtual env preferred)

```
python3 -m venv .venv && activate
pip install -r requirements.txt
```

Run the spider

```
scrapy runspider readallcomics.py -a category=nickelodeon-avatar-the-last-airbender-the-promise -s IMAGES_STORE=.
```

- `category` is the comic title that's going to be downloaded. It's the name after the category in url path `https://readallcomics.com/category/{category}/`
- `IMAGES_STORE` is the desired download path

## Acknowledgement

This program was inspired and modified from [batoto-downloader](https://github.com/curita/batoto-downloader)
