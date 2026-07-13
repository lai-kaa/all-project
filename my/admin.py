from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """后台订单管理"""

    list_display = ('id', 'user', 'train', 'seat', 'price', 'created_at')
    list_filter = ('created_at', 'seat__type')
    search_fields = ('user__username', 'train__number')
    readonly_fields = ('created_at',)
