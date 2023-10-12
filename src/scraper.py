import json, os, sys
from concurrent.futures import ThreadPoolExecutor
from copy import copy

import filetype
import requests
from tqdm.contrib.concurrent import thread_map
from tqdm import tqdm

from cli import get_default_dir

DEBUG = False

# The url we're requesting, and our request's headers (browser spoof)
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'}
search_url = "https://www.google.com/search?q={}&tbm=isch&async=_id:islrg_c,_fmt:json&asearch=ichunklite&ijn={}"

############################# utility functions ###############################

def sanitize_query(query: str):
    """Replace spaces with '+' symbols. Needed for url injection."""
    return query.replace(' ','+')

def eprint(*args, **kwargs):
    """Print to stderr instead of stdout"""
    print(*args, file=sys.stderr, **kwargs)


def add_filetype(file_path: str):
    """Try to guess an image's file type and rename the file."""
    try:
        img_type = filetype.guess(file_path).mime.split('/')[-1]
    except:
        img_type = 'jpg'
    # This just replaces any filetypes (existing or not) with the new type
    new_path = '.'.join((os.path.splitext(file_path)[0], img_type))
    try:
        os.rename(file_path, new_path)
        return 0
    except Exception as err:
        eprint("Couldn't rename file at path {}".format(file_path))
        eprint(err)
        return 1


def process_image_size(val: str):
    # This can be refactored to use maps and eliminate redundancy (test first)
    key = 'isz:'
    if (val == 'large'):
        return key + 'l'
    elif (val == 'medium'):
        return key + 'm'
    elif (val == 'icon'):
        return key + 'i'
    elif (val in ['400x300', '640x480', '800x600', '1024x768']):
        key += 'lt%2Cislt:' 
        if (val == '400x300'):
            return key + "qsvga"
        elif (val == '640x480'):
            return key + "vga"
        elif (val == '800x600'):
            return key + "svga"
        elif (val == '1024x768'):
            return key + "xga"
    elif (val in ['2mp','4mp','6mp','8mp','10mp',
                  '12mp','15mp','20mp','40mp','70mp']):
        return key + 'lt%2Cislt:' + val 
    else:
        return ""

def process_image_aspectratio(val: str):
    key = 'iar:'
    if (val == 'tall'):
        return key + 't'
    elif (val == 'square'):
        return key + 's'
    elif (val == 'wide'):
        return key + 'w'
    elif (val == 'panoramic'):
        return key + 'xw'

def process_image_color(val: str):
    if (val == "color"):
        return "ic:color"
    elif (val == "grayscale"):
        return "ic:gray"
    elif (val == "transparent"):
        return "ic:trans"
    elif (val in ['red','orange','yellow','green','teal','blue',
                  'purple','pink','white','gray','black','brown']):
        return "ic:specific%2Cisc:" + val
    else:
        return ""

def process_image_type(val: str):
    if (val in ['face', 'photo', 'clipart', 'lineart', 'animated']):
        return 'itp:' + val
    else:
        return ""

def process_image_region(val: str):
    if (val != None):
        return 'ctr:country' + val.upper()

def process_image_filetype(val: str):
    if (val in ['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico', 'raw']):
        return 'ift:' + val

def process_image_usage(val: str):
    key = 'sur:'
    if (val == 'cc'):
        return key + 'cl'
    elif (val == 'other'):
        return key + 'ol'
    else:
        return ''


def setup_url(filters):
    global search_url 
    filtered_url = copy(search_url)

    features = [search_url]
    url_ids = []

    filter_keys = list(filters.keys())
    # Need to confirm we can't put these into the tbs tag
    if filters["safesearch"] == "on":
        filtered_url += "&safe=on"
    if filters["site"] != None:
        filtered_url += ("&as_sitesearch=" + filters["site"])
    filter_keys.remove("safesearch")
    filter_keys.remove("site")
    # if filters["region"] != None:
    #     filtered_url += ("&" + process_image_region(filters["region"]))
    # filter_keys.remove("region")

    # append_val = (lambda l, a: l.append(a) if a is not None)
    def append_val(l, v):
        if v is not None:
            l.append(v)
    for k in filter_keys:
        function_name = "process_image_" + k
        process_function = globals()[function_name]
        append_val(url_ids, process_function(filters[k]))

    delim = ","
    if (url_ids[0] != []):
        filtered_url += "&tbs=" + delim.join(url_ids)

    return filtered_url


############################# scraping helpers ################################

