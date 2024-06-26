import os

from django.core.files.storage import default_storage

from django.utils.translation import gettext_lazy
from apps.api.messages_api.messages_non_front import ERROR_OCCURRED
from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from django.core.exceptions import ValidationError

from apps.api.messages_api.messages_errors import (MAXIMUM_FILE_SIZE,
                                                   LEVEL_VALUE_MIN_LIMIT,
                                                   LEVEL_VALUE_MAX_LIMIT)


def validate_level_value(value, level_min_limit, level_max_limit):
    if value < level_min_limit:
        raise ValidationError(gettext_lazy(
            LEVEL_VALUE_MIN_LIMIT(value, level_min_limit)))

    if value > level_max_limit:
        raise ValidationError(gettext_lazy(
            LEVEL_VALUE_MAX_LIMIT(value, level_max_limit)))


def check_maximum_limit_image_file_size(image, max_image_file_size_in_mb: float|int) -> None:
    try:
        file_size = image.file.size
        max_file_size = number_or_str_to_abs_float(max_image_file_size_in_mb)
        if file_size > max_file_size * 1024 * 1024:
            raise ValidationError(
                gettext_lazy(MAXIMUM_FILE_SIZE(max_file_size)))
    except (IOError, Exception) as error:
        print(gettext_lazy(EXCEPTION_INFO(error)))


def delete_file_default_storage(project_path_file_name):
    try:
        if default_storage.exists(project_path_file_name):  # for cloud default_storage
            default_storage.delete(project_path_file_name)  # for cloud default_storage
    except (IOError, ValueError) as error:
        print(gettext_lazy(ERROR_OCCURRED(error)))


def delete_file_os_remove(project_path_file_name):
    try:
        if os.path.exists(project_path_file_name):  # only for local storage
            os.remove(project_path_file_name)       # only for local storage
    except (IOError, ValueError) as error:
        print(gettext_lazy(ERROR_OCCURRED(error)))


def number_or_str_to_int(number_or_str_number: int | float | str) -> int | None:
    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")
        intermediate_float_number = float(number_or_str_number)
        non_fractional_integer_number = int(intermediate_float_number)
        return non_fractional_integer_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))


def number_or_str_to_abs_int(number_or_str_number: int | float | str) -> int | None:
    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")
        intermediate_float_number = float(number_or_str_number)
        positive_integer_number = abs(int(intermediate_float_number))
        return positive_integer_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))


def number_or_str_to_abs_float(number_or_str_number: int | float | str) -> float | None:
    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")
        positive_float_number = abs(float(number_or_str_number))
        return positive_float_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))


def get_abs_float_from_str_or_number(number_or_str_number: int | float | str) -> float | None:
    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")
        positive_float_number = abs(float(number_or_str_number))
        return positive_float_number
    except (TypeError, ValueError) as error:
        return None


def get_integer_from_str_or_number(number_or_str_number: int | float | str) -> int | None:
    try:
        number_or_str_number = str(number_or_str_number).strip()
        number_or_str_number = number_or_str_number.replace(",", ".")
        intermediate_float_number = float(number_or_str_number)
        non_fractional_integer_number = int(intermediate_float_number)
        return non_fractional_integer_number
    except (TypeError, ValueError) as error:
        return None
