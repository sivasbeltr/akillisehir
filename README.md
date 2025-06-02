# Sivas Belediyesi Akıllı Şehir Web Portalı

## 🌟 Yazılım Hakkında

Bu proje, **Sivas Belediyesi Akıllı Şehir Müdürlüğü** için geliştirilmiş kapsamlı bir web portalıdır. Modern web teknolojileri kullanılarak Django framework'ü ile Python dilinde yazılmıştır. Sivas'ın dijital dönüşümünde kilit rol oynayan bu platform, vatandaşlar ile belediye arasında etkili bir köprü görevi görmektedir.

### 🎯 Ne İşe Yarar?

Bu web portalı şehrimizin akıllı şehir vizyonunu hayata geçirmek için tasarlanmış çok fonksiyonlu bir platformdur:

**🏛️ Kurumsal İletişim:**
- Sivas Belediyesi Akıllı Şehir Müdürlüğü'nün faaliyetlerini kamuoyuna şeffaf bir şekilde sunma
- Vatandaşların belediye ile doğrudan iletişim kurabilmesi için güvenli kanallar sağlama
- Proje süreçlerinde şeffaflık ve hesap verebilirlik ilkelerini destekleme

**📊 Proje Yönetimi:**
- Akıllı şehir projelerinin detaylı takibi ve görselleştirilmesi
- Proje ilerlemelerinin gerçek zamanlı raporlanması
- Vatandaşların proje süreçlerini anlayabilmesi için detaylı bilgilendirme

**💡 Katılımcı Yönetim:**
- Vatandaşlardan gelen proje önerilerinin sistematik değerlendirilmesi
- Kamusal karar alma süreçlerine vatandaş katılımının artırılması
- Şehrin ihtiyaçlarının yerinden belirlenmesi için geri bildirim mekanizmaları

**📈 Veri Şeffaflığı:**
- Belediye faaliyetlerinin verilerle desteklenmesi
- Performans göstergelerinin kamuoyu ile paylaşılması
- Proje bütçeleri ve harcamalarının takibi

## ✨ Temel Özellikler

### 🎛️ **Gelişmiş Proje Yönetim Sistemi**
- **Kategori Bazlı Organizasyon:** Projeler konularına göre sistematik şekilde gruplandırılır
- **Durum Takibi:** Gerçek zamanlı proje durumu izleme (Planlama, Geliştirme, Test, Tamamlandı)
- **Bütçe Yönetimi:** Proje maliyetleri ve harcama takibi
- **İlerleme Raporlama:** Görsel çizelgeler ve grafik raporlar
- **PDF Dışa Aktarma:** Proje detaylarının profesyonel rapor formatında indirimi
- **Paydaş Yönetimi:** Proje katılımcılarının ve sorumlu birimlerinin takibi

## 🐳 Docker ile Kurulum

### Ön Gereksinimler
- Docker Engine 20.10+
- Docker Compose v2+
- Çalışan PostgreSQL sunucusu (PostGIS extension ile)
- Çalışan MinIO sunucusu

### Hızlı Başlangıç

1. **Projeyi klonlayın:**
```bash
git clone https://github.com/sivasbelediyesi/akillisehir.git
cd akillisehir
```

2. **Environment dosyasını oluşturun:**
```bash
cp .env.example .env
# .env dosyasını düzenleyerek kendi ayarlarınızı yapın
```

3. **Docker container'ını başlatın:**
```bash
# Development için
docker compose up -d

# Production için
docker compose -f compose.yml up -d
```

### Environment Ayarları

`.env` dosyasında aşağıdaki ayarları yapılandırın:

