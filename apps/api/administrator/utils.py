import os
import pathlib
from time import strftime  # Optional, if necessary
from PIL import Image  # Optional, if necessary
from datetime import datetime, UTC # Optional, if necessary


def get_image_file_name(instance, filename):
    id = f"{instance.id :04d}"
    file_ext = pathlib.Path(filename).suffix

    # file_path, file_ext = os.path.splitext(filename)       # Optional, if necessary both path and ext
    # instance_name = instance.name                          # Optional, if necessary
    # img_add_date = datetime.now(UTC).strftime("%Y_%m_%d")  # Optional, if necessary

    file_name = f"administrator_avatar_{id}_thumbnail{file_ext}"
    full_path_file_name = os.path.join("api",
                                       "administrator",
                                       "img",
                                       "thumbnail",
                                       file_name)
    return full_path_file_name
