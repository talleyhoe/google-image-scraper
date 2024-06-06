import argparse, os, sys

# Should revisit this to look for xdg_downloads in env
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def get_default_dir(search_key: str):
    """Generate the default folder to store scraped images in"""
    search_key = search_key.replace(" ", ".")
    default_dir = get_download_path()
    default_dir = os.path.join(default_dir, "google-image-scraper")
    default_dir = os.path.join(default_dir, search_key)
    return default_dir

def check_pos_int(val: int):
    val = int(val)
    if ( val > 0 ):
        return val
    else:
        raise ValueError

def get_arguments(argv=sys.argv):
    """ 
    The cli front end for the scraper.

    Keyword arguments:
    argv -- An array of keywords expected to look like sys.argv
    
    Returns:
    parser.parse_args() -- A struct with all required info to run the scraper
    """
    parser = argparse.ArgumentParser(description="Scrape Google for images")
    parser.add_argument("keyword", 
                        help="the phrase used to find images",
                        type=str,
                        nargs="?")
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
    parser.add_argument("-s", "--size",
                        help="Restrict your search to a certain size of image.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["large","medium","icon", "400x300", "640x480",
                                 "800x600", "1024x768", "2mp", "4mp", "8mp",
                                 "10mp", "12mp", "15mp", "20mp", "40mp", "70mp"])
    parser.add_argument("-a", "--aspectratio",
                        help="Restrict to specific aspect ratios.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["tall", "square", "wide", "panoramic"])
    parser.add_argument("-i", "--color",
                        help="Search for a certain color of image.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["color", "grayscale", "transparent", "red", 
                                 "orange", "yellow", "green", "teal", "blue", 
                                 "purple", "pink", "white", "gray", "black", 
                                 "brown"])
    parser.add_argument("-k", "--type",
                        help="The type of image to search for.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["face", "photo", "clipart", 
                                 "lineart", "animated"],
                        dest="type")
    parser.add_argument("-r", "--region",
                        help="Get results from a specific country.",
                        type=str,
                        nargs="?",
                        default=None)
    parser.add_argument("-w", "--site",
                        help="Get results from a specific site or domain.",
                        type=str,
                        nargs="?",
                        default=None)
    parser.add_argument("-f", "--filetype",
                        help="Search for a specific file extension.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["jpg", "gif", "png", "bmp", 
                                 "svg", "webp", "ico", "raw"])
    parser.add_argument("-u", "--usage",
                        help="Specify usage rights.",
                        type=str,
                        nargs="?",
                        default=None,
                        choices=["cc", "other"])
    parser.add_argument("-p", "--safesearch",
                        help="Specify safesearch usage. Can be 'on' or 'off'.",
                        type=str,
                        nargs="?",
                        default="off",
                        choices=["on", "off"])
    args = parser.parse_args(argv[1:])
    # Set default directory
    if args.directory is None:
        print(args.keyword[0])
        args.directory = get_default_dir(args.keyword)
    return args
