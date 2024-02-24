import os
import pathlib
from PIL import Image  # Optional, if necessary
from datetime import datetime, UTC # Optional, if necessary


def get_image_file_name(instance, filename):
    level_value = f"{instance.value :04d}"
    file_ext = pathlib.Path(filename).suffix

    # file_path, file_ext = os.path.splitext(filename)
    # instance_name = instance.name                          # Optional, if necessary
    # img_add_date = datetime.now(UTC).strftime("%Y_%m_%d")  # Optional, if necessary

    file_name = f"emotional_level_{level_value}_icon{file_ext}"
    full_path_file_name = os.path.join("api",
                                       "emotional_level",
                                       "img",
                                       "icon",
                                       file_name)
    return full_path_file_name
