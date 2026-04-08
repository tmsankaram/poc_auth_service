from rest_framework.serializers import ModelSerializer
from ..models import CustomUser


class UserModelSerializer(ModelSerializer):
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "company_name",
            "department_code",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
