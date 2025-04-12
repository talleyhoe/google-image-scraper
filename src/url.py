# NOTE: This is not currently used

def process_image_size(val: str):
    """Get the proper search key for specified image size"""
    img_sizes = {
            "large": "l",
            "medium": "m",
            "icon": "i",
            "400x300":  "lt%2Cislt:" + "qsvga",
            "640x480":  "lt%2Cislt:" + "vga",
            "800x600":  "lt%2Cislt:" + "svga",
            "1024x768": "lt%2Cislt:" + "xga",
            "2mp":  "lt%2Cislt:" + "2mp",
            "4mp":  "lt%2Cislt:" + "4mp",
            "6mp":  "lt%2Cislt:" + "6mp",
            "8mp":  "lt%2Cislt:" + "8mp",
            "10mp": "lt%2Cislt:" + "10mp",
            "12mp": "lt%2Cislt:" + "12mp",
            "15mp": "lt%2Cislt:" + "15mp",
            "20mp": "lt%2Cislt:" + "20mp",
            "40mp": "lt%2Cislt:" + "40mp",
            "70mp": "lt%2Cislt:" + "70mp",
    }
    try: 
        filter_tag = img_sizes[val]
    except Exception as err:
        eprint("Couldn't parse specified image size.")
        eprint(err)
        sys.exit(1)

    return "isz:" + filter_tag


def process_image_aspectratio(val: str):
    img_aspect_ratios = {
            "tall": "t",
            "square": "s",
            "wide": "w",
            "panoramic": "xw"
    }
    try: 
        filter_tag = img_aspect_ratios[val]
    except Exception as err:
        eprint("Couldn't parse specified image aspect ratio.")
        eprint(err)
        sys.exit(1)

    return "iar:" + filter_tag


def process_image_color(val: str):
    img_colors = {
            "color": "color",
            "grayscale": "gray",
            "transparent": "trans",
            "black":  "specific%2Cisc:" + "black",
            "blue":   "specific%2Cisc:" + "blue",
            "brown":  "specific%2Cisc:" + "brown",
            "gray":   "specific%2Cisc:" + "gray",
            "green":  "specific%2Cisc:" + "green",
            "orange": "specific%2Cisc:" + "orange",
            "red":    "specific%2Cisc:" + "red",
            "teal":   "specific%2Cisc:" + "teal",
            "pink":   "specific%2Cisc:" + "pink",
            "purple": "specific%2Cisc:" + "purple",
            "white":  "specific%2Cisc:" + "white",
            "yellow": "specific%2Cisc:" + "yellow",
    }
    try: 
        filter_tag = img_colors[val]
    except Exception as err:
        eprint("Couldn't parse specified image color.")
        eprint(err)
        sys.exit(1)

    return "ic:" + filter_tag


def process_image_type(val: str):
    if (val in ["face", "photo", "clipart", "lineart", "animated"]):
        return "itp:" + val
    else:
        eprint(f"Couldn't parse specified image filetype. Recieved: {val}")
        sys.exit(1)

def process_image_region(val: str):
    country_codes = []
    if (val in country_codes):
        return "ctr:country" + val.upper()
    else:
        eprint(f"Couldn't parse specified image region. Recieved: {val}")
        sys.exit(1)

def process_image_filetype(val: str):
    if (val in ["jpg", "gif", "png", "bmp", "svg", "webp", "ico", "raw"]):
        return "ift:" + val
    else:
        eprint(f"Couldn't parse specified image filetype. Recieved: {val}")
        sys.exit(1)

def process_image_usage(val: str):
    # There should be 3 options here? (commercial, cc, and all)
    img_usage_rights = {
            "cc": "cl",
            "other": "ol"
    }
    try: 
        filter_tag = img_usage_rights[val]
    except Exception as err:
        eprint("Couldn't parse specified image usage rights.")
        eprint(err)
        sys.exit(1)

    return "sur:" + filter_tag
