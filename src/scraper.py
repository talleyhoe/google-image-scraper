import json, os, sys
from concurrent.futures import ThreadPoolExecutor

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
            results = get_image_urls(search_key, results_page)
            if results == {}:
                # No error was thrown, but we still got an empty dict from get_image_urls 
                # Likely means there are no more results on the page.
                # Without this, can get stuck in infinite loop.
                # So, break out of while loop with what we have (if anything)
                manifest_len = len(img_manifest.items())
                break

            img_manifest.update(results)
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
     
def scrape_images(search_key, image_cnt, directory, threads):
    """ 
    Request manifest, generate paths, save files, get filetype. 
    This is the only function that should be called externally. 

    Keyword arguments:
    search_key -- the raw text search request
    image_cnt -- how many images are we trying to scrape
    directory -- the folder to save scraped images in 
    threads -- how many worker threads to spawn
    """
    if DEBUG:
        print("savedir: {}".format(directory))
    if not os.path.exists(directory):
        os.makedirs(directory)

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

    scrape_images(search_key, image_cnt, directory, threads)
    

if __name__ == "__main__":
    test()
