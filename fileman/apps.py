from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FilemanConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fileman"
    verbose_name = _("Dosya Yönetimi")
