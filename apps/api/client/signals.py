import os
from django.dispatch import receiver
from django.db.models.signals import (pre_delete,
                                      post_delete,
                                      pre_save,
                                      post_save)

from apps.api.client.models import Client

from django.conf import settings
from PIL import Image, UnidentifiedImageError

from apps.api.client.utils import get_image_file_name
from apps.api.utils.utils import (delete_file_default_storage,
                                  number_or_str_to_abs_int,
                                  )

from django.utils.translation import gettext_lazy

from apps.api.messages_api.messages_non_front import EXCEPTION_INFO

from apps.api.administrator.settings import (AVATAR_WIDTH,
                                             AVATAR_HEIGHT,
                                             IMAGE_QUALITY
                                             )


@receiver(pre_save, sender=Client)
def delete_old_avatar_before_client_save(sender, instance, **kwargs):

    if instance.pk and instance.thumbnail_link:  # Deleting old image file, so super() doesn't add hash to new file name
        try:
            old_img_proj_path_filename = sender.objects.get(
                                    pk=instance.pk).thumbnail_link.name

            new_img_proj_path_filename = instance.thumbnail_link.name

            if old_img_proj_path_filename:
                if old_img_proj_path_filename != new_img_proj_path_filename:

                    delete_file_default_storage(old_img_proj_path_filename)  # for cloud default_storage
                    # delete_file_os_remove(old_img_proj_path_filename)  # only for local storage

        except sender.DoesNotExist as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))


    if instance.pk and not instance.thumbnail_link:  # Delete img file, if img link was deleted in the model via front
        try:
            sender_obj_by_id = sender.objects.get(pk=instance.id)
            img_filename_pre_deletion_link = sender_obj_by_id.thumbnail_link.name

            delete_file_default_storage(img_filename_pre_deletion_link)  # for cloud default_storage
            # delete_file_os_remove(img_filename_pre_deletion_link)  # only for local storage

        except sender.DoesNotExist as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))


@receiver(post_save, sender=Client)
def open_resize_save_new_avatar_after_client_saved(sender, instance, **kwargs):

    if instance.pk and instance.thumbnail_link:  # Option 2, more complex: to resize image via PIL (pillow) lib
        try:
            proj_path_old_filename = instance.thumbnail_link.name
            base_old_filename = os.path.basename(instance.thumbnail_link.name)  # To get file ext from it in next step

            proj_path_new_filename_with_id = get_image_file_name(
                                            instance=instance,
                                            filename=base_old_filename)

            proj_path_new_filename_with_id = (
                proj_path_new_filename_with_id.replace("\\", "/"))

            full_path_new_filename_with_id = os.path.join(
                                        settings.MEDIA_ROOT,
                                        proj_path_new_filename_with_id)

            normalised_new_filename_with_id = os.path.normpath(
                                        full_path_new_filename_with_id)

            with Image.open(instance.thumbnail_link.path) as img:  # PIL.Image.open(): Resizing image
                img_width = number_or_str_to_abs_int(AVATAR_WIDTH)
                img_height = number_or_str_to_abs_int(AVATAR_HEIGHT)
                resample_quality = number_or_str_to_abs_int(IMAGE_QUALITY)

                img = img.resize(size=(img_width, img_height),
                                 resample=Image.BICUBIC)

                img.save(normalised_new_filename_with_id,
                         quality=resample_quality)

            sender_queryset_by_id = sender.objects.filter(pk=instance.pk)
            sender_queryset_by_id.update(thumbnail_link = proj_path_new_filename_with_id)  # Not save(), cycling signals occurs
            instance.thumbnail_link = proj_path_new_filename_with_id

            if proj_path_old_filename:  # Deleting previous file if filenames are different
                if proj_path_old_filename != proj_path_new_filename_with_id:

                    delete_file_default_storage(proj_path_old_filename)  # for cloud default_storage
                    # delete_file_os_remove(proj_path_old_filename)  # only for local storage

        except (sender.DoesNotExist, UnidentifiedImageError,
                IOError) as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))


@receiver(pre_delete, sender=Client)
def pre_delete_image_before_client_delete(sender, instance, **kwargs):
    pass  # for the future purposes


@receiver(post_delete, sender=Client)
def delete_avatar_after_client_deleted(sender, instance, **kwargs):
    if instance.pk and instance.thumbnail_link:  # Deleting image file when model instance was deleted
        try:
            file_name_to_delete = instance.thumbnail_link.name

            if file_name_to_delete:
                delete_file_default_storage(file_name_to_delete)  # for cloud default_storage
                # delete_file_os_remove(file_name_to_delete)  # only for local storage

        except sender.DoesNotExist as error:
            print(gettext_lazy(EXCEPTION_INFO(error)))
