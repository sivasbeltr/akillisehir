import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class DosyaTip(models.Model):
    """Dosya tipleri"""

    name = models.CharField(max_length=50, verbose_name="Dosya Tipi Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    icon = models.CharField(
        max_length=50, default="fas fa-file", verbose_name="Font Awesome İkon"
    )
    color = models.CharField(
        max_length=20,
        default="#138D19",
        verbose_name="Renk",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )

    class Meta:
        verbose_name = "Dosya Tipi"
        verbose_name_plural = "Dosya Tipleri"
        ordering = ["name"]

    def __str__(self):
        return self.name


class DosyaKategori(MPTTModel):
    """Dosya kategorileri"""

    # her kategori otomatik bir uuid alsın ve primary key olmasın
    uuid = models.UUIDField(
        primary_key=False,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name="Kategori UUID",
    )
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    icon = models.CharField(
        max_length=50, default="fas fa-folder", verbose_name="Font Awesome İkon"
    )
    color = models.CharField(
        max_length=20,
        default="#138D19",
        verbose_name="Renk",
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Üst Kategori",
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Kategori Slug",
        help_text="Kategori URL'si için benzersiz bir slug oluşturun.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = "Dosya Kategorisi"
        verbose_name_plural = "Dosya Kategorileri"
        ordering = ["name"]

    def __str__(self):
        return self.name


def dosya_upload_path(instance, filename):
    # Dosya kategorisinin slug'ını kullanarak dizin oluştur
    slug = instance.category.slug if instance.category else "kategorisiz"
    return f"{slug}/{filename}"


# dosya adı olarak orijinal dosya adını kullan ama min.io dosya ad uzunluğu geçmesin
class Dosya(models.Model):
    """Dosyalar"""

    name = models.CharField(max_length=255, verbose_name="Dosya Adı")
    file = models.FileField(upload_to=dosya_upload_path, verbose_name="Dosya")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    category = models.ForeignKey(
        DosyaKategori,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Kategori",
    )
    file_type = models.ForeignKey(
        DosyaTip,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Dosya Tipi",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )

    class Meta:
        verbose_name = "Dosya"
        verbose_name_plural = "Dosyalar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
