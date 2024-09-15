from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Category, Profile, Cart, CartItem, Order, CustomUser

# Registering your models
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)

# Admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ("name",)}

# Admin configuration for Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'phone']

# Admin configuration for CustomUser model, inheriting from UserAdmin
class CustomUserAdmin(UserAdmin):  # Inherit from UserAdmin
    fieldsets = UserAdmin.fieldsets + (  # Use UserAdmin.fieldsets, not admin.fieldsets
        (None, {'fields': ('image',)}),  # Add the image field
    )

# Register the CustomUser model with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)
