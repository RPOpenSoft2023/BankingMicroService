from rest_framework import serializers
from . import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = '__all__'

    def save(self, **kwargs):
        phone_number = self.validated_data.get('phone_number')
        ifsccode = self.validated_data.get('ifsc')
        account_number = self.validated_data.get('account_number')
        if (len(str(phone_number)) != 10):
            raise serializers.ValidationError("Invalid phone_number no.")
        if len(str(ifsccode)) != 11:
            raise serializers.ValidationError("Invalid ifsc code")
        if len(str(account_number)) < 11 or len(str(account_number)) > 16:
            raise serializers.ValidationError("Invalid account no.")
        return super().save()


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transaction
        fields = '__all__'