def get_image_urls(query: str, page: int):
    """
    Requests a mapping of image id's to source urls from Google Images

    Keyword arguments:
    query -- what you're searching for (must be sanitized)
    page  -- what page of results to return

    Returns:
    all_images -- a hash map of structure (id, url)
    """

    all_images = {}

    try:
        response = requests.get(search_url.format(query, page), headers=headers)

        if (response.status_code == 200):
            json_text = response.content.decode('utf8').removeprefix(")]}'")
            json_data = json.loads(json_text)
            try:
                results = json_data['ichunklite']['results']
                for result in results:
                    id = result['image_docid']
                    image_url = result['viewer_metadata']['original_image']['url']
                    all_images[id] = image_url

            except Exception as err:
                if DEBUG:
                    eprint(f"ERROR: Issue parsing json file for page {page}")
                    eprint(err)
        else:
            if DEBUG:
                eprint("ERROR: Status code {} for page {}."
                       .format(response.status_code, page))
            
    except Exception as err:
        if DEBUG:
            eprint("ERROR: There was an issue requesting the json file")
            eprint(err)

    return all_images


def download_image(img_url: str, file_path: str):
    """ 
    Download an image from a source url. 

    Keyword arguments:
    img_url   -- the source url of the image
    file_path -- where to save the image
    """
    try:
        response = requests.get(img_url, headers=headers)
    except Exception as err:
        if DEBUG:
            eprint(f"ERROR: Can't request image url: {img_url}")
            eprint(err)
        return 1

    if response.status_code == 200:
        response_content_type = response.headers.get("content-type", '').lower()
        if "image" in response_content_type:
            with open(file_path, 'wb') as img:
                img.write(response.content)
            add_filetype(file_path)
            return 0
        else:
            if DEBUG:
                eprint("ERROR: Bad content-type\n{}"
                       .format(response_content_type))
            return 1
    else:
        if DEBUG:
            eprint("ERROR: Status code {} for url {}."
                   .format(response.status_code, url))
        return 1


def get_manifest(search_key: str, image_cnt: int):
    """ 
    Try to populate a manifest matching content ids and image urls

    Keyword arguments:
    search_key -- the raw text search request
    image_cnt -- how many images are we trying to scrape

    Returns:
    img_manifest -- an array of (id, url) tuples 
    """
    err_cnt = 0
    err_limit = 5

    img_manifest = {}
    manifest_len = image_cnt

    results_page = 0
    search_key = sanitize_query(search_key)
    while ( len(img_manifest.items()) < image_cnt ): 
        try:
            img_manifest.update(get_image_urls(search_key, results_page))
            results_page += 1
        except:
            print(f"err_cnt: {err_cnt}")
            err_cnt += 1
        if (err_cnt > err_limit):
            eprint("Couldn't request all images")
            manifest_len = len(img_manifest.items())
            break
    # For some versions of python3 hashmaps are unordered => non-deterministic
    # This could be optimized with itertools
    print("Found {} of {} image sources".format(manifest_len, image_cnt))
    return list(img_manifest.items())[0:manifest_len]

################################# main api ####################################
     
def scrape_images(search_key, image_cnt, directory, threads, filters):
    """ 
    Request manifest, generate paths, save files, get filetype. 
    This is the only function that should be called externally. 

    Keyword arguments:
    search_key -- the raw text search request
    image_cnt -- how many images are we trying to scrape
    directory -- the folder to save scraped images in 
    threads -- how many worker threads to spawn
    filters -- hashmap of image filters to apply to the search results
    """
    if DEBUG:
        print("savedir: {}".format(directory))
    if not os.path.exists(directory):
        os.makedirs(directory)
    search_url = setup_url(filters)
    id_url_manifest = get_manifest(search_key, image_cnt)
    with ThreadPoolExecutor(max_workers=threads) as pool:
        with tqdm(total=len(id_url_manifest)) as progress:
            futures = [] # This is just to update the tqdm progress bar
            for result in id_url_manifest:
                id: str = result[0]
                url: str = result[1]
                save_path = os.path.join(directory, id)
                future = pool.submit(download_image, url, save_path)
                future.add_done_callback(lambda p: progress.update(1))
                futures.append(future)

            # Check who's done after submitting all jobs
            for future in futures:
                result = future.result()
    return 0


# If you run this file directly, you can test a default search
def test():
    globals()['DEBUG'] = True

    search_key = "arch linux"
    image_cnt  = 20
    directory  = get_default_dir(search_key)
    threads    = 4

    filters = {
        "size": "large",
        "aspectratio": "panoramic",
        "color": "green",
        "type": "clipart",
        "region": "CA", # Needs a mapping of inputs to country choices
                       # Use an import statement and roll in another file
        "site": "laksjdf",
        "filetype": "png",
        "usage": "other",
        "safesearch": "on"
    }

    scrape_images(search_key, image_cnt, directory, threads, filters)
    

if __name__ == "__main__":
    test()
