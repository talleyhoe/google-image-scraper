import os 

def eprint(*args, **kwargs):
    """Print to stderr instead of stdout"""
    print(*args, file=sys.stderr, **kwargs)

def check_pos_int(val: int):
    val = int(val)
    if ( val > 0 ):
        return val
    else:
        raise ValueError

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
