import argparse, sys

from utils import get_default_dir

def get_arguments(argv=sys.argv):
    """ 
    The cli front end for the scraper.

    Keyword arguments:
    argv -- An array of keywords expected to look like sys.argv
    
    Returns:
    parser.parse_args() -- A struct with all required info to run the scraper
    """
    parser = argparse.ArgumentParser(description="Scrape google for images")
    parser.add_argument("keyword", 
                        help="the phrase used to find images",
                        type=str,
                        nargs=1)
    parser.add_argument("-c", "--count",
                        help="How many images to try to scrape",
                        type=check_pos_int,
                        nargs="?",
                        default=10)
    parser.add_argument("-d", "--directory",
                        help="where to save scraped images",
                        type=str,
                        nargs="?")
    parser.add_argument("-t", "--threads",
                        help="How many threads to spawn and download from",
                        type=check_pos_int,
                        nargs="?",
                        default=1)
    args = parser.parse_args(argv[1:])
    # Set default directory
    if args.directory is None:
        print(args.keyword[0])
        args.directory = get_default_dir(args.keyword[0])
    return args
