from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Award, Project, ProjectProgress, Stakeholder


class ProjectProgressInline(admin.TabularInline):
    model = ProjectProgress
    extra = 0
    fields = [
        "title",
        "date",
        "progress_percentage",
        "created_by",
        "attachment",
        "image",
    ]
    readonly_fields = ["created_by"]

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class AwardInline(admin.TabularInline):
    model = Award
    extra = 0
    fields = ["name", "organization", "award_date", "certificate", "image"]


@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "stakeholder_type_display",
        "contact_person",
        "contact_email",
        "contact_phone",
        "is_active",
    ]
    list_filter = ["stakeholder_type", "is_active", "created_at"]
    search_fields = ["name", "contact_person", "contact_email"]
    ordering = ["name"]

    fieldsets = (
        ("Temel Bilgiler", {"fields": ("name", "stakeholder_type", "is_active")}),
        (
            "İletişim Bilgileri",
            {
                "fields": (
                    "contact_person",
                    "contact_email",
                    "contact_phone",
                    "address",
                    "website",
                )
            },
        ),
        ("Görsel", {"fields": ("logo",)}),
    )

    def stakeholder_type_display(self, obj):
        type_colors = {
            "department": "#28a745",  # Yeşil
            "company": "#007bff",  # Mavi
            "institution": "#6f42c1",  # Mor
            "ngo": "#fd7e14",  # Turuncu
            "other": "#6c757d",  # Gri
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            type_colors.get(obj.stakeholder_type, "#6c757d"),
            obj.get_stakeholder_type_display(),
        )

    stakeholder_type_display.short_description = "Paydaş Türü"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "status_badge",
        "progress_bar",
        "start_date",
        "planned_end_date",
        "is_featured",
        "is_public",
    ]
    list_filter = [
        "status",
        "category",
        "is_featured",
        "is_public",
        "start_date",
        "stakeholders",
    ]
    search_fields = ["name", "description", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("stakeholders",)
    inlines = [ProjectProgressInline, AwardInline]

    fieldsets = (
        (
            "Temel Bilgiler",
            {"fields": ("name", "slug", "short_description", "description")},
        ),
        (
            "Kategori ve İlişkiler",
            {"fields": ("category", "stakeholders", "project_manager")},
        ),
        ("Durum ve İlerleme", {"fields": ("status", "progress_percentage")}),
        ("Tarihler", {"fields": ("start_date", "planned_end_date", "actual_end_date")}),
        ("Görseller", {"fields": ("featured_image",)}),
        ("Bütçe ve Görünürlük", {"fields": ("budget", "is_featured", "is_public")}),
    )

    def status_badge(self, obj):
        colors = {
            "planning": "#17a2b8",  # Camgöbeği
            "development": "#007bff",  # Mavi
            "testing": "#6f42c1",  # Mor
            "implementation": "#fd7e14",  # Turuncu
            "live": "#28a745",  # Yeşil
            "completed": "#20c997",  # Turkuaz
            "suspended": "#ffc107",  # Sarı
            "cancelled": "#dc3545",  # Kırmızı
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, "#6c757d"),
            obj.get_status_display(),
        )

    status_badge.short_description = "Durum"

    def progress_bar(self, obj):
        # İlerleme çubuğu renkleri
        if obj.progress_percentage < 25:
            color = "#dc3545"  # Kırmızı
        elif obj.progress_percentage < 50:
            color = "#ffc107"  # Sarı
        elif obj.progress_percentage < 75:
            color = "#17a2b8"  # Camgöbeği
        else:
            color = "#28a745"  # Yeşil

        return format_html(
            """
            <div style="width:100%; background-color: #f8f9fa; border-radius: 5px;">
                <div style="width:{}%; background-color: {}; height: 10px; border-radius: 5px;"></div>
            </div>
            <span style="font-weight: bold; color: {};">%{}</span>
            """,
            obj.progress_percentage,
            color,
            color,
            obj.progress_percentage,
        )

    progress_bar.short_description = "İlerleme"

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, "created_by") and not instance.created_by:
                instance.created_by = request.user
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        """Eğer durum tamamlandı ise ve gerçek bitiş tarihi yoksa, bugünün tarihini ata"""
        if obj.status == "completed" and not obj.actual_end_date:
            obj.actual_end_date = timezone.now().date()
        super().save_model(request, obj, form, change)


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "title",
        "progress_percentage",
        "date",
        "created_by",
        "has_attachment",
        "has_image",
    ]
    list_filter = ["project", "date", "created_by"]
    search_fields = ["title", "description", "project__name"]
    date_hierarchy = "date"

    def has_attachment(self, obj):
        return bool(obj.attachment)

    has_attachment.boolean = True
    has_attachment.short_description = "Dosya Eki"

    def has_image(self, obj):
        return bool(obj.image)

    has_image.boolean = True
    has_image.short_description = "Görsel"

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "name",
        "organization",
        "award_date",
        "has_certificate",
        "has_image",
    ]
    list_filter = ["project", "award_date", "organization"]
    search_fields = ["name", "organization", "description", "project__name"]
    date_hierarchy = "award_date"

    def has_certificate(self, obj):
        return bool(obj.certificate)

    has_certificate.boolean = True
    has_certificate.short_description = "Sertifika"

    def has_image(self, obj):
        return bool(obj.image)

    has_image.boolean = True
    has_image.short_description = "Görsel"
