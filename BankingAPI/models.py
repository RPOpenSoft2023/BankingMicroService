from django.db import models

from django.utils import timezone


# Create your models here.
class Account(models.Model):

    ifsc = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.BigIntegerField(primary_key=True)
    account_opening_date = models.DateField(null=True, blank=True)
    account_type = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    branch_address = models.TextField(max_length=255, null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.account_number)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Transactions(models.Model):

    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    debit = models.IntegerField(null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(to='Account', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'