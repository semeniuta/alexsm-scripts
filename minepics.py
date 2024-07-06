import os
from pathlib import Path
from datetime import datetime
import argparse
from PIL import Image
from PIL.ExifTags import TAGS as ImageExifTags


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('rootdir')
    return parser.parse_args()


def guess_format_from_extension(filename):

    IMAGE_FORMATS = {
        'jpg': 'jpg',
        'jpeg': 'jpg',
        'heic': 'heic'
    }

    IMAGE_EXTENSIONS = ('jpg', 'jpeg', 'heic')
    for ext in IMAGE_EXTENSIONS:
        for ext_variant in (ext, ext.upper()):
            if filename.endswith(f'.{ext_variant}'):
                return IMAGE_FORMATS[ext]
    return 'other'


def parse_exif_tags(im):

    exif_data = im.getexif()

    data = {}

    for tag_id in exif_data:
        tag = ImageExifTags.get(tag_id)
        value = exif_data.get(tag_id)
        data[tag] = value

    return data


def get_mtime(filename):
    return os.stat(filename)[-2]


def get_exif_datetime(filename):

    try:
        im = Image.open(filename)
    except Exception as _:
        return None

    exif_data = parse_exif_tags(im)

    if 'DateTime' not in exif_data:
        return None

    return exif_data['DateTime']


if __name__ == '__main__':

    args = parse_args()
    
    for root, dirs, files in os.walk(args.rootdir):

        for filename in files:
            im_format = guess_format_from_extension(filename)

            if im_format == 'other':
                continue

            full_path = os.path.join(root, filename)

            mtime_ts = datetime.fromtimestamp(get_mtime(full_path))
            exif_datetime = get_exif_datetime(full_path) if im_format == 'jpg' else None
            exif_datetime_str = f'exif="{exif_datetime}"' if exif_datetime else ''

            print(f'{full_path} {mtime_ts} {exif_datetime_str}')
