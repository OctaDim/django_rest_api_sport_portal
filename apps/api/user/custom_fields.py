from enumchoicefield import ChoiceEnum
from rest_framework.serializers import BooleanField

from django.utils.translation import gettext_lazy
from apps.api.messages import (YES_FIELD_CHOICE,
                               NO_FIELD_CHOICE,
                               )



BOOLEAN_CHOICES = [(True, gettext_lazy(YES_FIELD_CHOICE)),
                   (False, gettext_lazy(NO_FIELD_CHOICE)), ]


class CustomTrueByDefaultBooleanField(BooleanField):
    initial = True

class YesNoChoiceEnum(ChoiceEnum):
    Yes = True
    No = False
