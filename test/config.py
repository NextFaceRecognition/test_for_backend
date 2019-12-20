# Information of target server.
HOST_IP = 'localhost'
PORT = '5050'
ROOT_PATH = '/faceService/'
URL = 'http://' + HOST_IP + ':' + PORT + ROOT_PATH

# Type of user id.
UID_TYPE = '工号'

# Upload channel.
UPLOAD_CHANNEL = 'test script'

# Image name format.
IMAGE_NAME_FORMAT = r'(?P<user_id>\w+)-(?P<user_name>\w+)'

ALLOWED_FILE_TYPE = ['jpg', 'jpeg', 'png']
