import os
import pathlib
from datetime import datetime, UTC

from django.utils.translation import gettext_lazy
from apps.api.messages_api.messages_non_front import (EXCEPTION_INFO)


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

    file_name = (f"coach_id_{instance_id}_"
                 f"upd_{image_update_date}_"
                 f"thumbnail"
                 f"{file_ext}")

    full_path_file_name = os.path.join("api",
                                       "coach",
                                       "img",
                                       "thumbnail",
                                       file_name)
    return full_path_file_name
