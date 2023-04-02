import fnmatch, os, sys, unittest

rootdir = os.path.abspath('./')
srcdir = os.path.join(rootdir, 'src')
sys.path.insert(1, rootdir)
sys.path.insert(1, srcdir)
from scraper import *

class TestScraper(unittest.TestCase):

    def test_sanitize_query(self):
        query =  " look at this weird string  "
        answer = "+look+at+this+weird+string++"
        sanitized = sanitize_query(query)
        self.assertEqual(sanitized, answer, 
                         "Sanitiezed query: {} | should be {}"
                         .format(sanitized, answer))

    def test_add_filetype(self):
        img_path = os.path.join(rootdir, 'tests', 'images', 'ftype')
        img_types = ["gif", "jpeg", "png", "webp"]
        os.system(os.path.join(img_path, 'ftype_prep.sh'))
        for file_type in img_types:
            test_folder = os.path.join(img_path, file_type, 'test')
            file_path = os.path.join(test_folder, 'image')
            add_filetype(file_path)
            self.assertTrue(os.path.exists(f"{file_path}.{file_type}"),
                            msg=f"Couldn't assign image type {file_type}")
    
    def test_get_image_urls(self):
        query = "linux"
        img_urls = get_image_urls(query, 1)
        self.assertGreater(len(next(iter(img_urls.keys()))),   0)
        self.assertGreater(len(next(iter(img_urls.values()))), 0)

    def test_download_image(self):
        img_name = "brazil-elections-2022-first-round.png"
        save_path = os.path.join(rootdir, 'tests', 'images', 'download', img_name)
        img_url = ("https://www.google.com/logos/doodles/2022/"
                   "brazil-elections-2022-first-round-6753651837109514-2x.png")
        if os.path.exists(save_path):
            os.unlink(save_path)
        download_image(img_url, save_path)
        self.assertTrue(os.path.exists(save_path), "Error downloading doodle")

if __name__ == "__main__":
    unittest.main()
