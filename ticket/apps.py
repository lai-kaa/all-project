from django.apps import AppConfig


class TicketConfig(AppConfig):
    """车次与票务应用"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticket'
    verbose_name = '铁路票务'
