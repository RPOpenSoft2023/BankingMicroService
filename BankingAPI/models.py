from django.db import models

from django.utils import timezone


# Create your models here.
class Account(models.Model):

    ifsc = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, primary_key=True)
    account_opening_date = models.DateField(null=True, blank=True)
    account_type = models.CharField(max_length=255, null=True, blank=True)
    bank_name = models.CharField(max_length=255, null=True, blank=True)
    branch_name = models.CharField(max_length=255, null=True, blank=True)
    branch_address = models.TextField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.account_number)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class Transaction(models.Model):

    CATEGORY_CHOICES = (('shoppingAndFood', 'shoppingAndFood'),
                        ('others', 'others'), ('travelling', 'travelling'),
                        ('investmentAndSaving', 'investmentAndSaving'),
                        ('medicalAndHealthcare',
                         'medicalAndHealthcare'), ('utilities', 'utilities'))

    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    debit = models.IntegerField(null=True, blank=True)
    credit = models.IntegerField(null=True, blank=True)
    balance = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(to='Account', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=255,
                                null=True,
                                blank=True,
                                choices=CATEGORY_CHOICES,
                                default='others')
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.description)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'