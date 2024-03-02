from django.db import models
from django.utils.translation import gettext_lazy

from apps.api.messages_fields import (DEPARTMENT,
                                      DEPARTMENTS,
                                      DEPARTMENT_COMPANY,
                                      DEPARTMENT_ADMINISTRATOR,
                                      COMPANY,
                                      ADDRESS,
                                      DESCRIPTION,
                                      IS_ACTIVE,
                                      CREATED_AT,
                                      UPDATED_AT,
                                      CREATOR)

from apps.api.user.models import User
from apps.api.company.models import Company
# from apps.api.administrator.models import Administrator  # todo: Uncommit, when Administrator model will be created



class Department(models.Model):
    company_id = models.ForeignKey(Company,
                                   on_delete=models.PROTECT,
                                   related_name=gettext_lazy(DEPARTMENTS),
                                   verbose_name=gettext_lazy(DEPARTMENT_COMPANY))

    # todo: Uncommit, when Administrator model will be created
    # administrator_id = models.ForeignKey(
    #                         Administrator,
    #                         on_delete=models.PROTECT,
    #                         related_name=gettext_lazy(DEPARTMENTS),
    #                         verbose_name=gettext_lazy(DEPARTMENT_ADMINISTRATOR))

    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=gettext_lazy(DEPARTMENT))

    address = models.CharField(max_length=300,
                               verbose_name=gettext_lazy(ADDRESS))

    description = models.TextField(max_length=500,
                                   blank=True, null=True,
                                   verbose_name=gettext_lazy(DESCRIPTION))

    is_active = models.BooleanField(default=True,
                                    verbose_name=gettext_lazy(IS_ACTIVE))

    created_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name=gettext_lazy(CREATED_AT))

    updated_at = models.DateTimeField(auto_now=True,
                                        verbose_name=gettext_lazy(UPDATED_AT))

    creator = models.ForeignKey(User,
                                on_delete=models.PROTECT,
                                related_name="department",
                                verbose_name=gettext_lazy(CREATOR))

    class Meta:
        verbose_name = gettext_lazy(DEPARTMENT)
        verbose_name_plural = gettext_lazy(DEPARTMENTS)
        ordering = ["name", "is_active"]

    def __str__(self):
        return f"{self.name}"
