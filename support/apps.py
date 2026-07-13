from django.apps import AppConfig


class SupportConfig(AppConfig):
    """智能客服：疑难解答 + DeepSeek V4"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'support'
    verbose_name = '智能客服'
