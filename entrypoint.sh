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