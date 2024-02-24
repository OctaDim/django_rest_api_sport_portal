import os
from PIL import Image  # Optional, if necessary
from datetime import datetime, UTC # Optional, if necessary


def get_image_file_name(instance, filename):
    path, ext = os.path.splitext(filename)
    level_value = f"{instance.value :04d}"
    # instance_name = instance.name  # Optional, if necessary
    # img_add_date = datetime.now(UTC).strftime("%Y_%m_%d")  # Optional, if necessary

    file_name = f"emotional_level_{level_value}_icon{ext}"
    full_path_file_name = os.path.join("api",
                                       "emotional_level",
                                       "img",
                                       "icon",
                                       file_name)
    return full_path_file_name
