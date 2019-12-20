from urllib import parse, request
import json
import os
import base64
import datetime

from test.config import URL, UID_TYPE, UPLOAD_CHANNEL


class Agent(object):
    """Agent class is used to provide an interface to send request to server."""

    def _post(self, url, data):
        """Send a POST request to server."""
        req = request.Request(url=url, data=data)
        res = request.urlopen(req)
        res = res.read()
        return res

    def _get(self, url):
        """Send a GET request to server."""
        req = request.Request(url=url)
        res = request.urlopen(req)
        res = res.read()
        return res

    def _stringnify(self, data):
        """Code the data to post."""
        data = parse.urlencode(data).encode('utf-8')
        return data

    def _read_img(self, img_path):
        """Read an image from file system, and encode to base64."""
        img = open(img_path, "rb")
        img_encoding = base64.b64encode(img.read())
        img.close()
        return img_encoding

    def _generate_data(self, uid, name, img_encoding):
        data = {}
        data['uid'] = uid
        data['uid_type'] = UID_TYPE
        data['name'] = name
        data['channel'] = UPLOAD_CHANNEL
        data['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['img'] = img_encoding
        return data

    def add_face(self, uid, name, img_path):
        """Send add face request.
        
        Args:
            uid: user's id.
            name: user's name.
            img_path: file path of face image.
        
        Return:
            res: a dict of response from server.
        """
        img_encoding = self._read_img(img_path)
        url = os.path.join(URL, 'addFaces')
        data = self._generate_data(uid, name, img_encoding)
        data = self._stringnify(data)
        res = self._post(url, data)
        return json.loads(res)

    def check_person(self, uid, name, img_path, mode='1v1'):
        """Send check person request.
        
        Args:
            uid: user's id.
            name: user's name.
            img_path: file path of face image.
            mode: check person mode, '1v1' or '1vn'.
        
        Return:
            res: a dict of response from server.
        """
        img_encoding = self._read_img(img_path)
        url = os.path.join(URL, 'checkPerson')
        data = self._generate_data(uid, name, img_encoding)
        data['mode'] = mode
        data = self._stringnify(data)
        res = self._post(url, data)
        return json.loads(res)

