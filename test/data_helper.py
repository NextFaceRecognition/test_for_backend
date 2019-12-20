import os
import re

from test.config import IMAGE_NAME_FORMAT


def parse_image_name(image_name):
    """This function is to parse user id, user name 
    from a given image name.
    """
    image_name, _ = os.path.splitext(image_name)
    m = re.match(IMAGE_NAME_FORMAT, image_name)
    uid = m.group('user_id')
    name = m.group('user_name')
    return uid, name
    
    