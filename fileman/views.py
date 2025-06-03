from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from .models import Dosya, DosyaKategori, DosyaTip


def file_list(request):
    """Ana dosya listesi sayfası"""
    # Tüm kategorileri ve dosya tiplerini al
    categories = DosyaKategori.objects.all()
    file_types = DosyaTip.objects.all()

    # Filtreleme parametreleri
    category_id = request.GET.get("category")
    file_type_id = request.GET.get("file_type")
    search_query = request.GET.get("search", "").strip()

    # Dosyaları filtrele
    files = Dosya.objects.select_related("category", "file_type").all()

    if category_id:
        try:
            category = DosyaKategori.objects.get(id=category_id)
            # Alt kategorileri de dahil et (MPTT)
            files = files.filter(
                category__in=category.get_descendants(include_self=True)
            )
        except DosyaKategori.DoesNotExist:
            pass

    if file_type_id:
        files = files.filter(file_type_id=file_type_id)

    if search_query:
        files = files.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Sayfalama
    paginator = Paginator(files, 12)  # Her sayfada 12 dosya
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Seçili kategori
    selected_category = None
    if category_id:
        try:
            selected_category = DosyaKategori.objects.get(id=category_id)
        except DosyaKategori.DoesNotExist:
            pass

    # Seçili dosya tipi
    selected_file_type = None
    if file_type_id:
        try:
            selected_file_type = DosyaTip.objects.get(id=file_type_id)
        except DosyaTip.DoesNotExist:
            pass

    context = {
        "page_title": "Dosya Yönetimi",
        "page_description": "Sivas Belediyesi Akıllı Şehir Müdürlüğü dosya arşivi",
        "categories": categories,
        "file_types": file_types,
        "files": page_obj,
        "selected_category": selected_category,
        "selected_file_type": selected_file_type,
        "search_query": search_query,
        "total_files": files.count(),
    }

    return render(request, "fileman/file_list.html", context)
