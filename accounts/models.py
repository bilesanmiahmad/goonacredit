import datetime
from django.db import models
from django.contrib.auth.models import (
    PermissionsMixin, AbstractBaseUser, UserManager)
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


from accounts import constants as c

# Create your models here.


class Farmer(models.Model):
    family_name = models.CharField(
        _('family name'),
        max_length=20,
        blank=True
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True
    )
    other_name = models.CharField(
        _('other name'),
        max_length=30,
        blank=True
    )
    dob = models.DateField(
        _('date of birth'),
        blank=True,
        null=True
    )
    address = models.TextField(
        _('address'),
        blank=True
    )
    phone = models.TextField(
        _('phone number'),
        blank=True
    )
    family_size = models.SmallIntegerField(
        _('family size'),
        blank=True
    )
    farm_location = models.TextField(
        _('farm location description'),
        blank=True
    )
    farm_size = models.IntegerField(
        _('farm size'),
        default=0
    )
    credit_rating = models.SmallIntegerField(
        _('credit rating'),

    )
    photo = models.ImageField(
        _('photo'),
        upload_to='farmers/photos',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True
    )
    last_updated = models.DateTimeField(
        _('last updated'),
        auto_now=True
    )


class NewManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        """
        Creates and saves a User with the given
        username, email and password.
        """
        if not phone_number:
            raise ValueError('The phone must be set')

        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        Token.objects.get_or_create(user=user)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        _('email address'),
        blank=True,
        null=True
    )
    id_number = models.CharField(
        _('identity number'),
        max_length=10
    )
    country_code = models.CharField(
        _('country code'),
        max_length=4,
        default='233'
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=30,
        blank=True,
        unique=True
    )
    gender = models.CharField(
        _('gender'),
        max_length=10,
        blank=True
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        blank=True,
        null=True
    )
    user_type = models.CharField(
        _('user type'),
        max_length=1,
        choices=c.USER_TYPE_CHOICES,
        default=c.GOON
    )

    is_verified = models.BooleanField(
        default=False
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    last_login = models.DateTimeField(
        _('last login'),
        auto_now=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        auto_now_add=True
    )
    verification_pin = models.IntegerField(
        blank=True,
        null=True
    )
    verification_tries = models.PositiveSmallIntegerField(
        default=0
    )

    objects = NewManager()

    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __repr__(self):
        return '{}-{}'.format(
            self.__class__, self.id
        )

    def __unicode__(self):
        return self.phone_number

    def __str__(self):
        return self.phone_number

    @property
    def date_joined_str(self):
        return self.date_joined.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    @property
    def last_login_str(self):
        return self.last_login.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    @property
    def avatar_url(self):
        return ''

    @property
    def age(self):
        this_year = datetime.datetime.today().year
        this_month = datetime.datetime.today().month
        this_day = datetime.datetime.today().day
        yob = self.date_of_birth.year
        mob = self.date_of_birth.month
        dob = self.date_of_birth.day

        if this_month < mob:
            return this_year - yob - 1
        elif this_month == mob and this_day < dob:
            return this_year - yob - 1

        return this_year - yob

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_full_name(self):
        """
        Returns the full name for the user.
        """
        return '{0} {1}'.format(
            self.first_name, self.last_name
        ).strip()

    def email_user(
            self, subject, email_template_name, context,
            html_email_template_name=None, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        # send_mail(
        #     subject, email_template_name, context, [self.email],
        #     html_email_template_name, from_email, **kwargs)


class MerchantProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    product = models.CharField(
        max_length=50,
        blank=True,
        help_text="Product or Service provided"
    )
    description = models.TextField(
        blank=True,
        help_text="Description of product or service"
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )


class ExtensionProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=30,
        blank=True
    )
    description = models.TextField(
        blank=True,
        help_text="Description of extension role"
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True
    )
