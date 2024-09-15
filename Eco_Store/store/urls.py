from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('product/list/', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/delete/<slug:slug>/', views.delete_product, name='delete_product'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),

    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
