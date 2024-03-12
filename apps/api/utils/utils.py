import os

from django.core.files.storage import default_storage

from django.utils.translation import gettext_lazy
from apps.api.messages_api.messages_non_front import (ERROR_OCCURRED)

from django.core.exceptions import ValidationError



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


def number_or_str_to_abs_int(number_or_str_number: int | float | str) -> int | None:
    try:
        number_or_str_number = str(number_or_str_number)
        number_or_str_number = number_or_str_number.replace(",", ".")
        integer_number = abs(int(number_or_str_number))
        return integer_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))


def number_or_str_to_abs_float(number_or_str_number: int | float | str) -> float | None:
    try:
        number_or_str_number = str(number_or_str_number)
        number_or_str_number = number_or_str_number.replace(",", ".")
        float_number = abs(float(number_or_str_number))
        return float_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))