```env
# Django ayarları
SECRET_KEY=your-secret-key-here
DEBUG=False

# Veritabanı ayarları
DATABASE_HOST=your-postgres-host
DATABASE_PORT=5432
DATABASE_NAME=akillisehir
DATABASE_USER=your-db-user
DATABASE_PASSWORD=your-db-password

# MinIO ayarları
MINIO_ENDPOINT=your-minio-endpoint:9000
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
MINIO_BUCKET_NAME=akillisehir
MINIO_CUSTOM_DOMAIN=your-domain.com

# Superuser ayarları (ilk kurulumda)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@sivas.bel.tr
DJANGO_SUPERUSER_PASSWORD=your-admin-password
```

### Docker Hub'dan Çalıştırma

Hazır imajı Docker Hub'dan çekebilirsiniz:

```bash
# Latest versiyonu çek
docker pull sivasbelediyesi/akillisehir:latest

# Çalıştır
docker run -d \
  --name akillisehir-web \
  -p 8000:8000 \
  --env-file .env \
  -v ./logs:/app/logs \
  sivasbelediyesi/akillisehir:latest
```

### Log İzleme

```bash
# Container loglarını izle
docker compose logs -f web

# Access loglarını izle
tail -f logs/access.log

# Error loglarını izle
tail -f logs/error.log
```

### Maintenance Komutları

```bash
# Container içinde komut çalıştır
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py createsuperuser

# Container'ı yeniden başlat
docker compose restart web

# Container'ı durdur ve sil
docker compose down
```

## 🚀 GitHub Actions ile CI/CD

### Docker Hub'a Otomatik Deploy

Bu proje GitHub Actions kullanarak otomatik olarak Docker Hub'a deploy edilir:

1. **GitHub Secrets'ı ayarlayın:**
   - `DOCKER_USERNAME`: Docker Hub kullanıcı adınız
   - `DOCKER_PASSWORD`: Docker Hub erişim token'ınız

2. **Deployment:**
   - `main` branch'e push edildiğinde otomatik build ve push
   - Tag push edildiğinde versiyonlu imaj oluşturma
   - Multi-platform support (linux/amd64, linux/arm64)

3. **Kullanılabilir imaj etiketleri:**
   ```bash
   sivasbelediyesi/akillisehir:latest
   sivasbelediyesi/akillisehir:main
   sivasbelediyesi/akillisehir:v1.0.0
   ```

### Production Deployment

Production ortamında deployment için:

```bash
# Latest versiyonu çek
docker pull sivasbelediyesi/akillisehir:latest

# Mevcut container'ı durdur
docker compose down

# Yeni versiyonu başlat
docker compose up -d

# Deployment'ı doğrula
docker compose ps
docker compose logs web
```

### 📞 **Gelişmiş İletişim Modülü**
- **Akıllı Form Sistemi:** Konu bazlı mesaj kategorilendirme
- **Otomatik Bildirim:** Mesaj durumu güncellemeleri
- **Admin Panel Entegrasyonu:** Mesajların yönetim panelinden takibi
- **Harita Entegrasyonu:** OpenStreetMap ile konum bilgileri
- **Çoklu İletişim Kanalı:** Telefon, e-posta ve form desteği

### 💡 **Proje Öneri Sistemi**
- **Kullanıcı Dostu Arayüz:** Sezgisel form tasarımı
- **Kategori Filtreleme:** Öneri türlerine göre sistemli organizasyon
- **Değerlendirme Süreci:** Admin panelinde öneri inceleme ve geri bildirim sistemi
- **Durum Takibi:** Önerinin hangi aşamada olduğunun şeffaf takibi

### 🎨 **Modern Kullanıcı Deneyimi**
- **Responsive Tasarım:** Tüm cihazlarda mükemmel görünüm
- **Dark/Light Mode:** Kullanıcı tercihine göre tema değişimi
- **Glassmorphism Efektleri:** Modern görsel tasarım öğeleri
- **Smooth Animasyonlar:** Akıcı geçiş efektleri
- **Tailwind CSS:** Hızlı ve tutarlı stil geliştirme

