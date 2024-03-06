from apps.api.messages_fields import (PASSWORD_NEW,
                                      NEW_PASSWORD_REPEATED)

from apps.api.messages_actions import (ENTER_NEW_PASSWORD,
                                       REPEAT_NEW_PASSWORD)

from apps.api.messages_errors import (PASSWORD_REQUIRED_MSG,
                                      PASSWORD2_REQUIRED_MSG,
                                      PASSWORDS_NOT_MATCH_ERROR,
                                      USER_CREATOR_REQUIRED)

from django import forms

from apps.api.user.models import User

from django.utils.translation import gettext_lazy




class UserCreationAdminCustomForm(forms.ModelForm):
    password = forms.CharField(max_length=128,
                                required=True,
                                widget=forms.PasswordInput,
                                help_text=gettext_lazy(ENTER_NEW_PASSWORD),
                                label=gettext_lazy(PASSWORD_NEW))

    password2 = forms.CharField(required=True,
                                max_length=128,
                                widget=forms.PasswordInput,
                                help_text=gettext_lazy(REPEAT_NEW_PASSWORD),
                                label=gettext_lazy(NEW_PASSWORD_REPEATED))

    class Meta:
        model = User
        fields = "__all__"


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        cleaned_data["password1"] = password

        error_messages = []

        ########## CHECK, IF USER CREATOR IS SELECTED ##################
        user_creator = self.cleaned_data.get("user_creator")
        if not user_creator:
            error_messages.append(USER_CREATOR_REQUIRED)

        ########## PASSWORD VALIDATION #################################
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if not password:
            error_messages.append(PASSWORD_REQUIRED_MSG)

        if not password2:
            error_messages.append(PASSWORD2_REQUIRED_MSG)

        if password != password2:
            error_messages.append(PASSWORDS_NOT_MATCH_ERROR)

        if error_messages:
            error_messages_str = " // ".join(error_messages)
            raise forms.ValidationError(gettext_lazy(error_messages_str))

        return cleaned_data



    ##################### FOR THE FUTURE ###############################
    # def clean_is_staff(self):
    # is_staff = self.cleaned_data.get("is_staff")
    # create_staff_allowed_roles = ["is_staff", "is_superuser"]
    # current_user = self.request if self.request else None
    # current_user_has_role = (any(getattr(current_user, role)
    #                              for role in create_staff_allowed_roles))
    #
    # if is_staff and not current_user_has_role:
    #     raise forms.ValidationError("New administrator/staff account can be created only by superuser or other administrator/staff")
    # return is_staff


    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password"])
    #     if commit:
    #         user.save()
    #     return user
