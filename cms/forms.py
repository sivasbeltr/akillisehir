from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import (
    ContactMessage,
    ProjectCategory,
    ProjectSuggestion,
    SuggestionRateLimit,
)


class ContactMessageForm(forms.ModelForm):
    """İletişim formu"""

    class Meta:
        model = ContactMessage
        fields = [
            "name",
            "email",
            "phone",
            "organization",
            "subject",
            "title",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Ad Soyad *",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "E-posta adresiniz *",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Telefon numaranız",
                }
            ),
            "organization": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Kurum/Şirket adınız",
                }
            ),
            "subject": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Mesaj başlığınız *",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-sivas-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-sivas-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Mesajınızı detaylı olarak yazınız... *",
                    "rows": 6,
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 5:
            raise ValidationError("Mesaj başlığı en az 5 karakter olmalıdır.")
        return title

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 20:
            raise ValidationError("Mesaj içeriği en az 20 karakter olmalıdır.")
        return message


class ProjectSuggestionForm(forms.ModelForm):
    """Proje önerisi formu"""

    class Meta:
        model = ProjectSuggestion
        fields = [
            "name",
            "email",
            "phone",
            "category",
            "title",
            "description",
            "expected_benefit",
            "estimated_cost",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Ad Soyad",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "E-posta adresiniz",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Telefon numaranız (opsiyonel)",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300"
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Proje başlığınız",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Projenizi detaylı olarak açıklayın...",
                    "rows": 5,
                }
            ),
            "expected_benefit": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Bu projenin şehrimize ve vatandaşlara sağlayacağı faydaları açıklayın...",
                    "rows": 4,
                }
            ),
            "estimated_cost": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:border-blue-500 dark:focus:border-cyan-500 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-cyan-500/20 transition-all duration-300",
                    "placeholder": "Tahmini maliyet (opsiyonel)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = ProjectCategory.objects.filter(
            is_active=True
        )
        self.fields["category"].empty_label = "Kategori seçiniz"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            # E-posta domain kontrolü
            allowed_domains = [
                "gmail.com",
                "hotmail.com",
                "outlook.com",
                "yahoo.com",
                "yandex.com",
            ]
            domain = email.split("@")[1].lower()
            if (
                domain not in allowed_domains
                and not domain.endswith(".edu.tr")
                and not domain.endswith(".bel.tr")
                and not domain.endswith(".gov.tr")
            ):
                # Geçerli domain'ler dışında da kabul et, sadece uyarı ver
                pass
        return email

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) < 10:
            raise ValidationError("Proje başlığı en az 10 karakter olmalıdır.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 50:
            raise ValidationError("Proje açıklaması en az 50 karakter olmalıdır.")
        return description


def check_rate_limit(ip_address, email):
    """Hız sınırlama kontrolü"""
    now = timezone.now()

    # IP bazlı kontrol (saatte en fazla 3 öneri)
    ip_limit = SuggestionRateLimit.objects.filter(
        ip_address=ip_address, last_submission__gte=now - timedelta(hours=1)
    ).first()

    if ip_limit and ip_limit.submission_count >= 3:
        return False, "Bu IP adresinden saatte en fazla 3 öneri gönderilebilir."

    # E-posta bazlı kontrol (günde en fazla 5 öneri)
    email_limit = SuggestionRateLimit.objects.filter(
        email=email, last_submission__gte=now - timedelta(days=1)
    ).first()

    if email_limit and email_limit.submission_count >= 5:
        return False, "Bu e-posta adresinden günde en fazla 5 öneri gönderilebilir."

    return True, None


def update_rate_limit(ip_address, email):
    """Hız sınırlama sayacını güncelle"""
    now = timezone.now()

    # IP bazlı güncelleme
    ip_limit, created = SuggestionRateLimit.objects.get_or_create(
        ip_address=ip_address, email=email
    )

    if created or ip_limit.last_submission < now - timedelta(hours=1):
        ip_limit.submission_count = 1
    else:
        ip_limit.submission_count += 1

    ip_limit.save()
