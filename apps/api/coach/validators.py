from apps.api.coach.settings import MAX_IMAGE_FILE_SIZE_IN_MB
from apps.api.utils.utils import (check_maximum_limit_image_file_size,
                                  number_or_str_to_abs_float,
                                  )



def validate_image_size(image):
    max_image_file_size = number_or_str_to_abs_float(MAX_IMAGE_FILE_SIZE_IN_MB)
    check_maximum_limit_image_file_size(image, max_image_file_size)