### 🔐 **Güvenlik ve Yönetim**
- **Django Admin Panel:** Gelişmiş içerik yönetim sistemi
- **IP Takibi:** Güvenlik amaçlı kullanıcı takibi
- **Form Validasyonu:** Veri bütünlüğü ve güvenliği
- **Rate Limiting:** Spam koruması
- **Kullanıcı Yetkilendirme:** Rol bazlı erişim kontrolü

## 🚀 Sunucu Kurulumu ve Çalıştırma

### 📋 Sistem Gereksinimleri

**Minimum Gereksinimler:**
- Python 3.8 veya üzeri
- Django 4.2 veya üzeri
- PostgreSQL 12+ (üretim ortamı için önerilen)
- Redis (cache ve session yönetimi için)
- 2GB RAM
- 10GB disk alanı

**Önerilen Gereksinimler:**
- Python 3.11+
- Django 5.0+
- PostgreSQL 15+
- Redis 7+
- 4GB RAM
- 50GB SSD disk

### 🛠️ Kurulum Adımları

#### 1. **Proje Dosyalarını İndirin**
```bash
# Git ile proje klonlama
git clone https://github.com/sivasbeltr/akillisehir.git
cd akillisehir

# Veya ZIP dosyası ile indirme
# İndirilen dosyayı /var/www/ dizinine çıkarın
```

#### 2. **Python Sanal Ortamı Oluşturun**
```bash
# Sanal ortam oluşturma
python3 -m venv venv

# Sanal ortamı aktifleştirme (Linux/Mac)
source venv/bin/activate

# Windows için:
# venv\Scripts\activate
```

#### 3. **Bağımlılıkları Yükleyin**
```bash
# Gerekli paketleri yükleme
pip install -r requirements.txt

# Manuel yükleme gerekirse:
pip install django djangorestframework django-cors-headers djangorestframework-gis django-admin-interface
pip install psycopg2-binary pillow
pip install gunicorn
```

#### 4. **Veritabanı Konfigürasyonu**

**PostgreSQL Kurulumu (Ubuntu/Debian):**
```bash
# PostgreSQL kurulumu
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL kullanıcısına geçiş
sudo -u postgres psql

# Veritabanı ve kullanıcı oluşturma
CREATE DATABASE akillisehir_db;
CREATE USER akillisehir_user WITH PASSWORD 'güçlü_şifre_123';
ALTER ROLE akillisehir_user SET client_encoding TO 'utf8';
ALTER ROLE akillisehir_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE akillisehir_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE akillisehir_db TO akillisehir_user;
\q
```

#### 5. **Ortam Değişkenlerini Ayarlayın**
```bash
# .env dosyası oluşturun
cat > .env << EOF
DEBUG=False
SECRET_KEY=very-secret-key-here-change-this-in-production
DATABASE_URL=postgresql://akillisehir_user:güçlü_şifre_123@localhost:5432/akillisehir_db
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,localhost,127.0.0.1
STATIC_ROOT=/var/www/akillisehir/staticfiles/
MEDIA_ROOT=/var/www/akillisehir/media/
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EOF
```

#### 6. **Django Ayarlarını Yapın**
```bash
# Migrations oluşturma
python manage.py makemigrations

# Veritabanı migration'larını uygulama
python manage.py migrate

# Static dosyaları toplama
python manage.py collectstatic --noinput

# Superuser oluşturma
python manage.py createsuperuser
```

#### 7. **Test Verilerini Yükleyin (Opsiyonel)**
```bash
# Örnek kategoriler ve test verilerini yükleme
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/sample_projects.json
```

### 🔧 Farklı Ortamlarda Çalıştırma

#### **Geliştirme Ortamı**
```bash
# Django development server
python manage.py runserver 0.0.0.0:8000

# Erişim: http://localhost:8000
# Admin Panel: http://localhost:8000/admin
```

#### **Üretim Ortamı (Gunicorn + Nginx)**

**Gunicorn Konfigürasyonu:**
```bash
# Gunicorn ile çalıştırma
gunicorn --bind 0.0.0.0:8000 akillisehir.wsgi:application

# Systemd servis dosyası oluşturun
sudo nano /etc/systemd/system/akillisehir.service
```

