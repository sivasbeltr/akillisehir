from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView
from weasyprint import HTML

from cms.models import ProjectCategory

from .models import Project


class ProjectListView(ListView):
    """Proje listesi görünümü"""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = 12

    def get_queryset(self):
        queryset = (
            Project.objects.filter(is_public=True)
            .select_related("category")
            .prefetch_related("stakeholders", "awards")
        )

        # Kategori filtresi
        category_slug = self.request.GET.get("category")
        if category_slug:
            queryset = queryset.filter(category__name__icontains=category_slug)

        # Durum filtresi
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        # Arama
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search)
                | models.Q(description__icontains=search)
                | models.Q(short_description__icontains=search)
            )

        # Sıralama
        ordering = self.request.GET.get("ordering", "-is_featured")
        if ordering in ["-created_at", "name", "-progress_percentage", "start_date"]:
            queryset = queryset.order_by(ordering, "-is_featured")
        else:
            queryset = queryset.order_by("-is_featured", "-created_at")

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Projelerimiz - Sivas Akıllı Şehir"
        context["page_description"] = (
            "Sivas Belediyesi Akıllı Şehir Müdürlüğü tarafından yürütülen projeler"
        )
        context["categories"] = ProjectCategory.objects.filter(is_active=True)
        context["status_choices"] = Project.STATUS_CHOICES
        context["current_category"] = self.request.GET.get("category", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["current_search"] = self.request.GET.get("search", "")
        context["current_ordering"] = self.request.GET.get("ordering", "-is_featured")

        # İstatistikler
        context["total_projects"] = Project.objects.filter(is_public=True).count()
        context["active_projects"] = Project.objects.filter(
            is_public=True, status__in=["development", "testing", "implementation"]
        ).count()
        context["completed_projects"] = Project.objects.filter(
            is_public=True, status="completed"
        ).count()

        return context


class ProjectDetailView(DetailView):
    """Proje detay görünümü"""

    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return (
            Project.objects.filter(is_public=True)
            .select_related("category", "project_manager")
            .prefetch_related("stakeholders", "progress_records", "awards")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        context["page_title"] = f"{project.name} - Proje Detayı"
        context["page_description"] = project.short_description

        # İlerleme kayıtları (son 10 tanesi)
        context["recent_progress"] = project.progress_records.all()[:10]

        # Benzer projeler (aynı kategoriden, mevcut proje hariç)
        context["related_projects"] = Project.objects.filter(
            category=project.category, is_public=True
        ).exclude(id=project.id)[:4]

        return context


@user_passes_test(lambda u: u.is_staff)
def project_print_view(request, slug):
    """Proje yazdırma görünümü (sadece admin kullanıcılar için)"""
    project = get_object_or_404(Project, slug=slug)

    # PDF için mi, HTML preview için mi?
    format_type = request.GET.get("format", "html")

    context = {
        "project": project,
        "progress_records": project.progress_records.all(),
        "awards": project.awards.all(),
    }

    if format_type == "pdf":
        # PDF oluştur
        html_string = render_to_string("projects/project_print.html", context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="{project.slug}-detay.pdf"'
        )
        return response
    else:
        # HTML preview
        return render(request, "projects/project_print.html", context)
