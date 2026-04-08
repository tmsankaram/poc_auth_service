from rest_framework.serializers import ModelSerializer, Serializer
from ..models import CustomUser


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "phone",
            "company_name",
            "job_title",
            "office_situated",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