**Systemd Servis Dosyası:**
```ini
[Unit]
Description=Sivas Akıllı Şehir Django Application
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/akillisehir
Environment="PATH=/var/www/akillisehir/venv/bin"
ExecStart=/var/www/akillisehir/venv/bin/gunicorn --workers 3 --bind unix:/var/www/akillisehir/akillisehir.sock akillisehir.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

**Nginx Konfigürasyonu:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/akillisehir;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        root /var/www/akillisehir;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/akillisehir/akillisehir.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Servisleri Başlatma:**
```bash
# Servisleri etkinleştirme
sudo systemctl daemon-reload
sudo systemctl start akillisehir
sudo systemctl enable akillisehir
sudo systemctl restart nginx

# Durum kontrolü
sudo systemctl status akillisehir
sudo systemctl status nginx
```

#### **Docker ile Çalıştırma**
```bash
# Docker image build etme
docker build -t sivas-akillisehir .

# Docker container çalıştırma
docker run -d --name akillisehir-app -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/akillisehir \
  sivas-akillisehir

# Docker Compose ile
docker-compose up -d
```

### 🔧 Bakım ve Güncelleme

#### **Düzenli Bakım İşlemleri**
```bash
# Log dosyalarını temizleme
sudo find /var/log -name "*.log" -type f -size +100M -exec truncate -s 0 {} \;

# Database vacuum (PostgreSQL)
python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('VACUUM ANALYZE;')"

# Cache temizleme
python manage.py clear_cache

# Static dosyaları güncelleme
python manage.py collectstatic --noinput
```

#### **Güvenlik Güncellemeleri**
```bash
# Python paketlerini güncelleme
pip list --outdated
pip install --upgrade package_name

# Sistem güncellemeleri (Ubuntu)
sudo apt update && sudo apt upgrade

# SSL sertifikası yenileme (Let's Encrypt)
sudo certbot renew
```

### 📊 Performans Optimizasyonu

#### **Veritabanı Optimizasyonu**
```python
# settings.py'de cache ayarları
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Database connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'MAX_CONNS': 20,
            'OPTIONS': {
                'MAX_CONNS': 20,
            }
        }
    }
}
```

### 🔍 İzleme ve Log Yönetimi

#### **Log Konfigürasyonu**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/akillisehir/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 📱 Kullanım Kılavuzu

### 👨‍💼 **Yönetici Kullanımı**
1. `/admin` paneline giriş yapın
2. Proje kategorilerini oluşturun
3. Yeni projeler ekleyin ve durumlarını güncelleyin
4. Gelen mesajları ve önerileri değerlendirin
5. Kullanıcı geri bildirimlerini takip edin

### 👥 **Vatandaş Kullanımı**
1. Ana sayfadan projeleri inceleyin
2. İletişim formunu kullanarak mesaj gönderin
3. Proje önerilerinizi paylaşın
4. Proje ilerlemelerini takip edin

## 🆘 Destek ve İletişim

**Teknik Destek:**
- E-posta: support@sivasakillisehir.gov.tr
- Telefon: +90 (346) 221 01 10

**Proje Deposu:**
- GitHub: https://github.com/sivasbeltr/akillisehir
- Dokümantasyon: https://docs.sivasakillisehir.gov.tr

---

## 📄 Lisans

Bu proje Sivas Belediyesi tarafından geliştirilmiş olup, MIT lisansı altında yayınlanmıştır.

**© 2024 Sivas Belediyesi Akıllı Şehir Müdürlüğü**
    *   Tailwind CSS kullanılarak geliştirilmiş, estetik, sade ve sezgisel bir tasarım.
    *   Tüm cihazlarla uyumlu (responsive) mobil öncelikli (mobile-first) tasarım.
*   **Tema Desteği:**
    *   Kullanıcı tercihine göre gece (dark) ve gündüz (light) modu seçenekleri.
*   **Harita Entegrasyonu:**
    *   OpenStreetMap (Leaflet.js) kullanılarak müdürlük veya proje konumlarının harita üzerinde gösterilmesi.

## 🛠️ Kullanılan Teknolojiler

*   **Backend:**
    *   Python 3.x
    *   Django Web Framework
    *   Django REST framework (API geliştirmeleri için)
    *   PostgreSQL (PostGIS eklentisi ile coğrafi veri desteği)
*   **Frontend:**
    *   HTML5
    *   Tailwind CSS (CSS Framework)
    *   JavaScript (Dinamik arayüz elemanları ve harita entegrasyonu için)
*   **Veritabanı:**
    *   PostgreSQL (Ana veritabanı)
    *   PostGIS (Coğrafi sorgular ve veri tipleri için PostgreSQL eklentisi)
*   **Diğer Önemli Kütüphaneler/Araçlar:**
    *   `psycopg2-binary`: PostgreSQL adaptörü.
    *   `python-dotenv`: Ortam değişkenlerini `.env` dosyasından yönetmek için.
    *   `django-admin-interface`: Django admin arayüzünü özelleştirmek için.
    *   `weasyprint`: HTML/CSS'den PDF oluşturmak için (Proje raporları).
    *   `Pillow`: Resim işleme kütüphanesi.

## 🚀 Kurulum ve Çalıştırma (Yerel Geliştirme Ortamı)

Projeyi yerel makinenizde kurup çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/kullanici_adiniz/akillisehir.git
    cd akillisehir
    ```

