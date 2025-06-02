#!/bin/sh

# Sivas Belediyesi Akıllı Şehir Web Portalı
# Docker Entrypoint Script

# Veritabanı bekleme fonksiyonu
wait_for_db() {
    echo "🔄 PostgreSQL veritabanı bekleniyor..."
    
    while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
        echo "⏳ Veritabanı henüz hazır değil. 2 saniye bekleniyor..."
        sleep 2
    done
    
    echo "✅ PostgreSQL veritabanı hazır!"
}

# Veritabanını bekle
if [ "$DATABASE_HOST" ] && [ "$DATABASE_PORT" ]; then
    wait_for_db
fi

# Database migrations
echo "🔄 Veritabanı migrasyonları uygulanıyor..."
python manage.py migrate --noinput

# Static dosyaları topla
echo "🔄 Static dosyalar toplanıyor..."
python manage.py collectstatic --noinput

# Superuser oluştur (sadece gerekirse)
if [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "🔄 Superuser kontrol ediliyor..."
    python manage.py shell << 'PYTHON_EOF'
import os
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' oluşturuldu.")
else:
    print(f"ℹ️ Superuser '{username}' zaten mevcut.")
PYTHON_EOF
fi

# Uygulama başlatma
echo "🚀 Akıllı Şehir Web Portalı başlatılıyor..."
echo "🏛️ Sivas Belediyesi Akıllı Şehir Müdürlüğü"
echo "🌐 Port: ${PORT:-8000}"
echo "👥 Workers: ${GUNICORN_WORKERS:-2}"

# Gunicorn ile Django'yu başlat
exec gunicorn akillisehir.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers ${GUNICORN_WORKERS:-2} \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 2 \
    --log-level info \
    --access-logfile /app/logs/access.log \
    --error-logfile /app/logs/error.log \
    --capture-output \
    --enable-stdio-inheritance