from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from cms.models import ProjectCategory


class Stakeholder(models.Model):
    """Proje paydaşları (Birimler ve Firmalar)"""

    STAKEHOLDER_TYPES = [
        ("department", "Belediye Birimi"),
        ("company", "Firma/Şirket"),
        ("institution", "Kurum"),
        ("ngo", "STK"),
        ("other", "Diğer"),
    ]

    name = models.CharField(max_length=200, verbose_name="Paydaş Adı")
    stakeholder_type = models.CharField(
        max_length=20, choices=STAKEHOLDER_TYPES, verbose_name="Paydaş Türü"
    )
    contact_person = models.CharField(
        max_length=100, blank=True, verbose_name="İlgili Kişi"
    )
    contact_email = models.EmailField(blank=True, verbose_name="İletişim E-posta")
    contact_phone = models.CharField(
        max_length=20, blank=True, verbose_name="İletişim Telefon"
    )
    address = models.TextField(blank=True, verbose_name="Adres")
    website = models.URLField(blank=True, verbose_name="Web Sitesi")
    logo = models.ImageField(
        upload_to="stakeholders/logos/", blank=True, null=True, verbose_name="Logo"
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )

    class Meta:
        verbose_name = "Paydaş"
        verbose_name_plural = "Paydaşlar"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_stakeholder_type_display()})"


class Project(models.Model):
    """Akıllı Şehir Projeleri"""

    STATUS_CHOICES = [
        ("planning", "Planlama Aşamasında"),
        ("development", "Geliştirme Aşamasında"),
        ("testing", "Test Aşamasında"),
        ("implementation", "Uygulama Aşamasında"),
        ("live", "Canlıda"),
        ("completed", "Tamamlandı"),
        ("suspended", "Askıya Alındı"),
        ("cancelled", "İptal Edildi"),
    ]

    # Temel bilgiler
    name = models.CharField(max_length=200, verbose_name="Proje Adı")
    slug = models.SlugField(unique=True, verbose_name="URL Kısaltması")
    description = models.TextField(verbose_name="Proje Açıklaması")
    short_description = models.TextField(max_length=500, verbose_name="Kısa Açıklama")

    # Kategoriler ve Paydaşlar
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.PROTECT, verbose_name="Kategori"
    )
    stakeholders = models.ManyToManyField(
        Stakeholder, blank=True, verbose_name="Paydaşlar"
    )
    project_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_projects",
        verbose_name="Proje Yöneticisi",
    )

    # Tarihler
    start_date = models.DateField(
        null=True, blank=True, verbose_name="Başlangıç Tarihi"
    )
    planned_end_date = models.DateField(
        null=True, blank=True, verbose_name="Planlanan Bitiş Tarihi"
    )
    actual_end_date = models.DateField(
        null=True, blank=True, verbose_name="Gerçekleşen Bitiş Tarihi"
    )

    # Durum ve İlerleme
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="planning", verbose_name="Durum"
    )
    progress_percentage = models.PositiveSmallIntegerField(
        default=0, verbose_name="İlerleme Yüzdesi", help_text="0-100 arası değer"
    )

    # Medya ve Dosyalar
    featured_image = models.ImageField(
        upload_to="projects/featured/",
        blank=True,
        null=True,
        verbose_name="Kapak Görseli",
    )

    # Meta veriler
    budget = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Bütçe (TL)",
    )
    is_featured = models.BooleanField(default=False, verbose_name="Öne Çıkan Proje")
    is_public = models.BooleanField(default=True, verbose_name="Halka Açık")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.name

    @property
    def duration_in_days(self):
        """Proje süresini gün olarak hesapla"""
        if not self.start_date:
            return None

        end_date = (
            self.actual_end_date or self.planned_end_date or timezone.now().date()
        )
        return (end_date - self.start_date).days


class ProjectProgress(models.Model):
    """Proje ilerleme kayıtları"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="progress_records",
        verbose_name="Proje",
    )
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(verbose_name="Açıklama")
    progress_percentage = models.PositiveSmallIntegerField(
        verbose_name="İlerleme Yüzdesi", help_text="0-100 arası değer"
    )
    date = models.DateField(verbose_name="Tarih")

    # Dosya ve görseller
    attachment = models.FileField(
        upload_to="projects/progress/attachments/",
        blank=True,
        null=True,
        verbose_name="Dosya Eki",
    )
    image = models.ImageField(
        upload_to="projects/progress/images/",
        blank=True,
        null=True,
        verbose_name="Görsel",
    )

    # Meta veriler
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="progress_records",
        verbose_name="Ekleyen",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "İlerleme Kaydı"
        verbose_name_plural = "İlerleme Kayıtları"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.project.name} - {self.title} (%{self.progress_percentage})"

    def save(self, *args, **kwargs):
        """İlerleme kaydı kaydedildiğinde proje ilerleme durumunu güncelle"""
        super().save(*args, **kwargs)

        # En son ilerleme kaydının yüzdesini projeye ata
        latest_progress = (
            ProjectProgress.objects.filter(project=self.project)
            .order_by("-date", "-created_at")
            .first()
        )

        if latest_progress:
            self.project.progress_percentage = latest_progress.progress_percentage
            self.project.save(update_fields=["progress_percentage"])

    # silinirse proje ilerleme durumunu güncelle
    def delete(self, *args, **kwargs):
        """İlerleme kaydı silindiğinde proje ilerleme durumunu güncelle"""
        super().delete(*args, **kwargs)

        # En son ilerleme kaydını bul ve projeyi güncelle
        latest_progress = (
            ProjectProgress.objects.filter(project=self.project)
            .order_by("-date", "-created_at")
            .first()
        )

        if latest_progress:
            self.project.progress_percentage = latest_progress.progress_percentage
        else:
            self.project.progress_percentage = 0

        self.project.save(update_fields=["progress_percentage"])


class Award(models.Model):
    """Projeler için ödüller"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="awards", verbose_name="Proje"
    )
    name = models.CharField(max_length=200, verbose_name="Ödül Adı")
    organization = models.CharField(max_length=200, verbose_name="Veren Kuruluş")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    award_date = models.DateField(verbose_name="Ödül Tarihi")
    certificate = models.FileField(
        upload_to="projects/awards/",
        blank=True,
        null=True,
        verbose_name="Sertifika/Belge",
    )
    image = models.ImageField(
        upload_to="projects/awards/images/",
        blank=True,
        null=True,
        verbose_name="Ödül Görseli",
    )

    class Meta:
        verbose_name = "Ödül"
        verbose_name_plural = "Ödüller"
        ordering = ["-award_date"]

    def __str__(self):
        return f"{self.project.name} - {self.name} ({self.organization})"
