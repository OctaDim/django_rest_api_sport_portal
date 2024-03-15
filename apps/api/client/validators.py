from apps.api.client.settings import MAX_IMAGE_FILE_SIZE_IN_MB
from apps.api.utils.utils import check_maximum_limit_image_file_size



def validate_image_size(image):
    check_maximum_limit_image_file_size(image, MAX_IMAGE_FILE_SIZE_IN_MB)
