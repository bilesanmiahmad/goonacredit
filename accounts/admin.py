from django.contrib import admin
from accounts import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.FarmerProfile)
admin.site.register(models.ExtensionProfile)
admin.site.register(models.MerchantProfile)
