import sys

from cli import get_arguments
from scraper import scrape_images

def main():
    args = get_arguments(sys.argv)
    print(args)
    print(args.keyword)
    filters = {
        "size": args.size,
        "aspectratio": args.aspectratio,
        "color": args.color,
        "type": args.type,
        "region": args.region,
        "site": args.site,
        "filetype": args.filetype,
        "usage": args.usage,
        "safesearch": args.safesearch,
    }
    scrape_images(args.keyword, args.count, args.directory, args.threads, filters)

if __name__ == "__main__":
    main()
