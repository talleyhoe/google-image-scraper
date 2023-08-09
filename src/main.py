import sys

from cli import get_arguments
from scraper import scrape_images

def main():
    args = get_arguments(sys.argv)
    scrape_images(args.keyword[0], args.count, args.directory, args.threads, args.size, args.aspectratio, args.color, args.imgtype, args.region, args.filetype, args.usage, args.safesearch)

if __name__ == "__main__":
    main()
