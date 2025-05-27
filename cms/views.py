from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from .forms import (
    ContactMessageForm,
    ProjectSuggestionForm,
    check_rate_limit,
    update_rate_limit,
)
from .models import PersonelStaff, ProjectCategory, ProjectSuggestion


class IndexView(TemplateView):
    template_name = "cms/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sivas Belediyesi Akıllı Şehir Müdürlüğü"
        context["page_description"] = (
            "Sivas'ı geleceğin akıllı şehri haline getiriyoruz"
        )
        return context


@method_decorator(csrf_protect, name="dispatch")
class ContactView(TemplateView):
    template_name = "cms/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "İletişim - Sivas Akıllı Şehir"
        context["page_description"] = (
            "Sivas Belediyesi Akıllı Şehir Müdürlüğü ile iletişime geçin"
        )
        context["form"] = ContactMessageForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            # IP adresini al
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")

            # Mesajı kaydet
            contact_message = form.save(commit=False)
            contact_message.ip_address = ip_address
            contact_message.user_agent = user_agent
            contact_message.save()

            messages.success(
                request,
                "Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapılacaktır.",
            )
            return redirect("cms:contact_success")

        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)

    def get_client_ip(self, request):
        """Kullanıcının IP adresini al"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class ContactSuccessView(TemplateView):
    template_name = "cms/contact_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Mesaj Gönderildi - Sivas Akıllı Şehir"
        context["page_description"] = "İletişim mesajınız başarıyla alındı"
        return context


@method_decorator(csrf_protect, name="dispatch")
class ProjectSuggestionView(TemplateView):
    template_name = "cms/project_suggestion.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Proje Önerisi Gönder - Sivas Akıllı Şehir"
        context["page_description"] = (
            "Sivas'ın geleceğine katkıda bulunun, proje önerinizi paylaşın"
        )
        context["form"] = ProjectSuggestionForm()
        context["categories"] = ProjectCategory.objects.filter(is_active=True)
        return context

    def post(self, request, *args, **kwargs):
        form = ProjectSuggestionForm(request.POST)

        if form.is_valid():
            # IP adresini al
            ip_address = self.get_client_ip(request)
            email = form.cleaned_data["email"]

            # Hız sınırlama kontrolü
            can_submit, error_message = check_rate_limit(ip_address, email)

            if not can_submit:
                messages.error(request, error_message)
                return self.render_to_response(self.get_context_data(form=form))

            # Öneriyi kaydet
            suggestion = form.save(commit=False)
            suggestion.ip_address = ip_address
            suggestion.save()

            # Hız sınırlama sayacını güncelle
            update_rate_limit(ip_address, email)

            messages.success(
                request,
                "Proje öneriniz başarıyla gönderildi! En kısa sürede değerlendirilerek size dönüş yapılacaktır.",
            )
            return redirect("cms:project_suggestion_success")

        else:
            context = self.get_context_data()
            context["form"] = form
            return self.render_to_response(context)

    def get_client_ip(self, request):
        """Kullanıcının IP adresini al"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class ProjectSuggestionSuccessView(TemplateView):
    template_name = "cms/project_suggestion_success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Proje Önerisi Gönderildi - Sivas Akıllı Şehir"
        context["page_description"] = "Proje öneriniz başarıyla alındı"
        return context


class StaffView(TemplateView):
    """Personel listesi ve detayları"""

    template_name = "cms/staff.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Ekibimiz - Sivas Akıllı Şehir"
        context["page_description"] = (
            "Sivas Belediyesi Akıllı Şehir Müdürlüğü çalışanları"
        )

        # Sadece halka açık ve aktif personelleri göster
        staff_members = (
            PersonelStaff.objects.filter(is_public=True, status="active")
            .select_related("created_by")
            .order_by("department", "position", "last_name")
        )

        # Departmanlara göre grupla
        departments = {}
        for staff in staff_members:
            dept_key = staff.department
            dept_name = staff.get_department_display()

            if dept_key not in departments:
                departments[dept_key] = {"name": dept_name, "members": [], "count": 0}

            departments[dept_key]["members"].append(staff)
            departments[dept_key]["count"] += 1

        context["departments"] = departments
        context["total_staff"] = staff_members.count()

        # Departman istatistikleri
        dept_stats = []
        for dept_key, dept_data in departments.items():
            dept_stats.append(
                {
                    "name": dept_data["name"],
                    "count": dept_data["count"],
                    "key": dept_key,
                }
            )

        context["department_stats"] = sorted(
            dept_stats, key=lambda x: x["count"], reverse=True
        )

        return context


def staff_detail_ajax(request, staff_id):
    """AJAX ile personel detayları"""
    try:
        staff = PersonelStaff.objects.get(id=staff_id, is_public=True, status="active")

        data = {
            "success": True,
            "staff": {
                "id": staff.id,
                "full_name": staff.full_name,
                "position": staff.get_position_display(),
                "department": staff.get_department_display(),
                "email": staff.email,
                "phone": staff.phone,
                "mobile": staff.mobile,
                "office_location": staff.office_location,
                "office_phone": staff.office_phone,
                "extension": staff.extension,
                "bio": staff.bio,
                "education": staff.education,
                "specialties": staff.get_specialties_list(),
                "linkedin_url": staff.linkedin_url,
                "github_url": staff.github_url,
                "website_url": staff.website_url,
                "hire_date": (
                    staff.hire_date.strftime("%d.%m.%Y") if staff.hire_date else ""
                ),
                "years_of_service": staff.get_years_of_service(),
                "profile_image": (
                    staff.profile_image.url if staff.has_profile_image() else ""
                ),
                "is_manager": staff.is_manager,
                "contact_info": staff.get_contact_info(),
                "department_badge_class": staff.get_department_badge_class(),
                "status_badge_class": staff.get_status_badge_class(),
            },
        }

        return JsonResponse(data)

    except PersonelStaff.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Personel bulunamadı."}, status=404
        )