2.  **Sanal Ortam Oluşturun ve Aktif Edin:**
    Python projeleri için sanal ortam kullanmak en iyi pratiktir.
    ```bash
    python -m venv venv
    ```
    *   Windows için:
        ```bash
        venv\Scripts\activate
        ```
    *   Linux/macOS için:
        ```bash
        source venv/bin/activate
        ```

3.  **Gerekli Paketleri Yükleyin:**
    Proje bağımlılıkları `requirements.txt` dosyasında listelenmiştir.
    ```bash
    pip install -r requirements.txt
    ```

4.  **`.env` Dosyasını Yapılandırın:**
    Proje ana dizininde `.env` adında bir dosya oluşturun. Bu dosya, hassas yapılandırma bilgilerini (veritabanı şifreleri, gizli anahtar vb.) içerecektir. Aşağıdaki içeriği örnek olarak kullanabilir ve kendi bilgilerinize göre düzenleyebilirsiniz:
    ```env
    SECRET_KEY='django_tarafindan_uretilen_guclu_bir_secret_key_buraya_gelecek'
    POSTGRES_DB='akillisehir_db'
    POSTGRES_USER='akillisehir_user'
    POSTGRES_PASSWORD='guclu_bir_sifre'
    POSTGRES_HOST='localhost'  # Veya PostgreSQL sunucunuzun adresi
    POSTGRES_PORT='5432'      # Varsayılan PostgreSQL portu
    ```
    **Not:** `SECRET_KEY` Django projeleri için kritik bir güvenlik ayarıdır. Güçlü ve benzersiz bir anahtar kullanın. Django'nun kendisi bu anahtarı üretebilir veya online araçlar kullanabilirsiniz.

5.  **Veritabanı Migration'larını Çalıştırın:**
    Model değişikliklerini veritabanına uygulamak için:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Süper Kullanıcı (Admin) Oluşturun:**
    Yönetim paneline erişmek için bir admin kullanıcısı oluşturun:
    ```bash
    python manage.py createsuperuser
    ```
    Komut sizden kullanıcı adı, e-posta ve şifre isteyecektir.

7.  **Geliştirme Sunucusunu Başlatın:**
    ```bash
    python manage.py runserver
    ```
    Varsayılan olarak, geliştirme sunucusu `http://127.0.0.1:8000/` adresinde çalışacaktır.
    *   Web sitesine `http://127.0.0.1:8000/` adresinden erişebilirsiniz.
    *   Yönetim paneline `http://127.0.0.1:8000/admin/` adresinden erişebilirsiniz.

