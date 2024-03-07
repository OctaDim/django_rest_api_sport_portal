from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from apps.api.utils.utils import number_or_str_to_float

from apps.api.client.settings import MAX_IMAGE_FILE_SIZE_IN_MB
from apps.api.messages_api.messages_errors import MAXIMUM_FILE_SIZE


def validate_image_size(image):
    file_size = image.file.size
    max_file_size = number_or_str_to_float(MAX_IMAGE_FILE_SIZE_IN_MB)
    if file_size > max_file_size * 1024 * 1024:
        raise ValidationError(
            gettext_lazy(MAXIMUM_FILE_SIZE(max_file_size)))
