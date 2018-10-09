from django.db import models
from django.utils.translation import ugettext_lazy as _

from operations import constants as c
from accounts.models import User, FarmerProfile, MerchantProfile
# Create your models here.


class Farm(models.Model):
    name = models.CharField(
        _('Farm name'),
        max_length=30
    )
    address = models.TextField(
        _('Farm address'),
        blank=True
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    size = models.IntegerField(
        _('size'),
        blank=True,
        null=True
    )
    owner_profile = models.ForeignKey(
        FarmerProfile,
        on_delete=models.CASCADE,
        related_name='farms'
    )
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )


class Offering(models.Model):
    name = models.CharField(
        _('name'),
        max_length=30
    )
    description = models.TextField(
        _('description'),
        blank=True
    )
    type = models.CharField(
        choices=c.OFFERING_TYPE_CHOICE,
        default=c.PRODUCT,
        max_length=1
    )
    owner_profile = models.ForeignKey(
        MerchantProfile,
        on_delete=models.CASCADE,
        related_name='offerings'
    )
    created = models.DateTimeField(
        _('created'),
        auto_now_add=True
    )


class Visitation(models.Model):
    officer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visiting_officer'
    )
    farmer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='visited_farmer'
    )
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='visited_farm'
    )
    summary = models.TextField(
        _('summary'),
        blank=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )


class TransactionAccount(models.Model):
    number = models.BigIntegerField(
        _('Account number')
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transaction_accounts'
    )
    balance = models.DecimalField(
        _('balance'),
        max_digits=8,
        decimal_places=2,
        default=0
    )


class Card(models.Model):
    ref_number = models.CharField(
        _('reference number'),
        max_length=50
    )
    account = models.ForeignKey(
        TransactionAccount,
        on_delete=models.CASCADE,
        related_name='cards'
    )
    expiry_date = models.DateField(
        _('expiry date'),
        blank=True,
        null=True
    )


class Transaction(models.Model):
    sender = models.ForeignKey(
        TransactionAccount,
        on_delete=models.CASCADE,
        related_name='sender_transactions'
    )
    receiver = models.ForeignKey(
        TransactionAccount,
        on_delete=models.CASCADE,
        related_name='receiver_transactions'
    )
    amount = models.DecimalField(
        _('amount'),
        max_digits=8,
        decimal_places=2
    )
    details = models.TextField(
        _('transaction details'),
        blank=True
    )
