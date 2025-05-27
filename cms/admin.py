from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import ContactMessage, PersonelStaff, ProjectCategory, ProjectSuggestion


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "color", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "name",
        "subject",
        "status_badge",
        "priority_badge",
        "created_at",
    ]
    list_filter = ["status", "priority", "subject", "created_at"]
    search_fields = ["name", "email", "title", "message"]
    readonly_fields = [
        "ip_address",
        "user_agent",
        "created_at",
        "updated_at",
        "read_at",
    ]

    fieldsets = (
        (
            "Kullanıcı Bilgileri",
            {"fields": ("name", "email", "phone", "organization")},
        ),
        (
            "Mesaj Bilgileri",
            {"fields": ("subject", "title", "message")},
        ),
        (
            "Durum",
            {"fields": ("status", "priority", "assigned_to", "admin_notes")},
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": (
                    "ip_address",
                    "user_agent",
                    "created_at",
                    "updated_at",
                    "read_at",
                    "read_by",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    def status_badge(self, obj):
        badge_class = obj.get_status_badge_class()
        return format_html(
            '<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {}">{}</span>',
            badge_class,
            obj.get_status_display(),
        )

    status_badge.short_description = "Durum"

    def priority_badge(self, obj):
        badge_class = obj.get_priority_badge_class()
        return format_html(
            '<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {}">{}</span>',
            badge_class,
            obj.get_priority_display(),
        )

    priority_badge.short_description = "Öncelik"

    def save_model(self, request, obj, form, change):
        if change and obj.status == "read" and not obj.read_at:
            obj.read_at = timezone.now()
            obj.read_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProjectSuggestion)
class ProjectSuggestionAdmin(admin.ModelAdmin):
    list_display = ["title", "name", "category", "status", "created_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["name", "email", "title", "description"]
    readonly_fields = [
        "ip_address",
        "created_at",
        "updated_at",
        "viewed_at",
        "viewed_by",
    ]

    fieldsets = (
        (
            "Kullanıcı Bilgileri",
            {"fields": ("name", "email", "phone")},
        ),
        (
            "Proje Bilgileri",
            {
                "fields": (
                    "category",
                    "title",
                    "description",
                    "expected_benefit",
                    "estimated_cost",
                )
            },
        ),
        (
            "Durum",
            {"fields": ("status", "viewed_at", "viewed_by")},
        ),
        (
            "Arşiv",
            {
                "fields": ("archived_at", "archived_by", "archive_reason"),
                "classes": ("collapse",),
            },
        ),
        (
            "Sistem",
            {
                "fields": ("ip_address", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if change and obj.status == "viewed" and not obj.viewed_at:
            obj.viewed_at = timezone.now()
            obj.viewed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PersonelStaff)
class PersonelStaffAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "position",
        "department_badge",
        "status_badge",
        "email",
        "is_public",
        "hire_date",
    ]
    list_filter = ["department", "position", "status", "is_public", "is_manager"]
    search_fields = ["first_name", "last_name", "email", "employee_id", "specialties"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (
            "Kişisel Bilgiler",
            {"fields": ("first_name", "last_name", "email", "phone", "mobile")},
        ),
        (
            "Görev Bilgileri",
            {
                "fields": (
                    "department",
                    "position",
                    "employee_id",
                    "office_location",
                    "office_phone",
                    "extension",
                )
            },
        ),
        (
            "Profil Bilgileri",
            {"fields": ("profile_image", "bio", "specialties", "education")},
        ),
        (
            "Sosyal Medya",
            {"fields": ("linkedin_url", "github_url", "website_url")},
        ),
        (
            "Durum ve Yetkilendirme",
            {
                "fields": (
                    "status",
                    "hire_date",
                    "is_public",
                    "is_manager",
                    "can_approve_projects",
                )
            },
        ),
        (
            "Sistem Bilgileri",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def department_badge(self, obj):
        badge_class = obj.get_department_badge_class()
        return format_html(
            '<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {}">{}</span>',
            badge_class,
            obj.get_department_display(),
        )

    department_badge.short_description = "Departman"

    def status_badge(self, obj):
        badge_class = obj.get_status_badge_class()
        return format_html(
            '<span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full {}">{}</span>',
            badge_class,
            obj.get_status_display(),
        )

    status_badge.short_description = "Durum"

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
