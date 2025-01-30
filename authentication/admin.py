from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'mobile_number', 'is_verified', 'created_at')
    search_fields = ('name', 'mobile_number')
    list_filter = ('is_verified', 'gender', 'created_at')
