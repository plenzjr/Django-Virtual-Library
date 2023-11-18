from django.contrib import admin
from app_account.models import User


# Register your models here.
@admin.register(User)
class Addresses(admin.ModelAdmin):
    pass
