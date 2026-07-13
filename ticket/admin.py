from django.contrib import admin
from .models import Train, Seat


class SeatInline(admin.TabularInline):
    """在车次编辑页内联维护座位信息"""

    model = Seat
    extra = 3


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('number', 'train_type', 'qi', 'mudi', 'start_time', 'end_time')
    search_fields = ('number', 'qi', 'mudi')
    list_filter = ('train_type',)
    inlines = [SeatInline]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('train', 'type', 'price', 'number')
    list_filter = ('type',)
    search_fields = ('train__number',)
