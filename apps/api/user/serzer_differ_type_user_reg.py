from apps.api.user.serzer_user_reg import UserRegistrySerializer

# ##################################################################
# from django.contrib.auth.models import User  # Django default user
from apps.api.user.models import User  # Custom user
# ##################################################################





# ######################################################################
# ########################## TRIAL CODE ################################
# ######################################################################

class _Test_DifferentTypeUserRegistrySerializer(UserRegistrySerializer):  # Inherited from the ordinal user serializer

    def create(self, validated_data):
        validated_data.pop("password2")  # Refactored to avoid tedious getting values from validated_data via get()
        user = User.objects.__TEST_create_different_type_user(
                        # email=validated_data.get("email"),        # Refactored. Passing as **validated_data dictionary,
                        # username=validated_data.get("username"),  # instead of huge quantity of the named parameters
                        # nickname=validated_data.get("nickname"),
                        # first_name=validated_data.get("first_name"),
                        # last_name=validated_data.get("last_name"),
                        # phone=validated_data.get("phone"),
                        # password=validated_data.get("password"),
                        # is_staff=validated_data.get("is_staff"),
                        # is_superuser=validated_data.get("is_superuser"),
                        # is_verified=validated_data.get("is_verified"),
                        **validated_data
                        )
        return user

# ######################################################################
# ######################################################################
# ######################################################################
