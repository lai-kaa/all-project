from django.apps import AppConfig


class MyConfig(AppConfig):
    """用户与订单应用"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my'
    verbose_name = '用户订单'