## ☁️ Sunucuya Kurulum (Deployment)

Projeyi bir üretim sunucusuna kurmak için genel adımlar aşağıdadır. Kullandığınız sunucu ortamına (Linux dağıtımı, bulut sağlayıcısı vb.) göre bazı adımlar farklılık gösterebilir.

1.  **Ön Koşullar:**
    *   Python 3.x ve pip kurulu bir Linux sunucusu.
    *   PostgreSQL ve PostGIS eklentisi kurulu ve yapılandırılmış.
    *   Bir WSGI HTTP sunucusu (örn: Gunicorn, uWSGI).
    *   Bir ters proxy (reverse proxy) ve web sunucusu (örn: Nginx, Apache).
    *   `git` kurulu olmalı.

2.  **Kodu Sunucuya Aktarın:**
    Proje dosyalarını sunucunuza klonlayın veya kopyalayın.
    ```bash
    git clone https://github.com/sivasbeltr/akillisehir.git
    cd akillisehir
    ```

3.  **Sanal Ortam ve Bağımlılıklar:**
    Yerel kurulumdaki gibi sunucuda da bir sanal ortam oluşturun ve `requirements.txt` ile bağımlılıkları yükleyin.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

4.  **`.env` Dosyasını Yapılandırın:**
    Sunucu ortamı için uygun ve güvenli değerlerle `.env` dosyasını oluşturun. Özellikle `SECRET_KEY` üretim ortamı için benzersiz ve çok gizli olmalıdır. Veritabanı bağlantı bilgileri sunucudaki PostgreSQL yapılandırmanıza uygun olmalıdır.

5.  **Django Ayarlarını Üretim İçin Düzenleyin (`akillisehir/settings.py`):**
    *   **`DEBUG = False`**: Üretim ortamında `DEBUG` kesinlikle `False` olmalıdır.
    *   **`ALLOWED_HOSTS`**: Projenizin sunulacağı alan adlarını veya IP adreslerini buraya ekleyin. Örn: `ALLOWED_HOSTS = ['sivasakillisehir.gov.tr', 'www.sivasakillisehir.gov.tr']`
    *   Veritabanı ayarlarının `.env` dosyasından doğru yüklendiğinden emin olun.
    *   Statik dosya ve medya dosyası yollarını (`STATIC_ROOT`, `MEDIA_ROOT`) kontrol edin.

6.  **Veritabanı Kurulumu ve Migration'lar:**
    *   Sunucudaki PostgreSQL'de proje için bir veritabanı ve kullanıcı oluşturun. Bu kullanıcıya gerekli yetkileri verin.
    *   `.env` dosyasındaki veritabanı bilgilerini bu yeni bilgilere göre güncelleyin.
    *   Migration'ları çalıştırın:
        ```bash
        python manage.py migrate
        ```
    *   Gerekirse bir süper kullanıcı oluşturun: `python manage.py createsuperuser`

7.  **Statik Dosyaları Toplayın:**
    Django'nun statik dosyalarını (CSS, JavaScript, resimler) tek bir dizine toplamak için:
    ```bash
    python manage.py collectstatic
    ```
    Bu komut, `settings.py` dosyasındaki `STATIC_ROOT` ile belirtilen dizine tüm statik dosyaları kopyalayacaktır.

