from django.contrib import admin
from .models import Train, Seat

@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('number', 'train_type', 'qi', 'mudi', 'start_time', 'end_time')
    search_fields = ('number', 'qi', 'mudi')

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('train', 'type', 'price', 'number')
    list_filter = ('type',)