from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ProjectCategory(models.Model):
    """Proje kategorileri"""

    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    icon = models.CharField(
        max_length=50, default="fas fa-folder", verbose_name="Font Awesome İkon"
    )
    color = models.CharField(max_length=20, default="blue", verbose_name="Renk")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    slug = models.SlugField(
        max_length=100, verbose_name="Kategori Kodu", blank=True, null=True
    )

    class Meta:
        verbose_name = "Proje Kategorisi"
        verbose_name_plural = "Proje Kategorileri"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ContactMessage(models.Model):
    """İletişim mesajları"""

    SUBJECT_CHOICES = [
        ("general", "Genel Bilgi"),
        ("suggestion", "Öneri"),
        ("complaint", "Şikayet"),
        ("technical", "Teknik Destek"),
        ("project", "Proje Hakkında"),
        ("cooperation", "İş Birliği"),
        ("other", "Diğer"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Düşük"),
        ("normal", "Normal"),
        ("high", "Yüksek"),
        ("urgent", "Acil"),
    ]

    STATUS_CHOICES = [
        ("new", "Yeni"),
        ("read", "Okundu"),
        ("in_progress", "İşlemde"),
        ("replied", "Yanıtlandı"),
        ("resolved", "Çözüldü"),
        ("closed", "Kapatıldı"),
    ]

    # Kullanıcı bilgileri
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    organization = models.CharField(
        max_length=150, blank=True, verbose_name="Kurum/Şirket"
    )

    # Mesaj bilgileri
    subject = models.CharField(
        max_length=20, choices=SUBJECT_CHOICES, default="general", verbose_name="Konu"
    )
    title = models.CharField(max_length=200, verbose_name="Başlık")
    message = models.TextField(verbose_name="Mesaj")

    # Sistem alanları
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="normal",
        verbose_name="Öncelik",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Durum"
    )

    # Güvenlik ve takip
    ip_address = models.GenericIPAddressField(verbose_name="IP Adresi")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")

    # Zaman damgaları
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    read_at = models.DateTimeField(null=True, blank=True, verbose_name="Okunma Tarihi")

    # Yönetici işlemleri
    read_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="read_messages",
        verbose_name="Okuyan Yönetici",
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_messages",
        verbose_name="Atanan Yönetici",
    )
    admin_notes = models.TextField(blank=True, verbose_name="Yönetici Notları")

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["subject", "-created_at"]),
            models.Index(fields=["priority", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.name}"

    def mark_as_read(self, user):
        """Mesajı okundu olarak işaretle"""
        if self.status == "new":
            self.status = "read"
            self.read_at = timezone.now()
            self.read_by = user
            self.save()

    def get_priority_badge_class(self):
        """Öncelik seviyesine göre CSS class döndür"""
        badge_classes = {
            "low": "bg-gray-100 text-gray-800",
            "normal": "bg-blue-100 text-blue-800",
            "high": "bg-yellow-100 text-yellow-800",
            "urgent": "bg-red-100 text-red-800",
        }
        return badge_classes.get(self.priority, "bg-gray-100 text-gray-800")

    def get_status_badge_class(self):
        """Durum seviyesine göre CSS class döndür"""
        badge_classes = {
            "new": "bg-green-100 text-green-800",
            "read": "bg-blue-100 text-blue-800",
            "in_progress": "bg-yellow-100 text-yellow-800",
            "replied": "bg-purple-100 text-purple-800",
            "resolved": "bg-indigo-100 text-indigo-800",
            "closed": "bg-gray-100 text-gray-800",
        }
        return badge_classes.get(self.status, "bg-gray-100 text-gray-800")


class ProjectSuggestion(models.Model):
    """Kullanıcı proje önerileri"""

    STATUS_CHOICES = [
        ("pending", "Beklemede"),
        ("viewed", "Görüldü"),
        ("under_review", "İnceleme Altında"),
        ("approved", "Onaylandı"),
        ("rejected", "Reddedildi"),
        ("archived", "Arşivlendi"),
    ]

    # Kullanıcı bilgileri
    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")

    # Proje bilgileri
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.CASCADE, verbose_name="Kategori"
    )
    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    description = models.TextField(verbose_name="Proje Açıklaması")
    expected_benefit = models.TextField(verbose_name="Beklenen Fayda")
    estimated_cost = models.CharField(
        max_length=100, blank=True, verbose_name="Tahmini Maliyet"
    )

    # Durum takibi
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Durum"
    )
    viewed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Görülme Tarihi"
    )
    viewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="viewed_suggestions",
        verbose_name="Görüleyen",
    )

    # Arşivleme
    archived_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Arşivlenme Tarihi"
    )
    archived_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="archived_suggestions",
        verbose_name="Arşivleyen",
    )
    archive_reason = models.TextField(blank=True, verbose_name="Arşivleme Sebebi")

    # Güvenlik
    ip_address = models.GenericIPAddressField(verbose_name="IP Adresi")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Proje Önerisi"
        verbose_name_plural = "Proje Önerileri"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.name}"

    def mark_as_viewed(self, user):
        """Öneriyi görüldü olarak işaretle"""
        if self.status == "pending":
            self.status = "viewed"
            self.viewed_at = timezone.now()
            self.viewed_by = user
            self.save()

    def archive(self, user, reason):
        """Öneriyi arşivle"""
        self.status = "archived"
        self.archived_at = timezone.now()
        self.archived_by = user
        self.archive_reason = reason
        self.save()


