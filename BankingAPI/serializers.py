from rest_framework import serializers
from . import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = '__all__'

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        phone = validated_data.get('phone')
        ifsccode = validated_data.get('ifsc')
        account_number = validated_data.get(account_number)
        if (len(str(phone)) < 10):
            raise serializers.ValidationError("Invalid phone no.")
        if len(str(ifsccode)) < 11:
            raise serializers.ValidationError("Invalid ifsc code")
        if len(str(account_number)) < 11 or len(str(account_number)) > 16:
            raise serializers.ValidationError("Invalid account no.")
        self.validated_data = validated_data
        return super().save()


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transaction
        fields = '__all__'