8.  **WSGI Sunucusunu Yapılandırın (Örn: Gunicorn):**
    Gunicorn, Django uygulamanızı sunmak için popüler bir WSGI sunucusudur.
    *   Gunicorn'u sanal ortama yükleyin: `pip install gunicorn`
    *   Gunicorn'u projenizle çalıştırmak için bir systemd servis dosyası veya Supervisor script'i oluşturmanız önerilir. Bu, sunucu yeniden başladığında uygulamanızın otomatik olarak başlamasını sağlar.
    *   Örnek bir Gunicorn çalıştırma komutu (proje ana dizinindeyken):
        ```bash
        gunicorn --workers 3 --bind unix:/tmp/akillisehir.sock akillisehir.wsgi:application
        ```
        *   `--workers 3`: Sunucu kaynaklarınıza göre çalışan işlem sayısını ayarlar (genellikle `2 * CPU_CORE_SAYISI + 1`).
        *   `--bind unix:/tmp/akillisehir.sock`: Gunicorn'un Nginx ile iletişim kurmak için kullanacağı bir Unix soketi oluşturur. Alternatif olarak bir IP ve port da belirtebilirsiniz (`--bind 0.0.0.0:8000`).
        *   `akillisehir.wsgi:application`: Projenizin WSGI uygulama nesnesine işaret eder.

9.  **Web Sunucusunu (Ters Proxy) Yapılandırın (Örn: Nginx):**
    Nginx, gelen HTTP isteklerini Gunicorn'a yönlendirmek (ters proxy) ve statik/medya dosyalarını doğrudan sunmak için kullanılır.
    *   Nginx'i sunucunuza kurun.
    *   `/etc/nginx/sites-available/` dizininde projeniz için bir yapılandırma dosyası oluşturun (örn: `akillisehir`):
        ```nginx
        server {
            listen 80;
            server_name sivasakillisehir.gov.tr www.sivasakillisehir.gov.tr; # Alan adlarınızı yazın

            location = /favicon.ico { access_log off; log_not_found off; }

            location /static/ {
                root /path/to/your/project/akillisehir; # STATIC_ROOT ayarınızın bir üst dizini veya doğrudan STATIC_ROOT
                                                       # collectstatic ile dosyaların toplandığı yer.
                                                       # Örneğin, STATIC_ROOT = /path/to/your/project/akillisehir/static_collected ise
                                                       # root /path/to/your/project/akillisehir/static_collected; şeklinde de olabilir.
                                                       # Önemli olan Nginx'in /static/ URL'sini doğru dosya yoluna eşlemesidir.
            }

            location /media/ {
                root /path/to/your/project/akillisehir; # MEDIA_ROOT ayarınızın bir üst dizini veya doğrudan MEDIA_ROOT
            }

            location / {
                include proxy_params;
                proxy_pass http://unix:/tmp/akillisehir.sock; # Gunicorn soket dosyanızın yolu
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
            }
        }
        ```
    *   Bu yapılandırma dosyasını `sites-enabled` dizinine sembolik link ile bağlayın:
        ```bash
        sudo ln -s /etc/nginx/sites-available/akillisehir /etc/nginx/sites-enabled/
        ```
    *   Nginx yapılandırmasını test edin: `sudo nginx -t`
    *   Nginx'i yeniden başlatın: `sudo systemctl restart nginx`

10. **Güvenlik Önlemleri:**
    *   **HTTPS/SSL:** Let's Encrypt gibi bir servis kullanarak siteniz için ücretsiz SSL sertifikası alın ve Nginx yapılandırmanıza ekleyerek HTTPS'i etkinleştirin.
    *   **Güvenlik Duvarı (Firewall):** Sunucunuzda `ufw` gibi bir güvenlik duvarı yapılandırarak sadece gerekli portlara (örn: 80, 443) erişime izin verin.
    *   **Düzenli Güncellemeler:** Sunucu işletim sistemini ve tüm yazılım paketlerini (Python, Django, PostgreSQL vb.) düzenli olarak güncelleyin.

11. **DNS Ayarları:**
    Alan adınızın (örn: `akillisehir.sivas.bel.tr`) DNS kayıtlarını sunucunuzun IP adresine yönlendirin.

Bu adımlar genel bir rehber niteliğindedir. Kullandığınız teknolojilere ve sunucu ortamına göre ek yapılandırmalar veya değişiklikler gerekebilir.

## 📜 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakınız.