class SuggestionRateLimit(models.Model):
    """Öneri gönderme hız sınırlama"""

    ip_address = models.GenericIPAddressField(verbose_name="IP Adresi")
    email = models.EmailField(verbose_name="E-posta")
    last_submission = models.DateTimeField(auto_now=True, verbose_name="Son Gönderim")
    submission_count = models.PositiveIntegerField(
        default=1, verbose_name="Gönderim Sayısı"
    )

    class Meta:
        verbose_name = "Hız Sınırlama"
        verbose_name_plural = "Hız Sınırlamaları"
        unique_together = ["ip_address", "email"]


class PersonelStaff(models.Model):
    """Personel/Çalışan bilgileri"""

    DEPARTMENT_CHOICES = [
        ("akilli_sehir", "Akıllı Şehir Müdürlüğü"),
        ("cbs", "CBS (Coğrafi Bilgi Sistemi)"),
        ("it_support", "IT Destek"),
        ("project_management", "Proje Yönetimi"),
        ("data_analysis", "Veri Analizi"),
        ("network", "Ağ Yönetimi"),
        ("software_dev", "Yazılım Geliştirme"),
        ("quality_assurance", "Kalite Güvence"),
        ("coordination", "Koordinasyon"),
        ("other", "Diğer"),
    ]

    POSITION_CHOICES = [
        ("director", "Müdür"),
        ("deputy_director", "Müdür Yardımcısı"),
        ("chief", "Şef"),
        ("senior_specialist", "Kıdemli Uzman"),
        ("specialist", "Uzman"),
        ("engineer", "Mühendis"),
        ("senior_developer", "Kıdemli Geliştirici"),
        ("developer", "Yazılım Geliştirici"),
        ("analyst", "Sistem Analisti"),
        ("technician", "Teknisyen"),
        ("coordinator", "Koordinatör"),
        ("assistant", "Asistan"),
        ("secretary", "Kalem"),
        ("intern", "Stajyer"),
    ]

    STATUS_CHOICES = [
        ("active", "Aktif"),
        ("inactive", "Pasif"),
        ("on_leave", "İzinli"),
        ("transferred", "Nakil"),
        ("retired", "Emekli"),
    ]

    # Kişisel bilgiler
    first_name = models.CharField(max_length=50, verbose_name="Ad")
    last_name = models.CharField(max_length=50, verbose_name="Soyad")
    email = models.EmailField(unique=True, verbose_name="E-posta")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    mobile = models.CharField(max_length=20, blank=True, verbose_name="Cep Telefonu")

    # Görev bilgileri
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES,
        default="akilli_sehir",
        verbose_name="Departman",
    )
    position = models.CharField(
        max_length=50, choices=POSITION_CHOICES, verbose_name="Pozisyon"
    )
    employee_id = models.CharField(
        max_length=20, unique=True, verbose_name="Personel No"
    )

    # İletişim ve ofis bilgileri
    office_location = models.CharField(
        max_length=100, blank=True, verbose_name="Ofis Konumu"
    )
    office_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Ofis Telefonu"
    )
    extension = models.CharField(max_length=10, blank=True, verbose_name="Dahili")

    # Profil bilgileri
    profile_image = models.ImageField(
        upload_to="staff/profiles/",
        blank=True,
        null=True,
        verbose_name="Profil Fotoğrafı",
    )
    bio = models.TextField(blank=True, verbose_name="Kısa Biyografi")
    specialties = models.TextField(
        blank=True,
        verbose_name="Uzmanlık Alanları",
        help_text="Virgülle ayırarak yazın (örn: Python, Django, PostgreSQL)",
    )
    education = models.TextField(blank=True, verbose_name="Eğitim Bilgileri")

    # Sosyal medya ve profesyonel profiller
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn Profili")
    github_url = models.URLField(blank=True, verbose_name="GitHub Profili")
    website_url = models.URLField(blank=True, verbose_name="Kişisel Website")

    # Durum ve tarihler
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Durum",
    )
    hire_date = models.DateField(verbose_name="İşe Başlama Tarihi")
    is_public = models.BooleanField(
        default=True,
        verbose_name="Halka Açık",
        help_text="Bu personelin bilgileri web sitesinde gösterilsin mi?",
    )

    # Yetkilendirme
    is_manager = models.BooleanField(
        default=False,
        verbose_name="Yönetici",
        help_text="Bu personel bir takım/departman yöneticisi mi?",
    )
    can_approve_projects = models.BooleanField(
        default=False, verbose_name="Proje Onay Yetkisi"
    )

    # Meta bilgiler
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_staff",
        verbose_name="Kaydeden",
    )

    class Meta:
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        ordering = ["department", "position", "last_name", "first_name"]
        indexes = [
            models.Index(fields=["department", "status"]),
            models.Index(fields=["position", "status"]),
            models.Index(fields=["employee_id"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_position_display()}"

    @property
    def full_name(self):
        """Tam ad döndür"""
        return f"{self.first_name} {self.last_name}"

    @property
    def display_name(self):
        """Görüntülenecek ad (pozisyonla birlikte)"""
        return f"{self.full_name} ({self.get_position_display()})"

    def get_department_badge_class(self):
        """Departman badge CSS class'ı"""
        badge_classes = {
            "akilli_sehir": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
            "bilgi_islem": "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
            "cbs": "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300",
            "it_support": "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300",
            "project_management": "bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300",
            "data_analysis": "bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-300",
            "network": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
            "software_dev": "bg-cyan-100 text-cyan-800 dark:bg-cyan-900 dark:text-cyan-300",
            "quality_assurance": "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
            "coordination": "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
            "other": "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
        }
        return badge_classes.get(self.department, "bg-gray-100 text-gray-800")

    def get_status_badge_class(self):
        """Durum badge CSS class'ı"""
        badge_classes = {
            "active": "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
            "inactive": "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300",
            "on_leave": "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
            "transferred": "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300",
            "retired": "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300",
        }
        return badge_classes.get(self.status, "bg-gray-100 text-gray-800")

    def get_specialties_list(self):
        """Uzmanlık alanlarını liste olarak döndür"""
        if self.specialties:
            return [
                skill.strip() for skill in self.specialties.split(",") if skill.strip()
            ]
        return []

    def get_contact_info(self):
        """İletişim bilgilerini yapılandırılmış şekilde döndür"""
        contact = {
            "email": self.email,
            "phone": self.phone,
            "mobile": self.mobile,
            "office_phone": self.office_phone,
            "extension": self.extension,
            "office_location": self.office_location,
        }
        return {k: v for k, v in contact.items() if v}  # Boş olmayan alanları döndür

    def has_profile_image(self):
        """Profil fotoğrafı var mı?"""
        return bool(self.profile_image)

    def get_years_of_service(self):
        """Hizmet yılı hesapla"""
        from datetime import date

        today = date.today()
        service_years = today.year - self.hire_date.year
        if today.month < self.hire_date.month or (
            today.month == self.hire_date.month and today.day < self.hire_date.day
        ):
            service_years -= 1
        return max(0, service_years)
