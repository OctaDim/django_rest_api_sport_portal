import os
import pathlib
from datetime import datetime, UTC

from django.core.files.storage import default_storage

from django.utils.translation import gettext_lazy
from apps.api.messages_non_front import (ERROR_OCCURRED,
                                         EXCEPTION_INFO)

from django.core.exceptions import ValidationError




def get_image_file_name(instance, filename):
    instance_id = None
    try:
        if instance.id:
           instance_id = f"{instance.id :05d}"
    except instance.DoesNotExist as error:
        print(gettext_lazy(EXCEPTION_INFO(error)))



    # instance_nickname = instance.user.nickname.lower()
    image_update_date = datetime.now(UTC).strftime("%Y_%m_%d")

    file_ext = pathlib.Path(filename).suffix
    # file_path, file_ext = os.path.splitext(filename)  # Optional, if necessary both path and ext

    file_name = (f"administrator_id_{instance_id}_"
                 f"upd_{image_update_date}_"
                 f"thumbnail"
                 f"{file_ext}")

    full_path_file_name = os.path.join("api",
                                       "administrator",
                                       "img",
                                       "thumbnail",
                                       file_name)
    return full_path_file_name


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
        integer_number = abs(int(number_or_str_number))
        return integer_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))


def number_or_str_to_float(number_or_str_number: int | float | str) -> float | None:
    try:
        float_number = abs(float(number_or_str_number))
        return float_number
    except (TypeError, ValueError) as error:
        raise ValidationError(gettext_lazy(ERROR_OCCURRED(error)))
