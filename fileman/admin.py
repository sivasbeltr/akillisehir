from django import forms
from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from mptt.admin import DraggableMPTTAdmin

from .models import Dosya, DosyaKategori, DosyaTip


class DosyaTipForm(forms.ModelForm):
    class Meta:
        model = DosyaTip
        fields = "__all__"
        widgets = {
            "color": forms.ColorInput(attrs={"type": "color"}),
        }


class DosyaKategoriForm(forms.ModelForm):
    class Meta:
        model = DosyaKategori
        fields = "__all__"
        widgets = {
            "color": forms.ColorInput(attrs={"type": "color"}),
        }


@admin.register(DosyaTip)
class DosyaTipAdmin(admin.ModelAdmin):
    form = DosyaTipForm
    list_display = ("name", "icon", "color", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)
    ordering = ("name",)


@admin.register(DosyaKategori)
class DosyaKategoriAdmin(DjangoMpttAdmin):
    form = DosyaKategoriForm
    list_display = ("name", "icon", "color", "parent", "created_at")
    search_fields = ("name", "description")
    list_filter = ("parent", "created_at")
    ordering = ("name",)
    mptt_level_indent = 20
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Dosya)
class DosyaAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "file_type", "description", "created_at")
    search_fields = ("name", "description", "file")
    list_filter = ("category", "file_type", "created_at")
    ordering = ("-created_at",)
    autocomplete_fields = ("category", "file_type")
