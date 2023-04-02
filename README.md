# google-image-scraper
A multithreaded Google Images scraper without Chromium. Only requires the python 
standard library, requests, and a few helper libraries. Aimed at being 
cross-platform, with a preference towards linux. 

**A Note:**

Scraping too aggressively can create large server loads, and lead to 503 errors. I'm sure this is less of an issue for Google, but please be considerate.
Thanks :)

**If you like the project give me a *Star ⭐***

## Usage

As of now, there's no packaging or runner scripts. You have to clone the repo,
manually install the dependencies, and run main with python.

### Clone the repo
```git clone https://github.com/talleyhoe/google-image-scraper.git```

### Install Dependencies
```pip install -r requirements.txt```

### Run main.py
```
$ -> python src/main.py [keyword]
optional arguments:
  --count, -c       How many images to try to scrape ( < 500 usually works )
  --directory, -d   What directory to save the images in 
                    (Default is ~/Downloads/[keyword]))
  --threads, -t     How many threads to scrape with
                    (Default is single threaded)
```

## Future Improvements
- Proper packaging 
- Extensibility to scrape other sites 
    - May not implement for a while unless there is sufficient interest
