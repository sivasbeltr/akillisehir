#!/bin/sh

# Sivas Belediyesi Akıllı Şehir Web Portalı
# Docker Entrypoint Script

set -e

echo "🚀 Akıllı Şehir Web Portalı başlatılıyor..."
echo "🏛️ Sivas Belediyesi Akıllı Şehir Müdürlüğü"

# Log dizinini oluştur ve izinleri düzelt
mkdir -p /app/logs
chown -R django:django /app/logs
chmod 755 /app/logs

# Ortam değişkenlerini kontrol et
if [ -z "$SECRET_KEY" ]; then
    echo "❌ SECRET_KEY environment variable is required!"
    exit 1
fi

if [ -z "$POSTGRES_HOST" ]; then
    echo "❌ POSTGRES_HOST environment variable is required!"
    exit 1
fi

# MinIO ayarlarını göster (eğer aktifse)
if [ "$USE_MINIO" = "True" ]; then
    echo "✅ MinIO Storage aktif: http://$MINIO_ENDPOINT"
    echo "   📦 Bucket: $MINIO_BUCKET_NAME"
    echo "   🌐 Domain: $MINIO_CUSTOM_DOMAIN"
    echo "   📁 Static: http://$MINIO_CUSTOM_DOMAIN/${MINIO_STATIC_LOCATION:-static}/"
    echo "   📷 Media: http://$MINIO_CUSTOM_DOMAIN/${MINIO_MEDIA_LOCATION:-media}/"
fi

# Veritabanı bağlantısını bekle
echo "🔄 Veritabanı bağlantısı kontrol ediliyor..."
while ! nc -z "$POSTGRES_HOST" "${POSTGRES_PORT:-5432}"; do
    echo "⏳ PostgreSQL bekleniyor ($POSTGRES_HOST:${POSTGRES_PORT:-5432})..."
    sleep 2
done
echo "✅ Veritabanı bağlantısı kuruldu!"

# Django user olarak çalıştır
exec su-exec django:django "$@"