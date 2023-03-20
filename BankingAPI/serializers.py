from rest_framework import serializers
from . import models


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = [
            'ifsc',
            'account_number',
            'account_opening_date',
            'account_type',
            'bank_name',
            'branch_address',
            'phone_number',
        ]

    def save(self, **kwargs):
        phone = self.validated_data.get('phone')
        if (len(str(phone)) < 10):
            raise serializers.ValidationError("Invalid phone no.")
        ifsccode = self.validated_data.get('ifsc')
        if len(str(ifsccode)) < 11:
            raise serializers.ValidationError("Invalid ifsc code")

        account_number = self.validated_data.get(account_number)
        if len(str(account_number)) < 11 or len(str(account_number)) > 16:
            raise serializers.ValidationError("Invalid account no.")
        return super().save(**kwargs)


class TransactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Transactions
        fields = "__all__ "
