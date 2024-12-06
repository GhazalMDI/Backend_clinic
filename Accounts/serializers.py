from rest_framework import serializers
from Accounts.models import User, AddressModel, OtpModel


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'birthday', 'national_code')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ('formatted_address', 'state', 'county', 'neighbourhood')
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        return AddressModel.objects.created(**validated_data)


class OtpSerializers(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)



    def create(self, validated_data):
        return  OtpModel.objects.create(**validated_data)
